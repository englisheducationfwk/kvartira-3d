"""G1: планировка — комната +50см влево и +80см вниз, мини-коридор у входа,
входная дверь и площадка перестроены, дверь балкона шире, мерцания (эркер балкона,
кухонный угол) убраны."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:120]
    s = s.replace(old, new, count)


# --- план
rep("  room:  { x0:0.00, x1:3.41, z0:0.00, z1:5.52 },",
    "  room:  { x0:-0.50, x1:3.41, z0:0.00, z1:6.32 },")
rep("  hall:  { x0:3.57, x1:4.45, z0:3.16, z1:5.52 },",
    "  hall:  { x0:3.57, x1:4.45, z0:3.16, z1:6.32 },")
rep("  balcony: { doorX0:0.35, doorX1:1.07, winX0:1.15, winX1:3.15, sill:0.85, winTop:2.30, h:2.10 }",
    "  balcony: { doorX0:0.35, doorX1:1.13, winX0:1.15, winX1:3.15, sill:0.85, winTop:2.30, h:2.10 }")
rep("var LAND = { x0:2.4, x1:6.9, z0:5.68, z1:7.6 };",
    "var LAND = { x0:2.4, x1:6.9, z0:5.68, z1:7.9 };")
rep("var MXSUM = 6.32;               /* зеркало: x' = MXSUM - x  */",
    "var MXSUM = 5.97;               /* зеркало: x' = MXSUM - x  */")
rep("var FLAT = { x0:-0.95, x1:7.27, z0:-1.60, z1:7.80 };",
    "var FLAT = { x0:-0.95, x1:7.27, z0:-1.60, z1:8.10 };")
rep("var LS = 'flat44k.v3';", "var LS = 'flat44k.v4';")

# --- стена комнаты на запад (x=-0.50) и юг (z=6.32)
rep("""  solidBox(-P.LOAD-0.001, 0.001, -0.30, 5.52+P.LOAD, 0, P.HC, { px:M.wall2, nx:M.concrete });
  seg(-0.08, -0.30, -0.08, 5.68, P.LOAD/2);""",
    """  solidBox(P.room.x0-P.LOAD, P.room.x0, -0.30, P.room.z1+P.LOAD, 0, P.HC, { px:M.wall2, nx:M.concrete });
  seg(P.room.x0-P.LOAD/2, -0.30, P.room.x0-P.LOAD/2, P.room.z1+0.16, P.LOAD/2);""")

# --- фасад комнаты: левая стойка до новой стены; стык с кухней больше не пересекается (мерцало)
rep("  cullList.push(solidBox(-0.16, RB.doorX0, FZ-FTH/2, FZ+FTH/2, 0, P.HC, { pz:M.wall2, nz:M.facade2 }));",
    "  cullList.push(solidBox(P.room.x0-0.16, RB.doorX0, FZ-FTH/2, FZ+FTH/2, 0, P.HC, { pz:M.wall2, nz:M.facade2 }));")
rep("  cullList.push(solidBox(RB.winX1, K.x0+0.08, FZ-FTH/2, FZ+FTH/2, 0, P.HC, { pz:M.wall2, nz:M.facade2 }));",
    "  cullList.push(solidBox(RB.winX1, K.x0, FZ-FTH/2, FZ+FTH/2, 0, P.HC, { pz:M.wall2, nz:M.facade2 }));")
rep("  cullList.push(solidBox(BAY.p3[0], K.x1+0.08, FZ-FTH/2, FZ+FTH/2, 0, P.HC, { pz:null, staged:['pz'], nz:M.facade2 }));",
    "  cullList.push(solidBox(BAY.p3[0], K.x1+P.LOAD, FZ-FTH/2, FZ+FTH/2, 0, P.HC, { pz:null, staged:['pz'], nz:M.facade2 }));")

# --- южная стена: квартира тянется на юг (входная дальше), санузел остаётся
rep("""  solidBox(-0.30, DH.ent.x0, P.room.z1, P.room.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });
  solidBox(DH.ent.x0, DH.ent.x1, P.room.z1, P.room.z1+P.LOAD, DH.ent.h, P.HC, { pz:M.hallWall, nz:M.wall2 });
  solidBox(DH.ent.x1, BA.x0, P.room.z1, P.room.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });
  solidBox(BA.x0, BA.x1+P.LOAD, P.room.z1, P.room.z1+P.LOAD, 0, 2.10, { pz:M.hallWall, nz:M.tile2 });
  solidBox(BA.x0, BA.x1+P.LOAD, P.room.z1, P.room.z1+P.LOAD, 2.10, P.HC, { pz:M.hallWall, nz:M.wall2 });
  seg(-0.30, P.room.z1+P.LOAD/2, DH.ent.x0, P.room.z1+P.LOAD/2, P.LOAD/2);
  seg(DH.ent.x1, P.room.z1+P.LOAD/2, BA.x1+P.LOAD, P.room.z1+P.LOAD/2, P.LOAD/2);""",
    """  solidBox(P.room.x0, DH.ent.x0, P.room.z1, P.room.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });
  solidBox(DH.ent.x0, DH.ent.x1, P.room.z1, P.room.z1+P.LOAD, DH.ent.h, P.HC, { pz:M.hallWall, nz:M.wall2 });
  solidBox(DH.ent.x1, BA.x0, P.room.z1, P.room.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });
  /* южная стена санузла осталась на месте — за ней ниша площадки */
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 0, 2.10, { pz:M.hallWall, nz:M.tile2 });
  solidBox(BA.x0, BA.x1+P.LOAD, BA.z1, BA.z1+P.LOAD, 2.10, P.HC, { pz:M.hallWall, nz:M.wall2 });
  seg(P.room.x0, P.room.z1+P.LOAD/2, DH.ent.x0, P.room.z1+P.LOAD/2, P.LOAD/2);
  seg(DH.ent.x1, P.room.z1+P.LOAD/2, BA.x0, P.room.z1+P.LOAD/2, P.LOAD/2);
  seg(BA.x0, BA.z1+P.LOAD/2, BA.x1+P.LOAD, BA.z1+P.LOAD/2, P.LOAD/2);""")

# --- перегородка коридор/санузел: тянется до входной, фантомный сег 5.01 поправлен
rep("""  solidBox(HA.x1, BA.x0, DH.bath.z1, P.room.z1+P.LOAD, 0, 2.10, { px:M.tile2, nx:M.wall2 });
  solidBox(HA.x1, BA.x0, DH.bath.z1, P.room.z1+P.LOAD, 2.10, P.HC, { px:M.wall2, nx:M.wall2 });
  seg(5.01, K.z1+P.LOAD, 5.01, DH.bath.z0, P.PART/2);
  seg(5.01, DH.bath.z1, 5.01, P.room.z1+0.16, P.PART/2);""",
    """  solidBox(HA.x1, BA.x0, DH.bath.z1, HA.z1, 0, 2.10, { px:M.tile2, nx:M.wall2 });
  solidBox(HA.x1, BA.x0, DH.bath.z1, HA.z1, 2.10, P.HC, { px:M.wall2, nx:M.wall2 });
  /* продолжение перегородки: торцы мини-коридора и ниши площадки */
  solidBox(HA.x1, BA.x0, HA.z1, HA.z1+P.LOAD, 0, P.HC, { px:M.hallWall, nx:M.hallWall });
  seg((HA.x1+BA.x0)/2, K.z1+P.LOAD, (HA.x1+BA.x0)/2, DH.bath.z0, P.PART/2);
  seg((HA.x1+BA.x0)/2, DH.bath.z1, (HA.x1+BA.x0)/2, HA.z1+0.16, P.PART/2);""")

# --- мерцание балкона: крыша лоджии больше не совпадает с её потолком; торцы балок прячутся в стену
rep("    roof.position.set(mx((LG.x0+LG.x1)/2), 2.48, (LG.z0+LG.z1)/2); roof.castShadow = true; gRoom.add(roof);",
    "    roof.position.set(mx((LG.x0+LG.x1)/2), 2.505, (LG.z0+LG.z1)/2); roof.castShadow = true; gRoom.add(roof);")
rep("    solidBeam([LG.x0,LG.z0],[LG.x0,LG.z1], 0.14, 0, 1.0, M.concrete, M.concrete, 1);",
    "    solidBeam([LG.x0,LG.z0],[LG.x0,LG.z1-0.02], 0.14, 0, 1.0, M.concrete, M.concrete, 1);")
rep("    solidBeam([LG.x1,LG.z0],[LG.x1,LG.z1], 0.14, 0, 1.0, M.concrete, M.concrete, 1);",
    "    solidBeam([LG.x1,LG.z0],[LG.x1,LG.z1-0.02], 0.14, 0, 1.0, M.concrete, M.concrete, 1);")

# --- площадка: перестроена под новую входную (пол/потолок двумя плитами, стены)
rep("""    var fl = new THREE.Mesh(new THREE.BoxGeometry(L1-L0, 0.08, LAND.z1-LAND.z0), M.concrete);
    fixBoxUV(fl.geometry, L1-L0, 0.08, LAND.z1-LAND.z0, 1);
    fl.position.set((L0+L1)/2, -0.046, (LAND.z0+LAND.z1)/2); fl.receiveShadow = true; g.add(fl);
    var ce = new THREE.Mesh(new THREE.PlaneGeometry(L1-L0, LAND.z1-LAND.z0), M.ceil);
    ce.rotation.x = Math.PI/2; ce.position.set((L0+L1)/2, 2.72, (LAND.z0+LAND.z1)/2); g.add(ce);""",
    """    var WZ = HA.z1 + P.LOAD;                       /* южная плоскость входной стены */
    var BW = Math.min(mx(BA.x0), mx(BA.x1));       /* восточная плита начинается у санузла */
    function slab(x0, x1, z0, z1){
      var m = new THREE.Mesh(new THREE.BoxGeometry(x1-x0, 0.08, z1-z0), M.concrete);
      fixBoxUV(m.geometry, x1-x0, 0.08, z1-z0, 1);
      m.position.set((x0+x1)/2, -0.046, (z0+z1)/2); m.receiveShadow = true; g.add(m); return m;
    }
    slab(L0, BW, WZ, LAND.z1);
    slab(BW, L1, LAND.z0, LAND.z1);
    function clg(x0, x1, z0, z1){
      var m = new THREE.Mesh(new THREE.PlaneGeometry(x1-x0, z1-z0), M.ceil);
      m.rotation.x = Math.PI/2; m.position.set((x0+x1)/2, 2.72, (z0+z1)/2); g.add(m); return m;
    }
    clg(L0, BW, WZ, LAND.z1);
    clg(BW, L1, LAND.z0, LAND.z1);""")
rep("""    w(L0-0.12, L0, (LAND.z0+LAND.z1)/2, 0.12);
    w(L1, L1+0.12, (LAND.z0+LAND.z1)/2, 0.12);
    w(L0, L1, LAND.z1, 0.12);
    w(L0-0.12, E0, LAND.z0, 0.12);
    w(E1, L1+0.12, LAND.z0, 0.12);
    w(E0, E1, LAND.z0, 0.12, 2.10, 2.72);
    seg(LAND.x0, LAND.z0, DH.ent.x0, LAND.z0, 0.07);
    seg(DH.ent.x1, LAND.z0, LAND.x1, LAND.z0, 0.07);
    seg(LAND.x0, LAND.z0, LAND.x0, LAND.z1, 0.08);
    seg(LAND.x1, LAND.z0, LAND.x1, LAND.z1, 0.08);
    seg(LAND.x0, LAND.z1, LAND.x1, LAND.z1, 0.08);""",
    """    w(L0-0.12, L0, (WZ+LAND.z1)/2, 0.12);
    w(L1, L1+0.12, (LAND.z0+LAND.z1)/2, 0.12);
    w(L0, L1, LAND.z1, 0.12);
    /* север: входная стена квартиры (E0..E1 — дверь) и стена санузла за нишей */
    w(L0-0.12, E0, WZ, 0.12);
    w(E1, BW, WZ, 0.12);
    w(E0, E1, WZ, 0.12, 2.10, 2.72);
    w(BW, L1+0.12, LAND.z0, 0.12);
    seg(BW, LAND.z0, LAND.x1, LAND.z0, 0.07);
    seg(LAND.x0, WZ, LAND.x0, LAND.z1, 0.08);
    seg(LAND.x1, LAND.z0, LAND.x1, LAND.z1, 0.08);
    seg(LAND.x0, LAND.z1, LAND.x1, LAND.z1, 0.08);""")
rep("""    var vr1 = new THREE.Mesh(new THREE.BoxGeometry(0.09, 2.72, vest), M.hallWall);
    vr1.position.set(E0-0.045, 1.36, LAND.z0+vest/2); vr1.receiveShadow = true; g.add(vr1);
    var vr2 = vr1.clone(); vr2.position.x = E1+0.045; g.add(vr2);
    var vr3 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0+0.18, 0.62, vest), M.hallWall);
    vr3.position.set((E0+E1)/2, 2.41, LAND.z0+vest/2); vr3.receiveShadow = true; g.add(vr3);
    var th1 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0, 0.02, vest), M.concrete);
    th1.position.set((E0+E1)/2, 0.01, LAND.z0+vest/2); g.add(th1);
    /* полки ниш: справа от двери и напротив (обувница/зеркало) */
    var nsh1 = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.03, 0.26), M.wood);
    nsh1.position.set(E0-0.045, 1.15, LAND.z0+0.17); g.add(nsh1);
    var nsh2 = nsh1.clone(); nsh2.position.x = E1+0.045; g.add(nsh2);""",
    """    var vr1 = new THREE.Mesh(new THREE.BoxGeometry(0.09, 2.72, vest), M.hallWall);
    vr1.position.set(E0-0.045, 1.36, WZ+vest/2); vr1.receiveShadow = true; g.add(vr1);
    var vr2 = vr1.clone(); vr2.position.x = E1+0.045; g.add(vr2);
    var vr3 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0+0.18, 0.62, vest), M.hallWall);
    vr3.position.set((E0+E1)/2, 2.41, WZ+vest/2); vr3.receiveShadow = true; g.add(vr3);
    var th1 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0, 0.02, vest), M.concrete);
    th1.position.set((E0+E1)/2, 0.01, WZ+vest/2); g.add(th1);
    var nsh1 = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.03, 0.26), M.wood);
    nsh1.position.set(E0-0.045, 1.15, WZ+0.17); g.add(nsh1);
    var nsh2 = nsh1.clone(); nsh2.position.x = E1+0.045; g.add(nsh2);""")
rep("""    j1.position.set(E0-0.09, 1.07, LAND.z0); g.add(j1);
    var j2 = j1.clone(); j2.position.x = E1+0.02; g.add(j2);
    var j3 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0+0.14, 0.07, 0.12), M.frame);
    j3.position.set((E0+E1)/2, 2.14, LAND.z0); g.add(j3);
    var plate = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.09, 0.02), M.white);
    plate.position.set(E1+0.16, 1.55, LAND.z0-0.07); g.add(plate);""",
    """    j1.position.set(E0-0.09, 1.07, WZ); g.add(j1);
    var j2 = j1.clone(); j2.position.x = E1+0.02; g.add(j2);
    var j3 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0+0.14, 0.07, 0.12), M.frame);
    j3.position.set((E0+E1)/2, 2.14, WZ); g.add(j3);
    var plate = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.09, 0.02), M.white);
    plate.position.set(E1+0.16, 1.55, HA.z1-0.07); g.add(plate);""")

# --- балконная дверь шире (как все двери)
rep("    balc: mkDoor(RB.doorX0, 0, 0.70, [1,0], [0,1]),",
    "    balc: mkDoor(RB.doorX0, 0, 0.78, [1,0], [0,1]),")

# --- плинтусы под новые стены
rep("""  pl(0.01, 0.01, RB.doorX0, 0.01); pl(RB.doorX1, 0.01, RB.winX0, 0.01); pl(RB.winX1, 0.01, 3.40, 0.01);
  plZ(0.01, 0.01, 5.51);
  plZ(3.40, 0.01, DH.room.z0); plZ(3.40, DH.room.z1, 5.51);
  pl(0.01, 5.51, DH.ent.x0, 5.51);""",
    """  pl(P.room.x0+0.01, 0.01, RB.doorX0, 0.01); pl(RB.doorX1, 0.01, RB.winX0, 0.01); pl(RB.winX1, 0.01, 3.40, 0.01);
  plZ(P.room.x0+0.01, 0.01, P.room.z1-0.01);
  plZ(3.40, 0.01, DH.room.z0); plZ(3.40, DH.room.z1, P.room.z1-0.01);
  pl(P.room.x0+0.01, P.room.z1-0.01, DH.ent.x0, P.room.z1-0.01);""")
rep("""  plZ(K.x0+0.01, 3.17, 5.51); plZ(HA.x1-0.01, 3.17, DH.bath.z0); plZ(HA.x1-0.01, DH.bath.z1, 5.51);
  pl(HA.x1+0.01, 5.51, DH.ent.x1+0.05, 5.51); pl(DH.ent.x0-0.05, 5.51, K.x0+0.01, 5.51);""",
    """  plZ(K.x0+0.01, 3.17, P.room.z1-0.01); plZ(HA.x1-0.01, 3.17, DH.bath.z0); plZ(HA.x1-0.01, DH.bath.z1, P.room.z1-0.01);
  pl(HA.x1+0.01, P.room.z1-0.01, DH.ent.x1+0.05, P.room.z1-0.01); pl(DH.ent.x0-0.05, P.room.z1-0.01, K.x0+0.01, P.room.z1-0.01);""")

# --- подсказки/размеры под новую геометрию
rep("  room:     [ [1.70, 1.50, 3.10],        [0,0,-1] ],",
    "  room:     [ [1.45, 1.50, 3.40],        [0,0,-1] ],")
rep("  entrance: [ [4.30, 1.55, 5.95],        [0,0,-1] ]",
    "  entrance: [ [4.05, 1.55, 6.95],        [0,0,-1] ]")
rep("  { p:[1.70, 0.30, 2.76], t:'комната 3,41 × 5,52 = 18,8 м²' },",
    "  { p:[1.45, 0.30, 3.10], t:'комната 3,91 × 6,32 ≈ 24,7 м²' },")
rep("  { p:[4.30, 1.55, 6.40], t:'площадка · лифт · кв. 278' }",
    "  { p:[4.05, 1.55, 7.05], t:'площадка · лифт · кв. 278' }")

p.write_text(s, encoding='utf-8')
print('G1 template ok')

# --- data.json
d = pathlib.Path('_tools/data.json')
t = d.read_text(encoding='utf-8')


def repj(old, new):
    global t
    assert old in t, 'JSON NOT FOUND: ' + old[:100]
    t = t.replace(old, new, 1)


repj('"value": "3,41 × 5,52 м = 18,8 м²", "note": "лоджия на фасаде (остеклена)"',
     '"value": "3,91 × 6,32 м ≈ 24,7 м²", "note": "по замерам хозяина · лоджия на фасаде (остеклена)"')
repj('"spawn": {"x": 4.3, "z": 6.6, "yaw": 0.0,',
     '"spawn": {"x": 4.2, "z": 7.0, "yaw": 0.0,')
repj('{"id": "hall", "t": "Коридор", "x": 4.27, "z": 4.6, "yaw": 0.0},',
     '{"id": "hall", "t": "Коридор", "x": 4.27, "z": 4.6, "yaw": 0.0},\n      {"id": "entry", "t": "Прихожая", "x": 3.85, "z": 5.9, "yaw": 3.14},')
d.write_text(t, encoding='utf-8')
print('G1 data ok')
