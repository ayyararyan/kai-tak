from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from conditional_model import *
from scipy.optimize import root
from scipy.optimize._numdiff import approx_derivative
HERE=Path(__file__).resolve().parent
seed=np.array(json.loads((OUT/'cases/mean/result.json').read_text())['primary']['q'])
ix=[1,2,3,10,11];sc=np.array([5.,300.,75.,1.,1.]);basewx=Case().p['wind_mps'][0]
# unknowns: five scaled flare coefficients, eta, three normalized interior active times

def unpack(z):
 q=seed.copy();q[ix]=z[:5]*sc;return q

def margins(z,wx):
 q=unpack(z);c=Case(wind=(wx,Case().p['wind_mps'][1],0));polys=c.curves(q)[1]
 ss=np.r_[0.,1.,z[6:9]];p=phase(polys,q[1],ss,c.p)
 return np.array([(2636-q[2]-2*q[3]-q[3]**2/(2*1.4709975))/2636,1-abs(p['slew'][0])/1e5,1-abs(p['slew'][1])/1e5,1-abs(p['slew'][2])/1e5,(1.4-p['load'][3])/.9,p['thrust'][4]/7e5])

def eq(z,wx):
 h=1e-5;der=[]
 for k,index in [(6,3),(7,4),(8,5)]:
  zp=z.copy();zm=z.copy();zp[k]+=h;zm[k]-=h;der.append((margins(zp,wx)[index]-margins(zm,wx)[index])/(2*h))
 return np.r_[margins(z,wx)-z[5],der]

def solve(wx,z):
 rr=root(lambda x:eq(x,wx),z,tol=2e-10)
 z=rr.x;J=approx_derivative(lambda x:eq(x,wx),z,method='3-point',rel_step=1e-4)
 fw=approx_derivative(lambda w:eq(z,w[0]),[wx],method='3-point').reshape(-1)
 dz=-np.linalg.solve(J,fw)
 G=approx_derivative(lambda x:margins(np.r_[x,z[5:]],wx),z[:5],method='3-point')
 weights=np.linalg.solve(np.vstack([G.T,np.ones(6)]),np.r_[np.zeros(5),1.])
 q=unpack(z);c=Case(wind=(wx,Case().p['wind_mps'][1],0));m,h,e,ps=c.evaluate(q,20001,True)
 # Flare-only envelope; approach is deliberately not part of the relaxed local proof.
 p=ps[1];flare={}
 for key,lo,hi in [('eas',135,175),('cl',0,2.8),('load',.5,1.4),('thrust',0,700000)]:flare[key+'_lower']=float(np.min((p[key]-lo)/(hi-lo)));flare[key+'_upper']=float(np.min((hi-p[key])/(hi-lo)))
 for key,cap in [('bank',np.deg2rad(25)),('roll',np.deg2rad(5)),('slew',1e5)]:flare[key]=float(np.min(1-abs(p[key])/cap))
 flare['descent']=float(np.min(1+p['gamma']/np.deg2rad(6)))
 return z,dict(wx_mps=wx,root_success=bool(rr.success),max_equation_residual=float(np.max(abs(eq(z,wx)))),z=z.tolist(),q=q.tolist(),eta=float(z[5]),deta_dwx=float(dz[5]),dq_dwx=(dz[:5]*sc).tolist(),dtimes_dwx=dz[6:].tolist(),multipliers=weights.tolist(),active_jacobian_min_singular=float(np.linalg.svd(np.vstack([G.T,np.ones(6)]),compute_uv=False)[-1]),system_condition=float(np.linalg.cond(J)),flare_sample_minima=flare,full_curve_sample_eta=float(min(map(np.min,m.values()))),full_curve_hard_min=float(min(map(np.min,h.values()))),classification='numerically regular local flare-relaxation branch; no interval existence or global certificate')

if __name__=='__main__':
 z=np.r_[seed[ix]/sc,.15236,.7635,.7425,.36715];z,base=solve(basewx,z);rows=[]
 for delta in [-.2,-.1,-.01,0,.01,.1,.2]:
  zz,r=solve(basewx+delta,z);r['wx_delta']=delta;rows.append(r);print(delta,r['eta'],r['deta_dwx'],min(r['multipliers']),r['max_equation_residual'],flush=True)
 out=dict(active_order=['stop','slew_gate','slew_touchdown','slew_interior','load_upper_interior','thrust_lower_interior'],flare_q_order=['Tf','xD','U','fx','fz'],baseline=base,continuation=rows)
 (HERE/'active_branch.json').write_text(json.dumps(out,indent=2)+'\n')
