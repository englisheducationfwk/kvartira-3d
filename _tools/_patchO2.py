# -*- coding: utf-8 -*-
"""O2: площадка перед входом — сотри и заново: ровные чистые стены без огрызков,
пол и потолок единой плитой, простенки у входной стены сплошные."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')

OLD = """  /* ---------- площадка с лифтами ---------- */
  (function(){
    var g = new THREE.Group(); gRoom.add(g);
    var L0 = Math.min(mx(LAND.x0), mx(LAND.x1)), L1 = Math.max(mx(LAND.x0), mx(LAND.x1));
    var E0 = Math.min(mx(DH.ent.x0), mx(DH.ent.x1)), E1 = Math.max(mx(DH.ent.x0), mx(DH.ent.x1));
    var WZ = HA.z1 + P.LOAD;                       /* южная плоскость входной стены */
    function slab(x0, x1, z0, z1){
      var m = new THREE.Mesh(new THREE.BoxGeometry(x1-x0, 0.08, z1-z0), M.concrete);
      fixBoxUV(m.geometry, x1-x0, 0.08, z1-z0, 1);
      m.position.set((x0+x1)/2, -0.038, (z0+z1)/2); m.receiveShadow = true; g.add(m); return m;
    }
    slab(L0-0.12, L1+0.12, WZ, LAND.z1);
    function clg(x0, x1, z0, z1){
      var m = new THREE.Mesh(new THREE.PlaneGeometry(x1-x0, z1-z0), M.ceil);
      m.rotation.x = Math.PI/2; m.position.set((x0+x1)/2, 2.718, (z0+z1)/2);
      m.castShadow = true; g.add(m); return m;
    }
    clg(L0-0.12, L1+0.12, WZ, LAND.z1);
    function w(x0,x1,zc,th,y0,y1,inM,outM){
      var m = new THREE.Mesh(new THREE.BoxGeometry(Math.abs(x1-x0), (y1||2.72)-(y0||0), th),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,inM||M.hallWall,outM||M.concrete]);
      fixBoxUV(m.geometry, Math.abs(x1-x0), (y1||2.72)-(y0||0), th, 1);
      m.position.set((x0+x1)/2, ((y0||0)+(y1||2.72))/2, zc); m.receiveShadow = true; g.add(m); return m;
    }
    /* боковые стены площадки — во всю длину (раньше были огрызки — светилась дыра) */
    (function(){
      var z0 = P.room.z1+P.LOAD, z1 = LAND.z1;
      var mw = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.78, z1-z0),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.concrete,M.hallWall]);
      fixBoxUV(mw.geometry, 0.12, 2.78, z1-z0, 1);
      mw.position.set(L0-0.06, 1.37, (z0+z1)/2); mw.receiveShadow = true; g.add(mw);
      var me = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.78, z1-z0),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.hallWall,M.concrete]);
      fixBoxUV(me.geometry, 0.12, 2.78, z1-z0, 1);
      me.position.set(L1+0.06, 1.37, (z0+z1)/2); me.receiveShadow = true; g.add(me);
    })();
    /* ниша слева от входа убрана: там стена соседа (сплошная) */
    (function(){
      var nz = new THREE.Mesh(new THREE.BoxGeometry(K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.hallWall,M.concrete]);
      fixBoxUV(nz.geometry, K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD), 1);
      nz.position.set((L0-0.12+K.x0-P.LOAD)/2, 1.36, (P.room.z1+P.LOAD+WZ)/2);
      nz.receiveShadow = true; g.add(nz);
      /* и справа от входа — такая же стена (была дырка в пустоту) */
      var nz2 = new THREE.Mesh(new THREE.BoxGeometry(L1+0.12-(K.x1+P.LOAD), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.hallWall,M.concrete]);
      fixBoxUV(nz2.geometry, L1+0.12-(K.x1+P.LOAD), 2.72, WZ-(P.room.z1+P.LOAD), 1);
      nz2.position.set((K.x1+P.LOAD+L1+0.12)/2, 1.36, (P.room.z1+P.LOAD+WZ)/2);
      nz2.receiveShadow = true; g.add(nz2);
    })();
    w(L0-0.12, L1+0.12, LAND.z1, 0.12);
    /* север — стена квартиры целиком (входная дверь в нише, см. ниже) */
    seg(LAND.x0, P.room.z1, LAND.x0, LAND.z1, 0.08);
    seg(LAND.x1, WZ, LAND.x1, LAND.z1, 0.08);
    seg(LAND.x0, LAND.z1, LAND.x1, LAND.z1, 0.08);
    /* ниша-выемка у двери убрана — стена просто ровная (по отметке) */
    /* дверь (полотно) — интерактивная, см. DOORS.ent */
    var j1 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 2.14, 0.12), M.frame);
    j1.position.set(E0-0.09, 1.07, WZ); g.add(j1);
    var j2 = j1.clone(); j2.position.x = E1+0.02; g.add(j2);
    var j3 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0+0.14, 0.07, 0.12), M.frame);
    j3.position.set((E0+E1)/2, 2.14, WZ); g.add(j3);
    /* табличку-номер с внутренней стороны убрали */
    /* просто стены (лифты и дверь соседа убраны по отметкам) */
    g.traverse(function(o){ if(o.isMesh){ o.receiveShadow = true; } });
  })();"""

NEW = """  /* ---------- площадка перед входом — начисто: ровные стены без огрызков ---------- */
  (function(){
    var g = new THREE.Group(); gRoom.add(g);
    var L0 = Math.min(mx(LAND.x0), mx(LAND.x1)), L1 = Math.max(mx(LAND.x0), mx(LAND.x1));
    var E0 = Math.min(mx(DH.ent.x0), mx(DH.ent.x1)), E1 = Math.max(mx(DH.ent.x0), mx(DH.ent.x1));
    var WZ = HA.z1 + P.LOAD;                       /* южная плоскость входной стены */
    var SZ = LAND.z1;
    var HH = 2.72, TH = 0.12;
    function bx(x0, x1, y0, y1, z0, z1, mats, mv){
      var m = new THREE.Mesh(new THREE.BoxGeometry(x1-x0, y1-y0, z1-z0), mats);
      fixBoxUV(m.geometry, x1-x0, y1-y0, z1-z0, mv || 1);
      m.position.set((x0+x1)/2, (y0+y1)/2, (z0+z1)/2); m.receiveShadow = true; g.add(m); return m;
    }
    /* пол и потолок — единой плитой во всю площадку */
    bx(L0-TH, L1+TH, -0.08, 0.0, WZ-TH, SZ+TH, M.concrete);
    bx(L0-TH, L1+TH, HH, HH+0.10, WZ-TH, SZ+TH, M.ceilB);
    /* западная и восточная стены — во всю длину, гладкие */
    bx(L0-TH, L0, 0, HH, WZ-TH, SZ+TH, [M.hallWall, M.concrete, M.concrete, M.concrete, M.concrete, M.concrete]);
    bx(L1, L1+TH, 0, HH, WZ-TH, SZ+TH, [M.concrete, M.hallWall, M.concrete, M.concrete, M.concrete, M.concrete]);
    /* южная стена — во всю ширину */
    bx(L0-TH, L1+TH, 0, HH, SZ, SZ+TH, [M.concrete, M.concrete, M.concrete, M.concrete, M.concrete, M.hallWall]);
    /* простенки у входной стены слева и справа от квартиры — сплошные, встык */
    bx(L0-TH, K.x0-P.LOAD, 0, HH, P.room.z1+P.LOAD, WZ, [M.concrete, M.concrete, M.concrete, M.concrete, M.hallWall, M.concrete]);
    bx(K.x1+P.LOAD, L1+TH, 0, HH, P.room.z1+P.LOAD, WZ, [M.concrete, M.concrete, M.concrete, M.concrete, M.hallWall, M.concrete]);
    seg(LAND.x0, P.room.z1, LAND.x0, LAND.z1, 0.08);
    seg(LAND.x1, WZ, LAND.x1, LAND.z1, 0.08);
    seg(LAND.x0, LAND.z1, LAND.x1, LAND.z1, 0.08);
    /* дверь (полотно) — интерактивная, см. DOORS.ent */
    var j1 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 2.14, 0.12), M.frame);
    j1.position.set(E0-0.09, 1.07, WZ); g.add(j1);
    var j2 = j1.clone(); j2.position.x = E1+0.02; g.add(j2);
    var j3 = new THREE.Mesh(new THREE.BoxGeometry(E1-E0+0.14, 0.07, 0.12), M.frame);
    j3.position.set((E0+E1)/2, 2.14, WZ); g.add(j3);
    g.traverse(function(o){ if(o.isMesh){ o.receiveShadow = true; } });
  })();"""

assert OLD in s, 'LANDING BLOCK NOT FOUND'
assert s.count(OLD) == 1
s = s.replace(OLD, NEW, 1)
p.write_text(s, encoding='utf-8')
print('O2 ok')
