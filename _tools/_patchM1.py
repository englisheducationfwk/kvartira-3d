"""M1: наличники дверей прижаты к проёмам (это и был «пиздец» — планки висели в 9 см),
половинчатый шкафчик над плитой (полудверца + полка под ней), дырка-ниша на площадке
перед входом заделана, окна — три одинаковых 0.48 (первое на скосе), стена вокруг
передних створок."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:130]
    s = s.replace(old, new, count)


# ---------- 1) наличники ровно по проёмам ----------
rep("  bs(P.LOAD+0.06, 2.14, 0.06, mx(K.x0-P.LOAD/2), 1.07, DH.room.z1+0.09);",
    "  bs(P.LOAD+0.06, 2.14, 0.06, mx(K.x0-P.LOAD/2), 1.07, DH.room.z1+0.02);")
rep("  bs(0.06, 2.14, P.LOAD+0.06, mx(DH.kit.x0-0.09), 1.07, K.z1+P.LOAD/2);",
    "  bs(0.06, 2.14, P.LOAD+0.06, mx(DH.kit.x0-0.02), 1.07, K.z1+P.LOAD/2);")
rep("  bs(P.PART+0.08, 2.14, 0.06, mx((HA.x1+BA.x0)/2), 1.07, DH.bath.z0-0.09);",
    "  bs(P.PART+0.08, 2.14, 0.06, mx((HA.x1+BA.x0)/2), 1.07, DH.bath.z0-0.02);")

# ---------- 2) половинчатый шкафчик над плитой: полудверца + полка под ней ----------
rep("""    if (i3 === 1){
      /* второй фасад обрезан в половину: верхняя дверца, низ — открытая секция */
      var d2h = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.front);
      d2h.position.set(mx(KX-0.35), (UYM+UY1)/2-0.005, uz); d2h.castShadow = d2h.receiveShadow = true;
      var hh2 = mkHinge(d2h, mx(KX-0.35), uz-(UZD-0.02)/2+0.01, 'шкафчик', -1.8, upGrp);
      var uhh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uhh.position.set(-0.025, (UPH/2-0.03)-0.075, UZD-0.02-0.055);
      uhh.castShadow = true; handles.push(uhh); hh2.grp.add(uhh);
    } else {""",
    """    if (i3 === 1){
      /* половинчатый шкафчик над плитой: полудверца сверху + полка под ней */
      var d2h = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.front);
      d2h.position.set(mx(KX-0.35), (UYM+UY1)/2-0.005, uz); d2h.castShadow = d2h.receiveShadow = true;
      var hh2 = mkHinge(d2h, mx(KX-0.35), uz-(UZD-0.02)/2+0.01, 'шкафчик', -1.8, upGrp);
      var uhh = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.13, 0.02), M.handleOld);
      uhh.position.set(-0.025, (UPH/2-0.03)-0.075, UZD-0.02-0.055);
      uhh.castShadow = true; handles.push(uhh); hh2.grp.add(uhh);
      var shelf2 = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.03, UZD-0.02), M.carcass);
      shelf2.position.set(mx(KX-0.17), UYM-0.02, uz); shelf2.castShadow = shelf2.receiveShadow = true;
      upGrp.add(shelf2);
      var back2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, UPH/2-0.03, UZD-0.02), M.carcass);
      back2.position.set(mx(KX-0.335), (UY0+UYM)/2, uz); upGrp.add(back2);
    } else {""")

# ---------- 3) ниша на площадке перед входом (дырка) заделана сплошной стеной ----------
rep("""    /* ниша слева от входа убрана: там стена соседа (сплошная) */
    (function(){
      var nz = new THREE.Mesh(new THREE.BoxGeometry(K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.concrete,M.concrete]);
      fixBoxUV(nz.geometry, K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD), 1);
      nz.position.set((L0-0.12+K.x0-P.LOAD)/2, 1.36, (P.room.z1+P.LOAD+WZ)/2);
      nz.receiveShadow = true; g.add(nz);
    })();""",
    """    /* ниша слева от входа убрана: там стена соседа (сплошная) */
    (function(){
      var nz = new THREE.Mesh(new THREE.BoxGeometry(K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.concrete,M.concrete]);
      fixBoxUV(nz.geometry, K.x0-P.LOAD-(L0-0.12), 2.72, WZ-(P.room.z1+P.LOAD), 1);
      nz.position.set((L0-0.12+K.x0-P.LOAD)/2, 1.36, (P.room.z1+P.LOAD+WZ)/2);
      nz.receiveShadow = true; g.add(nz);
      /* и справа от входа — такая же стена (была дырка в пустоту) */
      var nz2 = new THREE.Mesh(new THREE.BoxGeometry(L1+0.12-(K.x1+P.LOAD), 2.72, WZ-(P.room.z1+P.LOAD)),
        [DEF_M,DEF_M,M.ceilB,M.ceilB,M.concrete,M.concrete]);
      fixBoxUV(nz2.geometry, L1+0.12-(K.x1+P.LOAD), 2.72, WZ-(P.room.z1+P.LOAD), 1);
      nz2.position.set((K.x1+P.LOAD+L1+0.12)/2, 1.36, (P.room.z1+P.LOAD+WZ)/2);
      nz2.receiveShadow = true; g.add(nz2);
    })();""")

# ---------- 4) окна: три одинаковых 0.48 + стена вокруг передних ----------
rep("    var parts = [ [0.85, 0.00], [0.85, 0.85] ];",
    "    var parts = [ [0.48, 0.37], [0.48, 0.85] ];")
rep("""    var w = len - 0.08, off = 0.04;""",
    """    var w = len - 0.04, off = 0.02;""")
# глухие части фронта: низ, верх и стойки по бокам створок
rep("""  /* первое окно — вертикально на левом скосе (диагонали), открывается кликом */""",
    """  /* фронт: глухие части вокруг двух створок (стена красиво с окнами) */
  (function(){
    var a = BAY.p1, b = BAY.p2;
    var A2 = mp(a), B2 = mp(b);
    var len = Math.hypot(B2[0]-A2[0], B2[1]-A2[1]);
    var ux = (B2[0]-A2[0])/len, uz = (B2[1]-A2[1])/len;
    function sub(t0, t1, y0, y1){
      var m = solidBeam([A2[0]+ux*t0*len, A2[1]+uz*t0*len],
                        [A2[0]+ux*t1*len, A2[1]+uz*t1*len],
                        P.LOAD, y0, y1, null, M.facade2, 1.35, gRoom);
      if (m && m.userData.innerIdx !== undefined) stagedFaces.push({ mesh:m, idx:m.userData.innerIdx });
      return m;
    }
    var BWP0 = P.bay.winH + P.bay.sillY;
    sub(0, 1, 0, P.bay.sillY);                 /* низ по всей ширине */
    sub(0, 1, BWP0, P.HC);                     /* верх по всей ширине */
    sub(0, 0.37/1.70, P.bay.sillY, BWP0);      /* стойки по бокам створок */
    sub(1.33/1.70, 1, P.bay.sillY, BWP0);
  })();
  /* первое окно — вертикально на левом скосе (диагонали), открывается кликом */""")

p.write_text(s, encoding='utf-8')
print('M1 ok')
