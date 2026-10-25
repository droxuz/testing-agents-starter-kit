"""Synthetic regression checks for selection, tracing and literal test export."""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

TOOL = Path(__file__).with_name('select_candidates').resolve()
MODULE = runpy.run_path(str(TOOL))
SOLUTION = '''class Solution:
    def f(self, xs):
        total = 0
        for x in xs:
            if x > 0:
                total += x
        return total
'''


def candidate(xs, reason='positive and nonpositive interaction'):
    return {'args': [xs], 'reason': reason}


class SelectorChecks(unittest.TestCase):
    def invoke(self, candidates, inherited='', solution=SOLUTION, budget=50, existing=False, spec="## Signature\ndef f(self,xs):\n"):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'tests').mkdir()
            (root/'solution.py').write_text(solution)
            (root/'SPEC.md').write_text(spec)
            if inherited:
                (root/'tests/test_blackbox.py').write_text(inherited)
            if existing:
                (root/'tests/test_whitebox.py').write_text('def test_saved(): assert True\n')
            (root/'candidates.json').write_text(json.dumps(candidates))
            protected=[root/'solution.py',root/'candidates.json',root/'SPEC.md']
            if inherited:protected.append(root/'tests/test_blackbox.py')
            before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
            result=subprocess.run([sys.executable,str(TOOL),'candidates.json','--method','f',
                                   '--max-calls',str(budget),'--write'],cwd=root,text=True,
                                   capture_output=True,timeout=25)
            for p,digest in before.items():self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),digest)
            report=json.loads((root/'candidate_report.json').read_text()) if (root/'candidate_report.json').exists() else None
            exported=(root/'tests/test_whitebox.py').read_text() if (root/'tests/test_whitebox.py').exists() else None
            if result.returncode==0 and exported is not None:
                execution=subprocess.run([sys.executable,'-m','pytest','tests/test_whitebox.py','-q'],
                                         cwd=root,text=True,capture_output=True,timeout=10)
                self.assertEqual(execution.returncode,0,execution.stdout+execution.stderr)
            return result,report,exported

    def test_novel_branch_first_and_duplicates_removed(self):
        inherited='from solution import Solution\ndef test_old(): assert Solution().f([1])==1\n'
        r,report,text=self.invoke([candidate([1]),candidate([2]),candidate([-1]),candidate([-1])],inherited)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        selected=report['selected']
        self.assertEqual(selected[0]['index'],2)
        self.assertEqual(len(selected),2)
        self.assertNotIn('oracle',text)
        self.assertIn('from solution import Solution',text)

    def test_same_edges_different_order_trace(self):
        inherited='from solution import Solution\ndef test_old(): assert Solution().f([1,-1])==1\n'
        r,report,_=self.invoke([candidate([-1,1])],inherited)
        self.assertEqual(r.returncode,0,r.stdout)
        self.assertGreater(report['selected'][0]['novel_features'],0)
        self.assertEqual(report['selected'][0]['novel_edges'],0)

    def test_combined_budget_counts_calls_not_test_functions(self):
        inherited='from solution import Solution\ndef test_old():\n for x in [1,2,3]:\n  assert Solution().f([x])==x\n'
        r,report,_=self.invoke([candidate([4]),candidate([-1])],inherited,budget=4)
        self.assertEqual(r.returncode,0,r.stdout)
        self.assertEqual(report['inherited_calls'],3)
        self.assertEqual(len(report['selected']),1)

    def test_inherited_failure_retained_and_reported(self):
        inherited='from solution import Solution\ndef test_old(): assert Solution().f([1])==99\n'
        r,report,_=self.invoke([candidate([-1])],inherited)
        self.assertEqual(r.returncode,0,r.stdout)
        self.assertEqual(report['inherited_pytest_code'],1)

    def test_no_remaining_budget_no_export(self):
        inherited='from solution import Solution\ndef test_old(): assert Solution().f([1])==1\n'
        r,report,text=self.invoke([candidate([-1])],inherited,budget=1)
        self.assertEqual(r.returncode,0,r.stdout)
        self.assertEqual(report['status'],'inherited_budget_exhausted')
        self.assertFalse(report['candidates_executed'])
        self.assertIsNone(text)

    def test_bad_candidate_rejected_without_losing_valid(self):
        r,report,_=self.invoke([candidate(None),candidate([1])])
        self.assertEqual(r.returncode,0,r.stdout)
        self.assertEqual(len(report['rejected']),1)

    def test_nondeterministic_global_state_rejected(self):
        source='counter=0\nclass Solution:\n def f(self,xs):\n  global counter\n  counter+=1\n  return counter\n'
        r,report,text=self.invoke([candidate([1])],solution=source)
        self.assertEqual(r.returncode,1)
        self.assertIn('repeated outputs differ',report['rejected'][0]['error'])
        self.assertIsNone(text)

    def test_existing_new_file_not_overwritten(self):
        r,_,text=self.invoke([candidate([1])],existing=True)
        self.assertEqual(r.returncode,1)
        self.assertEqual(text,'def test_saved(): assert True\n')

    def test_collection_failure_blocks_measurement(self):
        r,_,text=self.invoke([candidate([1])],inherited='import nonexistent_trace_test\n')
        self.assertEqual(r.returncode,1)
        self.assertIsNone(text)

    def test_internal_recursion_does_not_spend_extra_calls(self):
        source = ('class Solution:\n def f(self,xs):\n  if xs:\n'
                  '   return 1+self.f(xs[1:])\n  return 0\n')
        inherited='from solution import Solution\ndef test_old(): assert Solution().f([1,2])==2\n'
        r,report,_=self.invoke([candidate([1]),candidate([])],inherited,solution=source,budget=4)
        self.assertEqual(r.returncode,0,r.stdout)
        self.assertEqual(report['inherited_calls'],1)
        self.assertEqual(len(report['selected']),2)
        self.assertEqual(report['selected'][0]['calls'],1)

    def test_illegal_candidate_rejected_before_target_execution(self):
        spec='Constraints:\n1 <= xs[i] <= 9\n## Signature\ndef f(self,xs):\n'
        source='class Solution:\n def f(self,xs):\n  if min(xs)<1: raise RuntimeError("bad input executed")\n  return sum(xs)\n'
        r,report,_=self.invoke([candidate([-1]),candidate([2])],solution=source,spec=spec)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('illegal input',report['rejected'][0]['error'])
        self.assertNotIn('bad input executed',report['rejected'][0]['error'])
        self.assertTrue(report['known_constraint_checks'])
    def test_dependent_window_constraint(self):
        spec='Constraints:\n1 <= k <= xs.length\n## Signature\ndef f(self,xs,k):\n'
        source='class Solution:\n def f(self,xs,k): return len(xs)+k\n'
        cases=[{'args':[[1],2],'reason':'illegal window'},{'args':[[1,2],2],'reason':'legal window'}]
        r,report,_=self.invoke(cases,solution=source,spec=spec)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('illegal input',report['rejected'][0]['error'])
    def test_matrix_keyword_argument_is_one_input(self):
        spec='## Signature\ndef f(self,intervals):\n'
        source='class Solution:\n def f(self,intervals): return sum(row[2] for row in intervals)\n'
        cases=[{'args':[],'kwargs':{'intervals':[[1,2,5],[3,4,6]]},'reason':'matrix argument'}]
        r,report,text=self.invoke(cases,solution=source,spec=spec)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('intervals=',text)
        self.assertEqual(len(report['selected']),1)
    def test_bad_matrix_nesting_reports_actual_parameter(self):
        spec='## Signature\ndef f(self,intervals):\n'
        source='class Solution:\n def f(self,intervals): return sum(row[2] for row in intervals)\n'
        cases=[{'args':[[1,2,5]],'reason':'malformed matrix'},
               {'args':[],'kwargs':{'intervals':[[1,2,5]]},'reason':'correct matrix'}]
        r,report,_=self.invoke(cases,solution=source,spec=spec)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertEqual(len(report['rejected']),1)
        self.assertIn('Actual parameter names: intervals',r.stdout)
    def test_constructor_consumes_budget(self):
        source='class Solution:\n def __init__(self): self.value=0\n def f(self,xs): return sum(xs)\n'
        inherited='from solution import Solution\ndef test_old(): assert Solution().f([1])==1\n'
        r,report,_=self.invoke([candidate([2]),candidate([3])],inherited,solution=source,budget=5)
        self.assertEqual(r.returncode,0,r.stdout)
        self.assertEqual(report['inherited_calls'],2)
        self.assertEqual(len(report['selected']),1)
        self.assertEqual(report['selected'][0]['calls'],2)

    def test_help(self):
        r=subprocess.run([sys.executable,str(TOOL),'--help'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0)
        self.assertIn('heuristic',r.stdout)

if __name__ == '__main__': unittest.main()
