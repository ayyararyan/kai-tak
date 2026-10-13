from search import *
seed=json.loads((OUT/'cases/urban45/result.json').read_text())['selected']['q']
calm=json.loads((OUT/'cases/calm/result.json').read_text())['selected']['q']
for c in [Case('urban50',urban=50),Case('urban55',urban=55),Case('urban60',urban=60),Case('tailwind2',wind=(2*tr.KT,0,0))]:
 pert=np.clip(np.array(seed)+np.array([3,0,0,0,0,0,20,-10,12,-5,0,0]),BOUNDS[:,0],BOUNDS[:,1])
 q=run(c,[seed,calm,pert])
 if q is not None:seed=q
