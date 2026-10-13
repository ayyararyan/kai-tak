// Logic-only DOM stub. This is not browser, layout or accessibility verification.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const nodes=new Map();
function node(id){if(!nodes.has(id))nodes.set(id,{attrs:{},dataset:{},open:false,setAttribute(k,v){this.attrs[k]=v},addEventListener(k,v){this[k]=v},showModal(){this.open=true},close(){this.open=false}});return nodes.get(id)}
const ctx={document:{querySelector:node,querySelectorAll:()=>[]}};vm.createContext(ctx);
vm.runInContext(fs.readFileSync(__dirname+'/gallery-script.js','utf8'),ctx);
let passed=0;function check(v){assert(v);passed++}
check((node('#gallery').innerHTML.match(/<article /g)||[]).length===12);
check(node('#gallery').innerHTML.includes('atlas-04-evidence.png'));
check(node('#gallery').innerHTML.includes('atlas-06-evidence.png'));
check(node('#gallery').innerHTML.includes('atlas-12-evidence.png'));
node('#context').onclick();check(node('#context').attrs['aria-pressed']===true);
check(!node('#gallery').innerHTML.includes('atlas-04-evidence.png'));
vm.runInContext('openImage(11)',ctx);check(node('#viewer').open);check(node('#download').href.includes('12-visual-atlas.png'));
node('#next').onclick();check(node('#counter').textContent.startsWith('01 / 12'));
node('#prev').onclick();check(node('#counter').textContent.startsWith('12 / 12'));
node('#close').onclick();check(!node('#viewer').open);
node('#evidence').onclick();vm.runInContext('openImage(3)',ctx);check(node('#download').href.includes('04-evidence.png'));
const result={verified_utc:new Date().toISOString(),checks_passed:passed,failed:0,scope:'JavaScript state logic with minimal DOM stub; not browser/layout/accessibility verification'};
fs.writeFileSync(__dirname+'/gallery-state-check.json',JSON.stringify(result,null,2)+'\n');console.log(result);
