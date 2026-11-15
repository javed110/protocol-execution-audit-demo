"""Restricted actual-run audit on synthetic events; no causal identification."""
import json,hashlib,copy
from pathlib import Path
DESIGN='new_user_point_treatment_v1'
CLAUSES=('design','protocol_id','time_zero','followup_days','outcome','covariates')
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def code_digest():return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
def validate(p):
 if not isinstance(p,dict) or set(p)!=set(CLAUSES):raise ValueError('protocol schema')
 if p['design']!=DESIGN:raise ValueError('unsupported design')
 if p['time_zero']!='first_eligible_visit' or p['outcome']!='event' or p['covariates']!=[]:raise ValueError('unsupported semantics')
 if type(p['followup_days']) is not int or not 1<=p['followup_days']<=365:raise ValueError('followup')
 if not isinstance(p['protocol_id'],str) or not p['protocol_id']:raise ValueError('protocol ID')
def run(p,rows):
 validate(p); seen=set(); selected=[]
 for r in rows:
  if not isinstance(r,dict) or set(r)!={'id','eligible','treatment','event_day'} or not isinstance(r['id'],str) or not r['id'] or r['id'] in seen or type(r['eligible']) is not bool or r['treatment'] not in ['A','B']:raise ValueError('row schema')
  seen.add(r['id']); day=r['event_day']
  if day is not None and (type(day) is not int or day<0):raise ValueError('event day')
  if r['eligible']:selected.append(r)
 rates={}
 for arm in ['A','B']:
  rs=[r for r in selected if r['treatment']==arm]
  rates[arm]=None if not rs else sum(r['event_day'] is not None and r['event_day']<=p['followup_days'] for r in rs)/len(rs)
 return {'actual':copy.deepcopy(p),'data_sha256':digest(rows),'code_sha256':code_digest(),'cohort_ids':sorted(r['id'] for r in selected),'risks':rates}
def audit(approved,receipt,rows,amendment_id=None,amendments=None):
 target=approved
 if amendment_id is not None:
  if not amendments or amendment_id not in amendments:return {'status':'deviation','reason':'unknown amendment'}
  target=amendments[amendment_id]
 try:validate(target);validate(receipt['actual'])
 except (ValueError,KeyError,TypeError):return {'status':'unsupported','reason':'outside restricted design'}
 differences=[k for k in CLAUSES if target[k]!=receipt['actual'][k]]
 if differences:return {'status':'deviation','clauses':differences}
 expected=run(receipt['actual'],rows)
 if receipt!=expected:return {'status':'deviation','reason':'artifact/execution mismatch'}
 return {'status':'pass','reason':'restricted fidelity only; no causal validity certification'}
def fixture():
 p=dict(design=DESIGN,protocol_id='P1',time_zero='first_eligible_visit',followup_days=30,outcome='event',covariates=[])
 rows=[dict(id='P1',eligible=True,treatment='A',event_day=40),dict(id='P2',eligible=True,treatment='B',event_day=10)]
 return p,rows
def demo():
 p,rows=fixture();receipt=run(p,rows);changed=dict(p,followup_days=60);new=run(changed,rows);unsupported=copy.deepcopy(receipt);unsupported['actual']['design']='dynamic_strategy'
 return {'synthetic_only':True,'faithful':audit(p,receipt,rows),'changed_window':audit(p,new,rows),
 'approved_amendment':audit(p,new,rows,'A1',{'A1':changed}),'unsupported':audit(p,unsupported,rows),'note':'Local recomputation, not secure remote attestation.'}
if __name__=='__main__':print(json.dumps(demo(),indent=2))
