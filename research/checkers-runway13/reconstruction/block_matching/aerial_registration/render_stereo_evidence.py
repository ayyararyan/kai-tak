from pathlib import Path
import csv,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
r=list(csv.DictReader((HERE/'dense_stereo_points.csv').open()))
a=np.array([[float(z['easting_hk1980_m']),float(z['northing_hk1980_m']),float(z['z_above_fitted_local_park_road_plane_m']),float(z['r'])/255] for z in r]);print('bounds',a[:,:3].min(0),a[:,:3].max(0))
# Image only: metric XYZ unchanged; narrow photograph-derived points, no interpolation or solid mesh.
sel=(a[:,0]>837430)&(a[:,0]<838050)&(a[:,1]>820990)&(a[:,1]<821620)
v=a[sel];fig=plt.figure(figsize=(14,9),facecolor='#f3f0e8');ax=fig.add_subplot(projection='3d',facecolor='#f3f0e8');ax.scatter(v[:,0]-837400,v[:,1]-821000,v[:,2],c=np.tile(v[:,3,None],(1,3)),s=1.7,linewidth=0,depthshade=False)
ax.view_init(elev=38,azim=-65);ax.set_box_aspect((620,630,130));ax.set_xlim(30,650);ax.set_ylim(-10,620);ax.set_zlim(-25,105);ax.set_xlabel('Easting minus 837400 m');ax.set_ylabel('Northing minus 821000 m');ax.set_zlabel('Metres above fitted local ground plane')
ax.set_title('Kowloon City from two actual photographs, 2 November 1993\nFiltered dense stereo points · nominal camera calibration · relative heights',fontsize=14,pad=14)
fig.text(.06,.04,'Observed image correspondences, not extruded modern buildings. Nominal-camera/ground-plane assumptions remain.\nHorizontal controls are local; vertical coordinate is NOT HKPD. No surface mesh or obstacle completeness is inferred.',fontsize=10,color='#444444')
fig.savefig(HERE/'dense_stereo_evidence.png',dpi=180,bbox_inches='tight');plt.close(fig)
