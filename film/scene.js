import * as THREE from './vendor/three.module.js';
import {gsap} from './vendor/gsap/index.js';
// All positions and motion derive from seek(t); no clock, no external visual assets.
const spec=await(await fetch('timing.json')).json();
for(let i=0;i<3;i++){const lines=spec.scenes[i].text;document.querySelector('#c'+(i+1)+' h1').innerHTML=lines[0]+'<br><span>'+lines[1]+'</span>';}document.querySelector('#c4 h1').innerHTML=spec.scenes[3].text.slice(2).join('<br>');
let seed=spec.seed;const rand=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296};
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)), smooth=x=>{x=clamp(x);return x*x*(3-2*x)}, mix=(a,b,t)=>a+(b-a)*t;
const V=(x,y,z)=>new THREE.Vector3(x,y,z);
const scene=new THREE.Scene();scene.background=new THREE.Color('#17384d');scene.fog=new THREE.FogExp2('#2c5065',.0062);
const renderer=new THREE.WebGLRenderer({canvas:document.querySelector('canvas'),antialias:true,preserveDrawingBuffer:true});renderer.setSize(1920,1080);renderer.setPixelRatio(1);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.24;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const camera=new THREE.PerspectiveCamera(39,1920/1080,.1,500);
scene.add(new THREE.HemisphereLight('#caeeff','#28415b',2.4));const sun=new THREE.DirectionalLight('#fff1de',3.8);sun.position.set(-35,65,20);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-60,right:60,top:55,bottom:-55,near:1,far:170});sun.shadow.bias=-.0005;sun.shadow.normalBias=.12;scene.add(sun);sun.target.position.set(0,0,0);scene.add(sun.target);
const mats={snow:new THREE.MeshStandardMaterial({color:'#effaff',roughness:.87,flatShading:true}),ice:new THREE.MeshStandardMaterial({color:'#8ec6dc',roughness:.6,metalness:.15,flatShading:true}),rock:new THREE.MeshStandardMaterial({color:'#17354a',roughness:.95,flatShading:true}),navy:new THREE.MeshStandardMaterial({color:'#0c2637',roughness:.5}),blue:new THREE.MeshStandardMaterial({color:'#45bcf0',roughness:.35,metalness:.25}),dark:new THREE.MeshStandardMaterial({color:'#071f31',roughness:.6}),wood:new THREE.MeshStandardMaterial({color:'#3c5864',roughness:.8}),glass:new THREE.MeshStandardMaterial({color:'#7fddf4',roughness:.2,metalness:.6}),light:new THREE.MeshStandardMaterial({color:'#ddf8ff',emissive:'#9be9ff',emissiveIntensity:1.5}),warm:new THREE.MeshStandardMaterial({color:'#fff0ca',emissive:'#ffd999',emissiveIntensity:.8})};
function mesh(g,m,p=V(0,0,0),parent=scene){const o=new THREE.Mesh(g,m);o.position.copy(p);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o}
function box(w,h,d,m,p,parent=scene){return mesh(new THREE.BoxGeometry(w,h,d),m,p,parent)}
function ball(r,m,p,parent=scene){return mesh(new THREE.SphereGeometry(r,12,8),m,p,parent)}
function rod(a,b,r,m,parent=scene){let d=b.clone().sub(a),o=mesh(new THREE.CylinderGeometry(r,r,d.length(),8),m,a.clone().add(b).multiplyScalar(.5),parent);o.quaternion.setFromUnitVectors(V(0,1,0),d.normalize());return o}
function tube(points,r,m,parent=scene){return mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points),Math.max(30,points.length*3),r,6,false),m,V(0,0,0),parent)}
function label(text,w=6,h=1.6,bg='#0b2638',fg='#def8ff',parent=scene){let c=document.createElement('canvas');c.width=768;c.height=192;let x=c.getContext('2d');x.fillStyle=bg;x.fillRect(0,0,768,192);x.fillStyle=fg;x.font='bold 90px Text';x.textAlign='center';x.textBaseline='middle';x.fillText(text,384,104);let tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;return mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({map:tex,side:THREE.DoubleSide}),V(0,0,0),parent)}
// Procedural triangulated mountain ridges. Irregular radial rings, no imported meshes.
function mountain(x,z,r,h,s){const n=13;let verts=[],idx=[];for(let j=0;j<5;j++){let f=j/4;for(let i=0;i<n;i++){let a=i/n*Math.PI*2,rr=r*(1-f)*(1+.17*Math.sin(i*8.3+s+j));verts.push(x+Math.cos(a)*rr, h*Math.pow(f,1.28)+(j>0&&j<4?Math.sin(i*3.7+s+j)*h*.08:0)-4,z+Math.sin(a)*rr)}}for(let j=0;j<4;j++)for(let i=0;i<n;i++){let a=j*n+i,b=j*n+(i+1)%n,c=(j+1)*n+i,d=(j+1)*n+(i+1)%n;idx.push(a,b,c,b,d,c)}let g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));g.setIndex(idx);g.computeVertexNormals();return mesh(g,mats.snow)}
for(let i=0;i<12;i++)mountain(-110+i*20,-65-rand()*18,18+rand()*17,22+rand()*28,i*3);
// Main floating alpine massif and sculpted continuous descent.
// Foreground terrain is one uninterrupted surface: no intersecting peak meshes.
function height(x,z){return 1.5+17*Math.exp(-((x+8)**2/600+(z+23)**2/850))+1.2*Math.sin(x*.12+z*.12)}
let tg=new THREE.PlaneGeometry(77,85,45,49);tg.rotateX(-Math.PI/2);let pos=tg.attributes.position;for(let i=0;i<pos.count;i++){const x=pos.getX(i),z=pos.getZ(i);pos.setY(i,height(x,z))}tg.computeVertexNormals();mesh(tg,mats.snow);
const path=new THREE.CatmullRomCurve3([V(-11,0,-32),V(-5,0,-22),V(4,0,-14),V(9,0,-4),V(5,0,7),V(12,0,18),V(20,0,27)]);
function onPath(u,offset=0){let p=path.getPoint(clamp(u));p.x+=offset;p.y=height(p.x,p.z)+.12;return p}
for(let side of [-1,1]){let points=[];for(let i=0;i<130;i++){let p=onPath(i/129,side*3.1);points.push(p)}tube(points,.065,mats.blue)}
// Fine, paired carved tracks alongside the skier.
for(let offset of [-.21,.21]){let ps=[];for(let i=0;i<140;i++){let p=onPath(i/139,offset);ps.push(p)}tube(ps,.045,mats.ice)}
// Forest with white snow caps.
function tree(x,z,k){let y=height(x,z),g=new THREE.Group();g.position.set(x,y,z);scene.add(g);rod(V(0,0,0),V(0,k*2.7,0),k*.13,mats.wood,g);for(let j=0;j<3;j++){let o=mesh(new THREE.ConeGeometry(k*(1-j*.2),k*1.8,7),j===0?mats.navy:mats.snow,V(0,k*(1+j*.65),0),g)}return g}
for(let i=0;i<62;i++){let x=-33+rand()*65,z=-33+rand()*65;let p=path.getPoint(clamp((z+32)/59));if(Math.abs(x-p.x)>6&&!(x>10&&z>7))tree(x,z,.7+rand()*.6)}
// Ski lift: cable, support pylons, moving occupied chairs.
const liftA=V(28,height(28,25)+8,25),liftB=V(16,height(16,-29)+9,-29);
const cable=[];for(let i=0;i<=40;i++){let p=liftA.clone().lerp(liftB,i/40);p.y-=Math.sin(i/40*Math.PI)*2;cable.push(p)}tube(cable,.055,mats.dark);
for(let t of [.05,.43,.83]){let p=liftA.clone().lerp(liftB,t);let y=height(p.x,p.z);rod(V(p.x,y,p.z),p,.2,mats.wood);rod(p.clone().add(V(-2,0,0)),p.clone().add(V(2,0,0)),.14,mats.dark)}
const chairs=[];for(let i=0;i<8;i++){let g=new THREE.Group();scene.add(g);rod(V(0,0,0),V(0,-2,0),.06,mats.dark,g);box(2.2,.2,1,mats.blue,V(0,-2.6,0),g);box(2.2,.85,.12,mats.navy,V(0,-2.1,-.48),g);for(let x of [-.55,.55]){ball(.26,mats.snow,V(x,-1.5,0),g);box(.45,.65,.4,mats.blue,V(x,-2,0),g);rod(V(x,-2.4,.15),V(x,-3.3,.4),.1,mats.navy,g)}chairs.push(g)}
function skier(color=mats.blue){const g=new THREE.Group();for(let x of [-.22,.22]){const ski=box(.15,.09,2.4,mats.navy,V(x,.08,0),g);ski.rotation.y=x*.15;rod(V(x,.2,0),V(x,.9,-.25),.105,mats.dark,g);rod(V(x,.9,-.25),V(x*.5,1.55,0),.12,color,g)}let body=box(.65,.8,.45,color,V(0,1.55,0),g);body.rotation.x=-.22;ball(.29,mats.snow,V(0,2.16,-.17),g);box(.48,.14,.25,mats.glass,V(0,2.16,.04),g);for(let s of [-1,1]){rod(V(s*.32,1.8,0),V(s*.66,1.25,.3),.085,color,g);rod(V(s*.66,1.25,.3),V(s*.85,.1,-.7),.035,mats.dark,g)}scene.add(g);return g}
const hero=skier();const pupils=Array.from({length:5},(_,i)=>skier(i===0?mats.snow:mats.blue));
// Equipment transforms: physical pass, ski rental rig and instructor's gate.
const equip=new THREE.Group();scene.add(equip);equip.position.set(3,16,-3);
const ticket=new THREE.Group();equip.add(ticket);ticket.position.set(-3,2,0);ticket.rotation.y=-.2;box(3.7,5,.18,mats.blue,V(0,0,0),ticket);box(3.7,.8,.2,mats.navy,V(0,1.65,.03),ticket);let txt=label('FORFAIT',3.25,.75,'#0b2638');txt.position.set(0,1.65,.14);ticket.add(txt);txt=label('SKIM',2.9,.9,'#45bcf0','#072435');txt.position.set(0,.25,.14);ticket.add(txt);for(let i=0;i<14;i++)box(.06+rand()*.06,.7,.02,mats.navy,V(-1.35+i*.2,-1.4,.13),ticket);rod(V(-.8,2.5,0),V(-.8,4,0),.05,mats.light,ticket);rod(V(.8,2.5,0),V(-.8,4,0),.05,mats.light,ticket);
const skis=new THREE.Group();equip.add(skis);skis.position.set(2,0,0);skis.rotation.z=-.18;for(let s of [-1,1]){box(.5,7,.25,mats.navy,V(s*.6,0,0),skis);box(.51,2,.27,mats.blue,V(s*.6,1,0),skis);box(.55,.7,.5,mats.snow,V(s*.6,-.35,.2),skis);ball(.25,mats.blue,V(s*.6,3.5,0),skis)}
const school=new THREE.Group();scene.add(school);school.position.set(12,height(12,1),1);for(let x of [-2,2])rod(V(x,0,0),V(x,5,0),.07,mats.blue,school);let flag=label('ESCUELA',4.2,1.1);flag.position.set(0,4.1,0);school.add(flag);
// Alpine village. Architectural miniature, warm windows and visible terrace meals.
const village=new THREE.Group();scene.add(village);village.position.set(20,height(20,21)+.1,21);
function chalet(x,z,s){let g=new THREE.Group();village.add(g);g.position.set(x,0,z);g.scale.setScalar(s);box(7,4.5,5,mats.wood,V(0,2.25,0),g);box(7.3,.25,5.3,mats.snow,V(0,.2,0),g);let roof=mesh(new THREE.ConeGeometry(5.3,3.2,4),mats.navy,V(0,5.5,0),g);roof.rotation.y=Math.PI/4;roof.scale.z=.8;let cap=mesh(new THREE.ConeGeometry(5.4,2.4,4),mats.snow,V(0,6.05,0),g);cap.rotation.y=Math.PI/4;cap.scale.z=.8;for(let xx of [-2,0,2])for(let yy of [1.4,3.2])box(1.05,1,.06,mats.warm,V(xx,yy,2.54),g);box(1.15,2,.1,mats.navy,V(0,1,2.61),g);box(.65,2.6,.65,mats.wood,V(2,6,0),g);return g}
chalet(0,0,1);chalet(7,-5,.65);chalet(-7,-4,.65);let sign=label('REFUGIO',4.8,.8);sign.position.set(0,4,2.6);village.add(sign);
// Patio, tables, plates and cups (meals are objects, not bullet points).
box(13,.18,7,mats.wood,V(0,.1,6),village);for(let x of [-4,3.4]){rod(V(x,.2,6),V(x,1.3,6),.16,mats.dark,village);mesh(new THREE.CylinderGeometry(1.65,1.65,.18,24),mats.snow,V(x,1.4,6),village);for(let a of [0,Math.PI]){let xx=x+Math.cos(a)*.8,zz=6+Math.sin(a)*.8;mesh(new THREE.CylinderGeometry(.43,.43,.04,20),mats.glass,V(xx,1.53,zz),village);ball(.25,mats.warm,V(xx,1.64,zz),village);mesh(new THREE.CylinderGeometry(.13,.13,.32,12),mats.navy,V(xx,1.65,zz+.5),village)}for(let j=0;j<3;j++){let a=j/3*Math.PI*2;box(.7,.2,.7,mats.blue,V(x+Math.cos(a)*2,.7,6+Math.sin(a)*2),village)}}
// Group coach arrives at the connected base.
const bus=new THREE.Group();village.add(bus);box(7,2.3,2.3,mats.snow,V(0,1.55,0),bus);box(7,.65,2.35,mats.blue,V(0,.75,0),bus);box(6.4,.9,2.36,mats.glass,V(0,1.95,0),bus);for(let x of [-2.3,2.3])for(let z of [-1.2,1.2]){const w=mesh(new THREE.CylinderGeometry(.5,.5,.18,16),mats.navy,V(x,.5,z),bus);w.rotation.x=Math.PI/2}let blogo=label('SKIM',2.6,.7,'#effaff','#0b2638');blogo.position.set(0,1.06,1.22);bus.add(blogo);
for(let i=0;i<7;i++){for(let side of [-1,1]){ball(.18,mats.navy,V(-2.6+i*.85,2.02,side*1.2),bus);box(.3,.3,.04,mats.navy,V(-2.6+i*.85,1.78,side*1.21),bus);}}
// Coordination hub: animated route links and protective insurance shield.
const hub=new THREE.Group();village.add(hub);hub.position.set(9,0,7);rod(V(0,0,0),V(0,6,0),.12,mats.navy,hub);const hubSign=label('SKIM',3,1);hubSign.position.set(0,5.6,0);hub.add(hubSign);const rings=[];for(let i=0;i<3;i++){let r=mesh(new THREE.TorusGeometry(1.5,.035,6,64),mats.light,V(0,.3+i*.1,0),hub);r.rotation.x=Math.PI/2;rings.push(r)}
const shield=new THREE.Group();village.add(shield);shield.position.set(-8,5,5);const shape=new THREE.Shape();shape.moveTo(0,1.8);shape.lineTo(1.5,1.2);shape.lineTo(1.3,-.6);shape.quadraticCurveTo(.8,-1.5,0,-2);shape.quadraticCurveTo(-.8,-1.5,-1.3,-.6);shape.lineTo(-1.5,1.2);shape.closePath();mesh(new THREE.ExtrudeGeometry(shape,{depth:.2,bevelEnabled:true,bevelSize:.12,bevelThickness:.1,bevelSegments:2,steps:1}),mats.blue,V(0,0,0),shield);box(.35,1.5,.15,mats.snow,V(0,0,.4),shield);box(1.5,.35,.15,mats.snow,V(0,0,.4),shield);
let route=[];for(let [x,z] of [[9,7],[7,4],[3,6],[-4,6],[-8,5]])route.push(V(x,.35,z));tube(route,.045,mats.light,village);
const groupSkiers=[];for(let i=0;i<7;i++){let g=skier(i%3===0?mats.snow:mats.blue);g.scale.setScalar(.7);groupSkiers.push(g)}
// Intro name written as twin ski lines in world space, using vector glyphs.
const glyphs={S:[[[1,1],[0,1],[0,.5],[1,.5],[1,0],[0,0]]],K:[[[0,0],[0,1]],[[1,1],[0,.5],[1,0]]],I:[[[0,1],[1,1]],[[.5,1],[.5,0]],[[0,0],[1,0]]],M:[[[0,0],[0,1],[.5,.45],[1,1],[1,0]]]};
const trackLetters=new THREE.Group();scene.add(trackLetters);trackLetters.position.set(-5,22,-24);trackLetters.rotation.x=-Math.PI/2;let letterLines=[];for(let j=0;j<4;j++)for(let stroke of glyphs['SKIM'[j]]){let pts=stroke.map(([x,y])=>V(j*3.2+x*2.5,y*4,0));for(let off of [-.08,.08]){let o=tube(pts.map(p=>p.clone().add(V(0,off,0))),.055,mats.blue,trackLetters);letterLines.push(o)}}
// Fine airborne snow; deterministic positions, time-driven drift.
let snowGeo=new THREE.BufferGeometry(),snowPos=new Float32Array(650*3),snowBase=[];for(let i=0;i<650;i++){snowBase.push([rand()*150-75,rand()*65,rand()*130-65]);}snowGeo.setAttribute('position',new THREE.BufferAttribute(snowPos,3));const snow=new THREE.Points(snowGeo,new THREE.PointsMaterial({color:'#d6f5ff',size:.105,transparent:true,opacity:.65,depthWrite:false}));scene.add(snow);
// Seekable choreography. Four views share the same constructed world.
const views=spec.camera;
let titleTimeline=gsap.timeline({paused:true});titleTimeline.to('#progress i',{width:1712,duration:15,ease:'none'},0);
function title(id,start,end,t){const el=document.getElementById(id),enter=smooth((t-start)/.48),leave=end===15?1:1-smooth((t-(end-.28))/.28);el.style.opacity=enter*leave;el.style.transform=`translate3d(${(1-enter)*-30}px,${(1-enter)*30}px,0) scale(${.975+.025*enter})`;}
window.seek=async function(t){t=clamp(t,0,15);titleTimeline.seek(t,false);spec.scenes.forEach((s,i)=>title('c'+(i+1),s.start,s.end,t));document.querySelector('#brand').style.opacity=t>11?1-smooth((t-11)/.4):1;let chapter=t<3?0:t<7?1:t<11?2:3;document.querySelector('#chapter').textContent=['01 / LA MONTAÑA NOS UNE','02 / ENCUENTRA TU RITMO','03 / UN GRUPO. TODO CONECTADO.','SKIM INCOMING / LA MOLINA'][chapter];
let i=0;while(i<views.length-2&&t>views[i+1].t)i++;let a=views[i],b=views[i+1],u=smooth((t-a.t)/(b.t-a.t));camera.position.fromArray(a.p.map((v,k)=>mix(v,b.p[k],u)));let target=V(...a.q.map((v,k)=>mix(v,b.q[k],u)));
// Horizontal composition: subject is intentionally on the right behind left typography.
camera.lookAt(target);camera.setViewOffset(1920,1080,-310,0,1920,1080);camera.fov=mix(a.f,b.f,u);camera.updateProjectionMatrix();
for(let j=0;j<chairs.length;j++){let u=(j/chairs.length+t*.035)%1,p=liftA.clone().lerp(liftB,u);p.y-=Math.sin(u*Math.PI)*2;chairs[j].position.copy(p);chairs[j].rotation.y=.15*Math.sin(t+j)}
let hu=clamp(.05+(t-2.5)*.13,.02,.98),hp=onPath(hu);hero.position.copy(hp);let tangent=path.getTangent(hu);hero.rotation.y=Math.atan2(tangent.x,tangent.z);hero.rotation.z=.14*Math.sin(t*3);hero.scale.setScalar(t<7?1.65:1);for(let j=0;j<pupils.length;j++){let p=onPath(.50+j*.045,j%2?2:-1.5);pupils[j].position.copy(p);pupils[j].scale.setScalar(.65);pupils[j].rotation.y=.3;}
let ee=smooth((t-4.0)/.65)*(1-smooth((t-6.5)/.5));equip.scale.setScalar(Math.max(.001,ee));equip.rotation.y=-.25+Math.sin(t*1.1)*.12;ticket.rotation.z=.08*Math.sin(t*2);school.scale.setScalar(.75+.1*Math.sin(t));
let ve=smooth((t-6.7)/.8);village.scale.setScalar(.65+.35*ve);bus.position.set(-5+smooth((t-7)/1.8)*5,.2,12);bus.rotation.y=-.14;shield.rotation.y=Math.sin(t*1.4)*.25;shield.position.y=5+Math.sin(t*2)*.2;for(let j=0;j<rings.length;j++){let s=1+((t*.65+j*.33)%1)*1.7;rings[j].scale.setScalar(s)}
for(let j=0;j<groupSkiers.length;j++){groupSkiers[j].position.set(23+j*.85,height(23+j*.85,35)+.15,35+(j%2)*1.4-smooth((t-8)/2)*2);groupSkiers[j].rotation.y=-.4+Math.sin(t+j)*.1;}
for(let j=0;j<letterLines.length;j++){let s=smooth((t-.25-j*.045)/.45);letterLines[j].scale.set(s,1,1);letterLines[j].visible=false;}
for(let j=0;j<650;j++){const p=snowBase[j];snowPos[j*3]=p[0]+Math.sin(t*.3+j)*.4;snowPos[j*3+1]=((p[1]-t*1.6)%65+65)%65;snowPos[j*3+2]=p[2]+t*.3;}snowGeo.attributes.position.needsUpdate=true;
// Subtle white flare on the musical transition, never over the held final CTA.
let flare=0;for(let beat of [3,7,11])flare=Math.max(flare,.13*Math.exp(-(((t-beat)/.065)**2)));document.querySelector('#flash').style.opacity=flare;
let trackProgress=smooth((t-.25)/1.55);for(let line of document.querySelectorAll('.ski-trace')){let len=document.querySelector('#tracks').getTotalLength();line.style.strokeDasharray=len;line.style.strokeDashoffset=len*(1-trackProgress)}document.querySelector('#ski-name').style.opacity=smooth(t/.2)*(1-smooth((t-2.65)/.35));
renderer.render(scene,camera);return true;};
await document.fonts.ready;await window.seek(0);window.READY=true;
