"""Bounded subprocess worker for the white-box candidate selector (not an agent tool)."""
import ast
from collections import Counter
import contextlib
import copy
import hashlib
import importlib
import inspect
import io
import json
import runpy
from pathlib import Path
import sys
import tempfile


def canonical(bound):
    return json.dumps(bound, sort_keys=True, separators=(',', ':'), allow_nan=False)


def literal_result(value):
    text = repr(value)
    if len(text) > 16384:
        raise ValueError('result too large for literal export')
    decoded = ast.literal_eval(text)
    if type(decoded) is not type(value) or decoded != value:
        raise ValueError('unsupported result type or unstable representation')
    return text


class Recorder:
    def __init__(self, target, signature):
        self.code = target.__code__
        self.signature = signature
        self.filename = self.code.co_filename
        self.active = None
        self.records = []
        self.target_calls = 0

    def profile(self, frame, event, arg):
        # Count entries from outside the solution, including constructors and helpers.
        # Internal recursion contributes trace features but consumes no extra entry.
        if (event == 'call' and frame.f_code.co_name != '<module>'
                and frame.f_code.co_filename == self.filename):
            caller = frame.f_back
            if caller is None or caller.f_code.co_filename != self.filename:
                self.target_calls += 1

    def trace(self, frame, event, arg):
        if event == 'call' and frame.f_code is self.code and self.active is None:
            if len(self.records) >= 1000:
                raise RuntimeError('too many inherited calls for bounded tracing')
            self.active = frame
            self.edges = Counter()
            self.previous = {}
            self.digest = hashlib.sha256()
            self.events = 0
            try:
                self.key = canonical({name: frame.f_locals[name] for name in self.signature.parameters})
            except (ValueError, TypeError, KeyError):
                self.key = None
        if self.active is not None and frame.f_code.co_filename == self.filename:
            if event == 'line':
                self.events += 1
                if self.events > 200000:
                    raise RuntimeError('trace event limit exceeded')
                identity = (frame.f_code.co_name, frame.f_code.co_firstlineno)
                location = (*identity, frame.f_lineno)
                previous = self.previous.get(id(frame))
                if previous is not None:
                    self.edges[(previous, location)] += 1
                self.previous[id(frame)] = location
                self.digest.update(repr(location).encode())
            elif event == 'return':
                self.previous.pop(id(frame), None)
                if frame is self.active:
                    features = {'trace:' + self.digest.hexdigest()}
                    for edge, count in self.edges.items():
                        features.add('edge:' + repr(edge))
                        features.add('count:' + repr(edge) + ':' + str(count.bit_length()))
                    self.records.append({'key': self.key, 'features': sorted(features)})
                    self.active = None
        return self.trace


def run(request):
    sys.path.insert(0, str(Path.cwd()))
    module = importlib.import_module('solution')
    method = request['method']
    target = getattr(module.Solution(), method)
    signature = inspect.signature(target)
    recorder = Recorder(target, signature)
    if request['mode'] == 'baseline':
        if not Path('tests/test_blackbox.py').exists():
            return {'records': [], 'calls': 0, 'pytest_code': None}
        import pytest
        sys.setprofile(recorder.profile)
        sys.settrace(recorder.trace)
        try:
            code = pytest.main(['tests/test_blackbox.py', '-q', '--tb=no', '-p', 'no:cacheprovider'])
        finally:
            sys.settrace(None)
            sys.setprofile(None)
        if code not in (0, 1):
            raise ValueError(f'inherited collection/execution could not be measured: pytest exit {code}')
        return {'records': recorder.records, 'calls': recorder.target_calls, 'pytest_code': code}
    input_tools=runpy.run_path(str(Path(__file__).resolve().parents[1]/'blackbox'/'check_inputs'))
    declared,params,bounds,symbols,dependent,unparsed,mappings=input_tools['prepare'](Path('SPEC.md').read_text())
    if declared!=method or set(params)!=set(signature.parameters):
        raise ValueError('method/signature does not match SPEC.md')
    rows = []
    for index, candidate in enumerate(request['candidates']):
        try:
            args, kwargs = copy.deepcopy(candidate['args']), copy.deepcopy(candidate.get('kwargs', {}))
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            failures,unknown=input_tools['validate'](bound.arguments,bounds,symbols,dependent,mappings)
            if failures:raise ValueError('illegal input: '+failures[0])
            key = canonical(bound.arguments)
            outputs, features, costs = [], None, []
            for _ in range(2):
                start = len(recorder.records)
                calls_before = recorder.target_calls
                sys.setprofile(recorder.profile)
                sys.settrace(recorder.trace)
                try:
                    output = getattr(module.Solution(), method)(*copy.deepcopy(candidate['args']),
                                                              **copy.deepcopy(candidate.get('kwargs', {})))
                finally:
                    sys.settrace(None)
                    sys.setprofile(None)
                outputs.append(literal_result(output))
                costs.append(recorder.target_calls - calls_before)
                if len(recorder.records) != start + 1:
                    raise ValueError('target trace missing or nested invocation unsupported')
                current = recorder.records[-1]['features']
                if features is not None and features != current:
                    raise ValueError('repeated execution trace changed')
                features = current
            if outputs[0] != outputs[1]:
                raise ValueError('repeated outputs differ')
            rows.append({'index': index, 'key': key, 'expected': outputs[0], 'features': features, 'calls': max(costs), 'unresolved_bounds': unknown})
        except Exception as error:
            sys.settrace(None)
            sys.setprofile(None)
            recorder.active = None
            rows.append({'index': index, 'error': type(error).__name__ + ': ' + str(error)[:180]})
    return {'rows': rows, 'parameters': list(signature.parameters), 'unparsed_rules': len(unparsed)}


if __name__ == '__main__':
    try:
        request = json.load(sys.stdin)
        # Discard implementation/pytest prints; only JSON reaches the parent.
        with tempfile.TemporaryFile(mode='w+') as discarded:
            with contextlib.redirect_stdout(discarded), contextlib.redirect_stderr(discarded):
                result = run(request)
        print(json.dumps(result, allow_nan=False))
    except Exception as error:
        sys.settrace(None)
        sys.setprofile(None)
        print(json.dumps({'error': type(error).__name__ + ': ' + str(error)[:300]}))
        sys.exit(1)
