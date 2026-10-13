"""Additional V3 calculations and calm-family bound; never modify frozen evidence."""
from pathlib import Path
import json,math,sys,csv
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'evidence/analytical/coupled'))
import existence_and_bounds as b
r={'vertical_speed':b.vertical_bound(),'family_upper_bound':b.stronger_bound()}
saved=json.loads((P/'evidence/analytical/coupled/existence_bounds.json').read_text())
assert r==saved
(P/'qa/fresh_existence_bounds.json').write_text(json.dumps(r,indent=2)+'\n')
i=json.loads((P/'qa/insight_calculations.json').read_text());turn=i['turn_78mps_15deg'];g=9.80665
assert math.isclose(turn['radius_m'],78**2/(g*math.tan(math.pi/12)),rel_tol=1e-13)
assert math.isclose(turn['time_47deg_s'],math.radians(47)/(g*math.tan(math.pi/12)/78),rel_tol=1e-13)
assert math.isclose(i['stop']['speed_10pct_braking_ratio'],1.21)
assert abs(78*math.sin(math.radians(-3.1))+4.218)<.001
ob=json.loads((P/'evidence/reconstruction/obstacles/readiness.json').read_text())
assert (ob['accepted_source_observations'],ob['distinct_digitized_sites'],ob['complete_obstacle_volumes'],ob['physical_upper_bounds_available'],ob['historical_clearance_ready'])==(24,12,0,0,False)
w=list(csv.DictReader((P/'evidence/evidence/cal605_reconstruction/wind/wind_records.csv').open()))
assert len(w)==225
(P/'qa/v3_claim_checks.json').write_text(json.dumps({'calm_regularity_and_upper_bound_fresh_match':True,'turn_benchmark':True,'quadratic_speed_sensitivity':True,'straight_descent_mps':78*math.sin(math.radians(-3.1)),'control_hull_share':3780/171307,'obstacle_status_verified':True,'weather_pairs':len(w)},indent=2)+'\n')
print('V3 explanatory calculations, obstacle status and fresh calm-family interval bound passed.')
