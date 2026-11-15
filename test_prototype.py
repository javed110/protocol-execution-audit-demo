import unittest,copy
from prototype import *
class AuditTests(unittest.TestCase):
 def test_actual_execution_risks(self):
  p,r=fixture();self.assertEqual(run(p,r)['risks'],{'A':0,'B':1})
 def test_faithful_pass(self):
  p,r=fixture();self.assertEqual(audit(p,run(p,r),r)['status'],'pass')
 def test_changed_window_deviation(self):
  p,r=fixture();q=dict(p,followup_days=60);self.assertEqual(audit(p,run(q,r),r)['clauses'],['followup_days'])
 def test_approved_amendment(self):
  p,r=fixture();q=dict(p,followup_days=60);self.assertEqual(audit(p,run(q,r),r,'A1',{'A1':q})['status'],'pass')
 def test_self_approved_amendment_refused(self):
  p,r=fixture();self.assertEqual(audit(p,run(p,r),r,'MADE_UP',{})['status'],'deviation')
 def test_forged_receipt(self):
  p,r=fixture();s=run(p,r);s['risks']['A']=1;self.assertEqual(audit(p,s,r)['status'],'deviation')
 def test_changed_data_and_code_digest(self):
  p,r=fixture();s=run(p,r);r[0]['event_day']=1;self.assertEqual(audit(p,s,r)['status'],'deviation')
  s=run(p,r);s['code_sha256']='0'*64;self.assertEqual(audit(p,s,r)['status'],'deviation')
 def test_unsupported(self):
  p,r=fixture();s=run(p,r);s['actual']['design']='dynamic';self.assertEqual(audit(p,s,r)['status'],'unsupported')
 def test_duplicate_and_boolean_window(self):
  p,r=fixture()
  with self.assertRaises(ValueError):run(p,r+r)
  p['followup_days']=True
  with self.assertRaises(ValueError):run(p,r)
if __name__=='__main__':unittest.main()
