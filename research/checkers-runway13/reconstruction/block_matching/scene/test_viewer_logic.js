// DOM/Plotly stubs test trace construction only. This is NOT browser/WebGL verification.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const base=__dirname;const source=JSON.parse(fs.readFileSync(path.join(base,'scene.json'),'utf8'));source.render_maps=source.maps.map(m=>({epoch:m.epoch,image:'fixture-image',gray:[[255,255],[255,255]]}));
const els=new Map();function elem(id){if(!els.has(id))els.set(id,{id,checked:['maptoggle'].includes(id),value:id==='epoch'?'1989-10':id==='representation'?'surface':'',textContent:'',innerHTML:'',disabled:false,removeAllListeners(){},on(){}});return els.get(id)}
let latest;const context={console,document:{getElementById:elem,querySelectorAll(){return ['stereo','sources','modern'].map(v=>({dataset:{view:v},classList:{toggle(){}}}))}},Plotly:{react(p,data,layout){latest={data,layout};return Promise.resolve()}},S_INPUT:source};vm.createContext(context);
let js=fs.readFileSync(path.join(base,'template.html'),'utf8').split('<script>').at(-1).split('</script>')[0].replace('/*SCENE_DATA*/','S_INPUT');vm.runInContext(js,context);
assert(latest.data.some(t=>t.type==='mesh3d'&&t.i.length>0));assert(elem('viewtitle').textContent.includes('observed image surfaces'));
elem('representation').value='points';vm.runInContext('render()',context);assert(latest.data.some(t=>t.type==='scatter3d'&&t.mode==='markers'&&t.x.length>100));
vm.runInContext("view='modern';render()",context);assert.equal(latest.data[0].type,'mesh3d');let expectedVertices=0;for(const f of source.modern.features)for(const ring of f.rings_local)expectedVertices+=2*(ring.length-1);assert.equal(latest.data[0].x.length,expectedVertices);assert.equal(latest.data.length,2);assert.equal(latest.layout.scene.zaxis.title,'Elevation (m HKPD)');
vm.runInContext("view='sources';epoch='1997-04';render()",context);assert.equal(latest.data.length,19);assert(latest.data.every(t=>t.type==='scatter'));assert(elem('viewsub').textContent.includes('1997-04'));
vm.runInContext("inspect({kind:'historic',id:S.historical_faces.find(f=>f.source_epoch===epoch).id})",context);assert(elem('details').innerHTML.includes('Unidentified'));
console.log('PASS: default mesh, points selector, courtyard trace construction, separate modern datum, source epoch and click detail logic. Browser/WebGL remains unverified.');
