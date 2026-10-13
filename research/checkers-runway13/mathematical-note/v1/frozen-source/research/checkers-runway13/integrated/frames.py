"""Explicit frame transforms. Numeric consistency does not validate historical datum."""
import math,numpy as np
from pyproj import Transformer
from clearance import finite

def official_itrf96_to_hk1980(lon_deg,lat_deg,ellipsoidal_height_m=0):
 finite([lon_deg,lat_deg,ellipsoidal_height_m])
 xyz=np.array(Transformer.from_crs('+proj=longlat +ellps=GRS80 +type=crs','+proj=geocent +ellps=GRS80 +units=m +type=crs',always_xy=True).transform(lon_deg,lat_deg,ellipsoidal_height_m))
 rx,ry,rz=np.radians(np.array([.067741,-2.243649,-1.158827])/3600);s=1.094239e-6
 M=np.array([[1+s,rz,-ry],[-rz,1+s,rx],[ry,-rx,1+s]])
 hk=M@xyz+np.array([162.619,276.961,161.763])
 llh=Transformer.from_crs('+proj=geocent +ellps=intl +units=m +type=crs','+proj=longlat +ellps=intl +type=crs',always_xy=True).transform(*hk)
 return Transformer.from_crs('EPSG:4611','EPSG:2326',always_xy=True).transform(*llh[:2])

def runway_to_grid(xyz,threshold_EN,grid_bearing_deg,runway_HKPD_m):
 """All datum/registration inputs mandatory; none inferred from chart AMSL."""
 if threshold_EN is None or grid_bearing_deg is None or runway_HKPD_m is None:raise ValueError('unresolved registration/datum')
 p=finite(xyz);o=finite(threshold_EN);finite([grid_bearing_deg,runway_HKPD_m])
 if p.shape[-1]!=3 or o.shape!=(2,):raise ValueError('dimensions')
 b=math.radians(grid_bearing_deg);A=np.array([[math.sin(b),math.cos(b),0],[math.cos(b),-math.sin(b),0],[0,0,1]])
 return p@A.T+np.array([*o,runway_HKPD_m])

def grid_to_runway(enu,threshold_EN,grid_bearing_deg,runway_HKPD_m):
 if threshold_EN is None or grid_bearing_deg is None or runway_HKPD_m is None:raise ValueError('unresolved registration/datum')
 p=finite(enu);o=finite(threshold_EN);finite([grid_bearing_deg,runway_HKPD_m])
 if p.shape[-1]!=3 or o.shape!=(2,):raise ValueError('dimensions')
 b=math.radians(grid_bearing_deg);A=np.array([[math.sin(b),math.cos(b),0],[math.cos(b),-math.sin(b),0],[0,0,1]])
 return (p-np.array([*o,runway_HKPD_m]))@A

def steady_wind_domain(wind_from_true_deg,speed_kt,runway_true_deg,condition):
 finite([wind_from_true_deg,speed_kt,runway_true_deg])
 if speed_kt<0:raise ValueError('negative windspeed')
 limits={'dry':25.,'wet_no_standing_water':22.,'standing_water_or_slush':10.}
 if condition not in limits:raise ValueError('unsupported landing condition')
 d=math.radians(wind_from_true_deg-runway_true_deg);head=speed_kt*math.cos(d);cross=-speed_kt*math.sin(d);limit=limits[condition]
 return {'headwind_kt':head,'rightward_crosswind_kt':cross,'crosswind_limit_kt':limit,'source_condition_passes':abs(cross)<=limit,'full_landing_feasible':None,'gust_policy_certified':False,'scope':'CAD Report1/95 pp49-50 airline limits; true bearing is supplied, not historical survey inferred'}
