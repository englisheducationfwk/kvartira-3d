# -*- coding: utf-8 -*-
"""O3: дом на 12-м этаже — за окнами и лоджией открывается вид с высоты:
двор и шоссе далеко внизу (земля на −33 м), корпус дома уходит вниз до земли,
вдали — город. Задник перерисован под взгляд с 12-го этажа."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')

OLD_TEX = """var texOutside = ctex(1024,512,function(g,w,h){
  var R = rng(13);
  var grd=g.createLinearGradient(0,0,0,h);
  grd.addColorStop(0,'#bcd6ea'); grd.addColorStop(.45,'#dcebf0'); grd.addColorStop(.62,'#e2e9dc'); grd.addColorStop(1,'#a9bd9a');
  g.fillStyle=grd; g.fillRect(0,0,w,h);
  g.fillStyle='rgba(255,255,255,.55)';
  for (var i=0;i<14;i++){ g.beginPath(); g.ellipse(R()*w, h*0.06+R()*h*0.3, 50+R()*110, 12+R()*22, 0, 0, 6.3); g.fill(); }
  for (var i=0;i<22;i++){ var bh=(0.10+R()*0.22)*h, bw=40+R()*90, x=R()*w, y=h*0.60-bh;
    g.fillStyle='rgba(150,162,168,'+(0.35+R()*0.4).toFixed(2)+')'; g.fillRect(x,y,bw,bh);
    g.fillStyle='rgba(255,255,255,.16)';
    for (var wy=y+6; wy<y+bh-4; wy+=10) g.fillRect(x+4, wy, bw-8, 3);
  }
  for (var i=0;i<26;i++){ g.fillStyle='rgba(104,130,88,'+(0.3+R()*0.4).toFixed(2)+')';
    g.beginPath(); g.arc(R()*w, h*0.66+R()*h*0.3, 20+R()*46, 0, 6.3); g.fill(); }
  g.fillStyle='rgba(120,120,118,.5)'; g.fillRect(0,h*0.86,w,h*0.14);
});"""

NEW_TEX = """/* вид с 12-го этажа: небо, город у горизонта, ниже — двор со высоты птичьего полёта */
var texOutside = ctex(1024,512,function(g,w,h){
  var R = rng(13);
  var HZ = h*0.53;                       /* линия горизонта — примерно на уровне глаз */
  var grd=g.createLinearGradient(0,0,0,HZ);
  grd.addColorStop(0,'#a9cdec'); grd.addColorStop(.6,'#cfe4f0'); grd.addColorStop(1,'#e8efe0');
  g.fillStyle=grd; g.fillRect(0,0,w,HZ);
  g.fillStyle='rgba(255,255,255,.6)';
  for (var i=0;i<12;i++){ g.beginPath(); g.ellipse(R()*w, h*0.05+R()*h*0.22, 60+R()*120, 11+R()*20, 0, 0, 6.3); g.fill(); }
  /* дальний город — крыши чуть ниже горизонта (смотрим с высоты) */
  for (var i=0;i<26;i++){ var bh=(0.08+R()*0.13)*h, bw=36+R()*80, x=R()*w, y=HZ-bh*0.25;
    g.fillStyle='rgba(158,170,178,'+(0.45+R()*0.35).toFixed(2)+')'; g.fillRect(x,y,bw,bh);
    g.fillStyle='rgba(255,255,255,.14)';
    for (var wy=y+5; wy<y+bh-3; wy+=8) g.fillRect(x+3, wy, bw-6, 2.4);
  }
  /* ниже горизонта — двор сверху: газон, дорожки */
  g.fillStyle='#b7c8a8'; g.fillRect(0,HZ,w,h-HZ);
  g.fillStyle='rgba(216,216,208,.9)';
  g.fillRect(w*0.06, HZ+h*0.02, w*0.09, h); g.fillRect(w*0.55, HZ-h*0.01, w*0.06, h);
  g.fillRect(0, HZ+h*0.06, w, h*0.025);
  /* шоссе внизу с разметкой и машинами */
  (function(){
    var ry = HZ + h*0.20, rh = h*0.13;
    g.fillStyle='#8e8f8c'; g.fillRect(0, ry, w, rh);
    g.fillStyle='#a9aaa6'; g.fillRect(0, ry, w, 3); g.fillRect(0, ry+rh-3, w, 3);
    g.fillStyle='rgba(255,244,190,.95)';
    for (var x=10; x<w; x+=64) g.fillRect(x, ry+rh/2-2, 30, 4);
    for (var c=0;c<14;c++){
      var cx2=R()*w, cy2=ry+6+R()*(rh-20), cw2=18+R()*22;
      g.fillStyle=['#d9534f','#4a7fb5','#e8e5dc','#3d4148','#7fb069'][Math.floor(R()*5)];
      g.fillRect(cx2, cy2, cw2, 10);
    }
  })();
  /* кроны деревьев сверху — с тенью */
  for (var i=0;i<30;i++){
    var tx=R()*w, ty=HZ+8+R()*(h-HZ-14), tr=14+R()*30;
    g.fillStyle='rgba(90,110,80,.32)'; g.beginPath(); g.arc(tx+4, ty+5, tr, 0, 6.3); g.fill();
    g.fillStyle='rgba(104,138,88,'+(0.55+R()*0.35).toFixed(2)+')'; g.beginPath(); g.arc(tx, ty, tr, 0, 6.3); g.fill();
  }
});
/* земля далеко внизу (12-й этаж): двор, парковки, шоссе — если смотреть вниз */
var texYard = ctex(1024,1024,function(g,w,h){
  var R = rng(77);
  g.fillStyle='#b7c8a8'; g.fillRect(0,0,w,h);
  g.fillStyle='#c3d1b2';
  for (var i=0;i<40;i++){ g.beginPath(); g.arc(R()*w, R()*h, 30+R()*90, 0, 6.3); g.fill(); }
  g.fillStyle='rgba(216,216,208,.92)';   /* дорожки и проезды */
  g.fillRect(w*0.18, 0, 34, h); g.fillRect(0, h*0.34, w, 30);
  g.fillRect(w*0.62, h*0.34, 30, h*0.66);
  /* парковка с машинами */
  g.fillStyle='#9a9b98'; g.fillRect(w*0.19, h*0.52, w*0.40, h*0.16);
  for (var px=w*0.20; px<w*0.57; px+=46){
    g.fillStyle=['#d9534f','#4a7fb5','#e8e5dc','#3d4148','#7fb069','#c9c3b8'][Math.floor(R()*6)];
    g.fillRect(px, h*0.54, 34, 20);
  }
  /* шоссе через низ — 4 полосы, разметка, машины */
  var ry = h*0.80, rh = h*0.13;
  g.fillStyle='#87888a'; g.fillRect(0, ry, w, rh);
  g.fillStyle='#9a9b9d'; g.fillRect(0, ry, w, 5); g.fillRect(0, ry+rh-5, w, 5);
  g.fillStyle='rgba(238,238,232,.9)'; g.fillRect(0, ry+rh*0.24-1.5, w, 3); g.fillRect(0, ry+rh*0.76-1.5, w, 3);
  g.fillStyle='rgba(255,244,190,.95)';
  for (var x=14; x<w; x+=80) g.fillRect(x, ry+rh/2-3, 40, 6);
  for (var c=0;c<22;c++){
    var cxp=R()*w, lane=[ry+8, ry+rh*0.42, ry+rh*0.58, ry+rh-24][c%4], cw2=30+R()*26;
    g.fillStyle=['#d9534f','#4a7fb5','#e8e5dc','#3d4148','#7fb069','#211f1e'][Math.floor(R()*6)];
    g.fillRect(cxp, lane, cw2, 14);
  }
  /* деревья с тенями */
  for (var t=0;t<70;t++){
    var tx=R()*w, ty=R()*h; if (ty>ry-20 && ty<ry+rh+20) continue;
    var tr=12+R()*26;
    g.fillStyle='rgba(90,110,80,.30)'; g.beginPath(); g.arc(tx+4, ty+5, tr, 0, 6.3); g.fill();
    g.fillStyle='rgba(100,134,84,'+(0.5+R()*0.4).toFixed(2)+')'; g.beginPath(); g.arc(tx, ty, tr, 0, 6.3); g.fill();
  }
  /* детская площадка */
  g.fillStyle='#d8b56a'; g.fillRect(w*0.42, h*0.60, w*0.14, h*0.10);
  g.fillStyle='#b45b4a'; g.fillRect(w*0.44, h*0.62, 40, 40); g.fillRect(w*0.49, h*0.64, 60, 24);
});
/* стена панельного дома — уходит вниз от нашей квартиры до земли */
var texTower = ctex(256, 256, function(g,w,h){
  g.fillStyle='#cfc8b8'; g.fillRect(0,0,w,h);
  g.strokeStyle='rgba(120,112,96,.55)'; g.lineWidth=3;
  g.strokeRect(0,0,w,h);
  g.beginPath(); g.moveTo(0,h/2); g.lineTo(w,h/2); g.stroke();
  g.beginPath(); g.moveTo(w/2,0); g.lineTo(w/2,h); g.stroke();
  for (var r2=0;r2<2;r2++) for (var c2=0;c2<2;c2++){
    var wx=c2*w/2, wy=r2*h/2;
    g.fillStyle='#77808a'; g.fillRect(wx+w*0.14, wy+h*0.10, w*0.28, h*0.26);
    g.strokeStyle='rgba(255,255,255,.5)'; g.lineWidth=2;
    g.strokeRect(wx+w*0.14, wy+h*0.10, w*0.28, h*0.26);
    g.beginPath(); g.moveTo(wx+w*0.28, wy+h*0.10); g.lineTo(wx+w*0.28, wy+h*0.36); g.stroke();
  }
});"""

assert OLD_TEX in s, 'texOutside not found'
assert s.count(OLD_TEX) == 1
s = s.replace(OLD_TEX, NEW_TEX, 1)

OLD_PLANE = """  /* ---------- мир за фасадом ---------- */
  var outP = new THREE.Mesh(new THREE.PlaneGeometry(18, 10), M.outside);
  outP.position.set(3.2, 2.8, -5.4); gRoom.add(outP);"""
NEW_PLANE = """  /* ---------- мир за фасадом: вид с 12-го этажа ---------- */
  var outP = new THREE.Mesh(new THREE.PlaneGeometry(34, 14), M.outside);
  outP.position.set(mx(3.2), 3.4, -7.6); gRoom.add(outP);
  /* земля далеко внизу: 12 этажей ≈ 33 м */
  var GROUND_Y = -33.4;
  var yard = new THREE.Mesh(new THREE.PlaneGeometry(220, 220),
    new THREE.MeshBasicMaterial({ map: texYard }));
  yard.rotation.x = -Math.PI/2;
  yard.position.set(mx(3.2), GROUND_Y, 4.0); gRoom.add(yard);
  /* корпус дома под квартирой — из окна вниз виден свой дом до земли */
  var towerMat = new THREE.MeshStandardMaterial({ map: texTower, roughness: .9 });
  towerMat.map.wrapS = towerMat.map.wrapT = THREE.RepeatWrapping;
  towerMat.map.repeat.set(3, 9);
  var tower = new THREE.Mesh(new THREE.BoxGeometry(9.9, 33.3, 14.2), towerMat);
  tower.position.set(mx(3.16), GROUND_Y + 33.3/2, 4.90);
  tower.receiveShadow = true; gRoom.add(tower);
  /* соседние дома вокруг — стоят на земле */
  [ [-26, 30, 15, 36], [33, 42, 13, 30], [-4, 40, 17, 33], [55, 12, 14, 27] ].forEach(function(bd){
    var nb = new THREE.Mesh(new THREE.BoxGeometry(bd[2], bd[3], bd[2]*0.9), towerMat.clone());
    nb.material.map = towerMat.map.clone();
    nb.material.map.needsUpdate = true; nb.material.map.wrapS = nb.material.map.wrapT = THREE.RepeatWrapping;
    nb.material.map.repeat.set(3, bd[3]/3.6);
    nb.position.set(mx(bd[0]), GROUND_Y + bd[3]/2, bd[1]);
    nb.receiveShadow = true; gRoom.add(nb);
  });"""
assert OLD_PLANE in s, 'outP not found'
assert s.count(OLD_PLANE) == 1
s = s.replace(OLD_PLANE, NEW_PLANE, 1)

p.write_text(s, encoding='utf-8')
print('O3 ok')
