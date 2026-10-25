"""Shared bounded execution support. Reads task files only; never edits tests/source."""
import argparse
import ast
import contextlib
import functools
import hashlib
import io
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import types
from pathlib import Path


MAX_SOURCE = 200_000


def inside(root, name, *, exists=True):
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('path must be inside the current task folder')
    if exists and not path.is_file():
        raise ValueError(f'file not found: {name}')
    return path


def read_source(root, name='solution.py'):
    path = inside(root, name)
    if path.stat().st_size > MAX_SOURCE:
        raise ValueError('source must not exceed 200 KB')
    text = path.read_text(encoding='utf-8-sig')
    ast.parse(text)
    return path, text


def method_name(root, source, requested=None):
    tree = ast.parse(source)
    cls = next((n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Solution'), None)
    if cls is None:
        raise ValueError('source must define class Solution')
    methods = {n.name: n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    if requested:
        if requested not in methods:
            raise ValueError(f'Solution has no declared method {requested!r}')
        chosen = requested
    else:
        public = [n for n in methods if not n.startswith('_')]
        spec_path = root / 'SPEC.md'
        signatures = set()
        if spec_path.is_file():
            spec_path = inside(root, 'SPEC.md')
        if spec_path.is_file() and spec_path.stat().st_size <= MAX_SOURCE:
            signatures = set(re.findall(r'\bdef\s+([A-Za-z_]\w*)\s*\(', spec_path.read_text()))
        matches = [n for n in public if n in signatures]
        if len(matches) == 1:
            chosen = matches[0]
        elif len(public) == 1:
            chosen = public[0]
        else:
            raise ValueError('ambiguous target method; specify --method NAME')
    if isinstance(methods[chosen], ast.AsyncFunctionDef):
        raise ValueError('async target methods are not supported')
    return chosen


def preview(value, depth=0):
    """Bound diagnostic output. Tagged/truncated values are not executable oracles."""
    if value is None or type(value) in (bool, int):
        return value
    if type(value) is float:
        return value if math.isfinite(value) else {'type': 'float', 'repr': repr(value)}
    if type(value) is str:
        return value if len(value) <= 500 else {'type': 'str', 'prefix': value[:500], 'length': len(value)}
    if depth >= 5:
        return {'type': type(value).__name__, 'truncated': True}
    if type(value) in (list, tuple):
        parts = [preview(v, depth + 1) for v in value[:30]]
        if type(value) is list and len(value) <= 30:
            return parts
        return {'type': type(value).__name__, 'items': parts, 'length': len(value)}
    if type(value) is dict:
        items = list(value.items())[:30]
        if len(value) <= 30 and all(type(k) is str for k in value):
            return {k: preview(v, depth + 1) for k, v in items}
        return {'type': 'dict', 'items': [[preview(k, depth + 1), preview(v, depth + 1)] for k, v in items], 'length': len(value)}
    return {'type': type(value).__name__, 'opaque': True}


def short_error(error):
    return f'{type(error).__name__}: {str(error)[:1000]}'


class Capture(io.TextIOBase):
    def __init__(self):
        self.tail = ''

    def write(self, text):
        self.tail = (self.tail + str(text)[-3000:])[-3000:]
        return len(text)

    def flush(self):
        pass


def load_solution(root, source):
    module = types.ModuleType('solution')
    module.__file__ = str(root / 'solution.py')
    sys.modules['solution'] = module
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    return module


class Recorder:
    def __init__(self):
        self.current = None
        self.phase = 'collection'
        self.calls = []
        self.counts = {}
        self.fingerprints = {}

    def instrument(self, module, method):
        descriptor = vars(module.Solution)[method]
        function = descriptor.__func__ if isinstance(descriptor, (staticmethod, classmethod)) else descriptor
        skip_first = not isinstance(descriptor, staticmethod)

        @functools.wraps(function)
        def recorded(*args, **kwargs):
            nodeid, phase = self.current, self.phase
            self.counts[nodeid] = self.counts.get(nodeid, 0) + 1
            values = args[1:] if skip_first else args
            before = preview({'args': list(values), 'kwargs': kwargs})
            event = {'nodeid': nodeid, 'phase': phase, 'input': before}
            # Keep examples compact, while counts include every invocation.
            saved = sum(e['nodeid'] == nodeid for e in self.calls) < 3 and len(self.calls) < 300
            if saved:
                self.calls.append(event)
                fingerprint = hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest()[:12]
                self.fingerprints.setdefault(fingerprint, []).append(nodeid)
            try:
                value = function(*args, **kwargs)
            except BaseException as error:
                if saved:
                    event['raised'] = short_error(error)
                raise
            else:
                if saved:
                    event['returned'] = preview(value)
                return value
            finally:
                if saved:
                    event['input_after'] = preview({'args': list(values), 'kwargs': kwargs})

        wrapped = staticmethod(recorded) if isinstance(descriptor, staticmethod) else classmethod(recorded) if isinstance(descriptor, classmethod) else recorded
        setattr(module.Solution, method, wrapped)


def suite_worker(root, source, method, scratch):
    import pytest

    recorder = Recorder()
    recorder.instrument(load_solution(root, source), method)

    class Plugin:
        def __init__(self):
            self.order = []
            self.reports = {}
            self.collection_errors = []

        def pytest_collection_finish(self, session):
            self.order = [item.nodeid for item in session.items]

        def pytest_collectreport(self, report):
            if report.failed:
                self.collection_errors.append({'nodeid': report.nodeid, 'detail': str(report.longrepr)[-2000:]})

        @pytest.hookimpl(tryfirst=True)
        def pytest_runtest_setup(self, item):
            recorder.current, recorder.phase = item.nodeid, 'setup'

        @pytest.hookimpl(tryfirst=True)
        def pytest_runtest_call(self, item):
            recorder.current, recorder.phase = item.nodeid, 'call'

        @pytest.hookimpl(tryfirst=True)
        def pytest_runtest_teardown(self, item):
            recorder.current, recorder.phase = item.nodeid, 'teardown'

        def pytest_runtest_logreport(self, report):
            result = {'phase': report.when, 'outcome': report.outcome}
            if report.failed:
                result['detail'] = str(report.longrepr)[-2500:]
            self.reports.setdefault(report.nodeid, []).append(result)

        def pytest_runtest_logfinish(self, nodeid, location):
            recorder.current, recorder.phase = None, 'between-tests'

    plugin = Plugin()
    tests_dir = (root / 'tests').resolve()
    if not tests_dir.is_relative_to(root):
        raise ValueError('tests directory must be inside the task folder')
    files = []
    for path in sorted(tests_dir.glob('test_*.py')):
        if path.is_file():
            checked = inside(root, str(path))
            files.append(str(checked.relative_to(root)))
    if not files:
        return {'status': 'no_tests', 'method': method, 'tests': [], 'calls_total': 0, 'calls_outside_tests': 0}
    config = scratch / 'pytest.ini'
    config.write_text('[pytest]\n')
    code = int(pytest.main([*files, '-c', str(config), '--rootdir', str(root), '-q', '--tb=short', '--no-header', '--noconftest',
                           '--confcutdir', str(root), '-p', 'no:cacheprovider', '--capture=no'], plugins=[plugin]))
    tests = []
    for nodeid in plugin.order:
        phases = plugin.reports.get(nodeid, [])
        outcome = 'failed' if any(p['outcome'] == 'failed' for p in phases) else 'skipped' if any(p['outcome'] == 'skipped' for p in phases) else 'passed' if any(p['phase'] == 'call' and p['outcome'] == 'passed' for p in phases) else 'not_run'
        tests.append({'nodeid': nodeid, 'outcome': outcome, 'calls': recorder.counts.get(nodeid, 0),
                      'failures': [p for p in phases if p['outcome'] == 'failed']})
    outside = recorder.counts.get(None, 0)
    return {'status': 'completed', 'method': method, 'pytest_exit_code': code, 'tests': tests,
            'collection_errors': plugin.collection_errors, 'calls_total': sum(recorder.counts.values()),
            'calls_outside_tests': outside, 'call_examples': recorder.calls,
            'repeated_recorded_inputs': [{'fingerprint': key, 'nodeids': ids} for key, ids in recorder.fingerprints.items() if len(ids) > 1],
            'notes': ['Counts include recursive target entries and fixture calls in this run.',
                      'Failure/skip paths may execute fewer calls than repaired tests.',
                      'Only test_*.py files are collected; conftest files and external pytest plugins are disabled.',
                      'Input previews are bounded; repeated previews are hints, not proof of redundant tests.']}


def execute(root, source, method, *, timeout=20):
    """Execute one isolated worker with transient files confined to the task folder."""
    with tempfile.TemporaryDirectory(prefix='.whitebox-', dir=root) as directory:
        request_path, report_path = Path(directory) / 'request.json', Path(directory) / 'report.json'
        request_path.write_text(json.dumps({'source': source, 'method': method}))
        env = os.environ | {'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1', 'PYTHONDONTWRITEBYTECODE': '1',
                            'PYTEST_ADDOPTS': '', 'PYTEST_PLUGINS': ''}
        try:
            result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '_worker',
                                     str(request_path), str(report_path)], cwd=root, env=env,
                                    text=True, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {'status': 'timeout', 'timeout_seconds': timeout}
        if not report_path.exists():
            return {'status': 'worker_error', 'detail': (result.stderr + result.stdout)[-2000:]}
        report = json.loads(report_path.read_text())
        if result.returncode:
            report['worker_exit_code'] = result.returncode
        return report


def worker(request_name, report_name):
    root = Path.cwd().resolve()
    request_path, report_path = inside(root, request_name), inside(root, report_name, exists=False)
    request = json.loads(request_path.read_text())
    capture = Capture()
    with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
        try:
            report = suite_worker(root, request['source'], request['method'], request_path.parent)
        except BaseException as error:
            report = {'status': 'execution_error', 'detail': short_error(error)}
    report['captured_output_tail'] = capture.tail
    report_path.write_text(json.dumps(report, allow_nan=False))


def common_parser(description):
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--method', help='target method; inferred from SPEC/signature or the sole public method')
    parser.add_argument('--timeout', type=float, default=20, help='overall execution timeout, 0.1-100 seconds (default %(default)s)')
    parser.add_argument('--json', action='store_true', help='emit structured JSON instead of compact text')
    return parser


def prepare(args):
    if not 0.1 <= args.timeout <= 100:
        raise ValueError('--timeout must be 0.1-100 seconds')
    root = Path.cwd().resolve()
    _, source = read_source(root)
    method = method_name(root, source, args.method)
    return root, source, method


def json_output(report):
    print(json.dumps(report, indent=2, ensure_ascii=True, allow_nan=False))


def suite_passed(report):
    return (report.get('status') == 'completed' and report.get('pytest_exit_code') == 0
            and bool(report.get('tests')) and not report.get('collection_errors')
            and all(t['outcome'] in ('passed', 'skipped') for t in report['tests']))


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '_worker':
        worker(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit('Internal execution helper; use the documented tool commands.')
