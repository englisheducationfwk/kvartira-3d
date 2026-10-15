"""L1: окна эркера — все одинаковые (первое на скосе + два спереди по 0.85);
маленький диван — длиннее/шире в 1.3 и без мерцания; дверь комнаты не задевает стену;
мерцание у входа (совпадение грани) и полоса-выемка у входа убраны; плинтус у двери;
линолеум коридора — единый рисунок (мировая фаза UV); второй верхний фасад — верхняя
половинка, низ убран."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# ---------- 1) окна эркера: передние две ровно по 0.85, скос — по максимуму ----------
rep("    var parts = [ [1.00, 0.00], [0.70, 1.00] ];",
    "    var parts = [ [0.85, 0.00], [0.85, 0.85] ];")
rep("""    var len = Math.hypot(B2[0]-A2[0], B2[1]-A2[1]);
    var ux = (B2[0]-A2[0])/len, uz = (B2[1]-A2[1])/len;
    var w = len - 0.10, off = 0.05;""",
    """    var len = Math.hypot(B2[0]-A2[0], B2[1]-A2[1]);
    var ux = (B2[0]-A2[0])/len, uz = (B2[1]-A2[1])/len;
    var w = len - 0.08, off = 0.04;""")

# ---------- 2) маленький диван: длиннее и шире в 1.3, без наложения граней ----------
rep("""  var IT = item('Диван (маленький)', '🛋', 0.74, 0.52);
  ibox(IT, 1.60, 5.99, 1.44, 0.66, 0.15, 0.27, M.woodDark);            /* каркас */
  [[0.98,5.72],[2.22,5.72],[0.98,6.26],[2.22,6.26]].forEach(function(lg){
    ibox(IT, lg[0], lg[1], 0.05, 0.05, 0, 0.15, M.woodDark);           /* ножки */
  });
  ibox(IT, 0.94, 5.99, 0.12, 0.70, 0, 0.60, M.fabric2);                /* подлокотники */
  ibox(IT, 2.26, 5.99, 0.12, 0.70, 0, 0.60, M.fabric2);
  ibox(IT, 1.60, 5.58, 1.24, 0.46, 0.27, 0.50, M.fabric);              /* сиденье выдвинуто */
  ibox(IT, 1.60, 6.08, 1.24, 0.44, 0.27, 0.50, M.fabric);              /* лежак */
  ibox(IT, 1.60, 6.27, 1.24, 0.10, 0.30, 0.58, M.fabric2);             /* спинка лежит у стены */""",
    """  var IT = item('Диван (маленький)', '🛋', 0.94, 0.68);
  ibox(IT, 1.58, 6.00, 1.87, 0.86, 0.15, 0.27, M.woodDark);            /* каркас */
  [[0.74,5.66],[2.42,5.66],[0.74,6.34],[2.42,6.34]].forEach(function(lg){
    ibox(IT, lg[0], lg[1], 0.06, 0.06, 0, 0.15, M.woodDark);           /* ножки */
  });
  ibox(IT, 0.73, 6.00, 0.12, 0.90, 0, 0.68, M.fabric2);                /* подлокотники */
  ibox(IT, 2.43, 6.00, 0.12, 0.90, 0, 0.68, M.fabric2);
  ibox(IT, 1.58, 5.36, 1.61, 0.60, 0.25, 0.50, M.fabric);              /* сиденье выдвинуто */
  ibox(IT, 1.58, 5.98, 1.61, 0.56, 0.25, 0.50, M.fabric);              /* лежак */
  ibox(IT, 1.58, 6.255, 1.61, 0.13, 0.28, 0.60, M.fabric2);            /* спинка лежит у стены */""")

# ---------- 3) дверь комнаты: полотно ровно по проёму, чтобы не задевало стену ----------
rep("    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1-0.02, 0.80, [0,-1], [-1,0]),",
    "    room: mkDoor(K.x0-P.LOAD/2, DH.room.z1-0.01, 0.79, [0,-1], [-1,0]),")

# ---------- 4) мерцание у входной: стена входа не совпадает гранью с перегородкой ----------
rep("  solidBox(K.x0-P.LOAD, DH.ent.x0, HA.z1, HA.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });",
    "  solidBox(K.x0, DH.ent.x0, HA.z1, HA.z1+P.LOAD, 0, P.HC, { pz:M.hallWall, nz:M.wall2 });")
rep("  seg(K.x0-P.LOAD, HA.z1+P.LOAD/2, DH.ent.x0, HA.z1+P.LOAD/2, P.LOAD/2);",
    "  seg(K.x0, HA.z1+P.LOAD/2, DH.ent.x0, HA.z1+P.LOAD/2, P.LOAD/2);")
# восточная стена не доходит до входной (грань в грань не совпадает)
rep("  solidBox(K.x1, K.x1+P.LOAD, BA.z1+P.LOAD, HA.z1+P.LOAD, 0, P.HC, { nx:M.wall2 });",
    "  solidBox(K.x1, K.x1+P.LOAD, BA.z1+P.LOAD, HA.z1, 0, P.HC, { nx:M.wall2 });")

# ---------- 5) выемка у входа: полоса-ниша убрана, там сплошная стена ----------
rep("""    slab(L0, K.x0-P.LOAD, P.room.z1+P.LOAD, WZ);          /* полоса у входа */
    clg(L0, K.x0-P.LOAD, P.room.z1+P.LOAD, WZ);""",
    """    /* ниша слева от входа убрана: там стена соседа (сплошная) */
    (function(){
      var nz = new THREE.Mesh(new THREE.BoxGeometry(K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.concrete,M.concrete]);
      fixBoxUV(nz.geometry, K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD), 1);
      nz.position.set((L0-0.12+K.x0-P.LOAD)/2, 1.36, (P.room.z1+P.LOAD+WZ)/2);
      nz.receiveShadow = true; g.add(nz);
    })();""")
rep("  ceilPlane({ x0:2.70, x1:3.11, z0:6.78, z1:7.30 });", "")

# ---------- 6) плинтус у двери не проходит через проём ----------
rep("  pl(HA.x1+0.01, HA.z1-0.01, BA.x1+P.LOAD-0.02, HA.z1-0.01);",
    "  pl(DH.ent.x1+0.05, HA.z1-0.01, BA.x1+P.LOAD-0.02, HA.z1-0.01);")

# ---------- 7) линолеум: единый рисунок по миру (UV в мировых координатах) ----------
rep("""  function floorBox(r, mat, uvScale){
    var x0 = Math.min(mx(r.x0), mx(r.x1)) - 0.08, x1 = Math.max(mx(r.x0), mx(r.x1)) + 0.08;
    var m = new THREE.Mesh(new THREE.BoxGeometry(x1-x0, 0.02, (r.z1-r.z0)+0.16), mat);
    fixBoxUV(m.geometry, x1-x0, 0.02, r.z1-r.z0, uvScale);
    m.position.set((x0+x1)/2, 0.011, (r.z0+r.z1)/2); m.receiveShadow = true; gRoom.add(m);
  }""",
    """  function floorBox(r, mat, uvScale){
    var x0 = Math.min(mx(r.x0), mx(r.x1)) - 0.08, x1 = Math.max(mx(r.x0), mx(r.x1)) + 0.08;
    var m = new THREE.Mesh(new THREE.BoxGeometry(x1-x0, 0.02, (r.z1-r.z0)+0.16), mat);
    fixBoxUV(m.geometry, x1-x0, 0.02, r.z1-r.z0, uvScale);
    /* рисунок привязан к мировым координатам — швов между кусками пола нет */
    var uvs = m.geometry.attributes.uv, ou = x0/uvScale, oz = (r.z0-0.08)/uvScale;
    for (var ui = 0; ui < uvs.count; ui++) uvs.setXY(ui, uvs.getX(ui)+ou, uvs.getY(ui)+oz);
    uvs.needsUpdate = true;
    m.position.set((x0+x1)/2, 0.011, (r.z0+r.z1)/2); m.receiveShadow = true; gRoom.add(m);
  }""")

# ---------- 8) второй верхний фасад: только верхняя половинка, низ убран ----------
rep("""    var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.02, UZD-0.02), M.front);
    d2.position.set(mx(KX-0.35), UYM, uz); d2.castShadow = d2.receiveShadow = true;
    var hu = mkHinge(d2, mx(KX-0.35), uz - (UZD-0.02)/2 + 0.01, 'шкафчик', -1.8, upGrp);
    var uh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
    uh.position.set(-0.025, UY0-UYM+0.09, UZD-0.02-0.055);
    uh.castShadow = true; handles.push(uh); hu.grp.add(uh);
  }""",
    """    if (i3 === 1){
      /* второй фасад обрезан в половину: верхняя дверца, низ — открытая секция */
      var d2h = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.front);
      d2h.position.set(mx(KX-0.35), (UYM+UY1)/2-0.005, uz); d2h.castShadow = d2h.receiveShadow = true;
      var hh2 = mkHinge(d2h, mx(KX-0.35), uz-(UZD-0.02)/2+0.01, 'шкафчик', -1.8, upGrp);
      var uhh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uhh.position.set(-0.025, (UPH/2-0.03)-0.075, UZD-0.02-0.055);
      uhh.castShadow = true; handles.push(uhh); hh2.grp.add(uhh);
    } else {
      var d2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH-0.02, UZD-0.02), M.front);
      d2.position.set(mx(KX-0.35), UYM, uz); d2.castShadow = d2.receiveShadow = true;
      var hu = mkHinge(d2, mx(KX-0.35), uz - (UZD-0.02)/2 + 0.01, 'шкафчик', -1.8, upGrp);
      var uh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uh.position.set(-0.025, UY0-UYM+0.09, UZD-0.02-0.055);
      uh.castShadow = true; handles.push(uh); hu.grp.add(uh);
    }
  }""")

# ---------- 9) площадка: плита пола заходит под боковые стены (без щелей) ----------
rep("    slab(L0, L1, WZ, LAND.z1);", "    slab(L0-0.12, L1+0.12, WZ, LAND.z1);")
rep("    w(L0, L1, LAND.z1, 0.12);", "    w(L0-0.12, L1+0.12, LAND.z1, 0.12);")

p.write_text(s, encoding='utf-8')
print('L1 ok')
