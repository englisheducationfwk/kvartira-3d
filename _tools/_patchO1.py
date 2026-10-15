# -*- coding: utf-8 -*-
"""O1: верхние шкафы — половинчатый шкафчик над плитой (корпус вдвое ниже),
все остальные полые с полками; предметы ставятся внутрь, если влезают по высоте."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:140]
    s = s.replace(old, new, 1)


# --- глобалы для проверки габаритов при постановке ---
rep("var handles = [], patches = [], doorsGrp, upGrp, socket, sockHole, det, detHole, mold1, mold2, filmK, filmW, filmW2, ventMesh;",
    "var handles = [], patches = [], doorsGrp, upGrp, socket, sockHole, det, detHole, mold1, mold2, filmK, filmW, filmW2, ventMesh;\nvar UPLIM = null, LOWLIM = null;   /* объёмы шкафов — постановка предметов по размеру */")

# --- верхние шкафы: полые по секциям; над плитой — половинчатый корпус ---
rep("""  /* верхние шкафы: 4 одинаковых фасада до самой стены, тоже открываются */
  upGrp = new THREE.Group();
  var up = new THREE.Mesh(new THREE.BoxGeometry(0.34, UPH, 2.33), M.carcass);
  up.position.set(mx(KX-0.17), WT+AH+UPH/2, 1.825); up.castShadow = up.receiveShadow = true; upGrp.add(up);
  var UZD = (2.99 - 0.66) / 4;
  var UY0 = WT+AH, UY1 = WT+AH+UPH, UYM = (UY0+UY1)/2;   /* низ/верх/середина шкафов */
  for (var i3=0;i3<4;i3++){""",
"""  /* верхние шкафы: полые, с полками (как низ) — внутрь можно ставить предметы */
  upGrp = new THREE.Group();
  var UZD = (2.99 - 0.66) / 4;
  var UY0 = WT+AH, UY1 = WT+AH+UPH, UYM = (UY0+UY1)/2;   /* низ/верх/середина шкафов */
  UPLIM = { x0:KX-0.38, x1:KX, z0:0.62, z1:2.99, y0:UY0, y1:UY1, ymid:UYM,
            halfZ:0.66+UZD, halfZ1:0.66+2*UZD };      /* 2-я секция — половинчатая, над плитой */
  LOWLIM = { x0:KX-0.62, x1:KX, z0:0.48, z1:2.99, y0:BASE, y1:BASE+LOWH, ymid:BASE+0.30 };
  for (var i4=0;i4<4;i4++){
    var z4 = 0.66 + UZD/2 + i4*UZD;
    var y4a = (i4 === 1) ? UYM : UY0;                 /* половинчатый — только верхняя половина */
    solidBox(KX-0.36, KX-0.01, z4-UZD/2+0.01, z4+UZD/2-0.01, y4a, y4a+0.02, { side:M.carcass }, 1, upGrp);
    solidBox(KX-0.36, KX-0.01, z4-UZD/2+0.01, z4+UZD/2-0.01, UY1-0.02, UY1, { side:M.carcass }, 1, upGrp);
    solidBox(KX-0.04, KX-0.01, z4-UZD/2+0.01, z4+UZD/2-0.01, y4a, UY1, { side:M.dark, nx:M.dark }, 1, upGrp);
    solidBox(KX-0.36, KX-0.01, z4-UZD/2+0.001, z4-UZD/2+0.021, y4a, UY1, { side:M.carcass }, 1, upGrp);
    solidBox(KX-0.36, KX-0.01, z4+UZD/2-0.021, z4+UZD/2-0.001, y4a, UY1, { side:M.carcass }, 1, upGrp);
    if (i4 !== 1){
      solidBox(KX-0.35, KX-0.03, z4-UZD/2+0.03, z4+UZD/2-0.03, UYM-0.015, UYM+0.015, { side:M.carcass }, 1, upGrp);
    }
  }
  for (var i3=0;i3<4;i3++){""")

# --- постановка: запоминаем низ/высоту предмета, ставим на поверхность, проверяем габарит ---
rep("""function pickUp(g){
  var b3 = new THREE.Box3().setFromObject(g);
  var c = b3.getCenter(new THREE.Vector3());
  g.userData.cc = [c.x, c.z];""",
"""function pickUp(g){
  g.updateMatrixWorld(true);
  var b3 = new THREE.Box3().setFromObject(g);
  var c = b3.getCenter(new THREE.Vector3());
  g.userData.cc = [c.x, c.z];
  g.userData.baseOff = b3.min.y - g.position.y;   /* низ предмета относительно его нуля */
  g.userData.hgt = b3.max.y - b3.min.y;""")

rep("""  if (p){
    var pad = (n.y > 0.7) ? 0.02 : 0.30;
    p.add(n.multiplyScalar(pad));
  } else {""",
"""  if (p){
    var pad = (n.y > 0.7) ? 0.02 : 0.30;
    p.add(n.multiplyScalar(pad));
    p.surfUp = (n.y > 0.7);                       /* легло на горизонталь — можно ставить ровно */
  } else {""")

rep("""  var p = aimTarget(nx, ny);
  if (!p) return;
  var cc = it.g.userData.cc || [p.x, p.z];
  it.g.position.x += (p.x - cc[0]);
  it.g.position.z += (p.z - cc[1]);
  it.g.userData.cc = [p.x, p.z];
  it.g.visible = true;
  if (doPaint) paint();
}""",
"""  var p = aimTarget(nx, ny);
  if (!p) return;
  var cc = it.g.userData.cc || [p.x, p.z];
  it.g.position.x += (p.x - cc[0]);
  it.g.position.z += (p.z - cc[1]);
  it.g.userData.cc = [p.x, p.z];
  if (p.surfUp && it.g.userData.baseOff !== undefined){
    it.g.position.y = p.y - it.g.userData.baseOff;   /* ставим ровно на поверхность */
  }
  it.g.visible = true;
  if (doPaint) paint();
}""")

rep("""function placeHeld(nx, ny){
  if (held < 0 || !inv[held]){ toast('Сначала выбери вещь в слотах (1–9)'); return; }
  var p = aimTarget(nx, ny);
  if (!p){ toast('Наведись на пол и поставь'); return; }
  commitPlace(inv[held], p.x, p.z);
}
function placeAt(it, x, z){ commitPlace(it, x, z); }
function commitPlace(it, x, z){
  var cc = it.g.userData.cc || [x, z];
  it.g.position.x += (x - cc[0]);
  it.g.position.z += (z - cc[1]);
  it.g.userData.cc = [x, z];""",
"""/* влезает ли предмет по высоте на это место (шкафы, полки, столешница под шкафами) */
function placeCheck(it, p){
  if (!p || !p.surfUp) return true;
  var h = it.g.userData.hgt;
  if (h === undefined) return true;
  function fits(top){
    var avail = top - p.y;
    if (h > avail + 0.005){
      toast('Не влезает по высоте: тут свободно ' + Math.max(0, avail).toFixed(2) + ' м');
      return false;
    }
    return true;
  }
  var U = UPLIM, Lo = LOWLIM;
  if (U && p.y > U.y0 - 0.03 && p.y < U.y1 && p.x > U.x0 && p.x < U.x1 && p.z > U.z0 && p.z < U.z1){
    var top = (p.y < U.ymid - 0.005) ? U.ymid - 0.015 : U.y1;
    if (p.z > U.halfZ && p.z < U.halfZ1 && p.y < U.ymid) top = U.ymid;
    return fits(top);
  }
  if (U && p.y <= U.y0 + 0.03 && p.x > U.x0 && p.x < U.x1 && p.z > U.z0 && p.z < U.z1){
    var top2 = U.y0;                               /* столешница под верхними шкафами */
    if (p.z > U.halfZ && p.z < U.halfZ1) top2 = U.ymid;
    return fits(top2);
  }
  if (Lo && p.y > Lo.y0 - 0.05 && p.y < Lo.y1 && p.x > Lo.x0 && p.x < Lo.x1 && p.z > Lo.z0 && p.z < Lo.z1){
    var topL = (p.y < Lo.ymid - 0.005) ? Lo.ymid : Lo.y1;
    return fits(topL);
  }
  return true;
}
function placeHeld(nx, ny){
  if (held < 0 || !inv[held]){ toast('Сначала выбери вещь в слотах (1–9)'); return; }
  var p = aimTarget(nx, ny);
  if (!p){ toast('Наведись на пол и поставь'); return; }
  if (!placeCheck(inv[held], p)) return;
  commitPlace(inv[held], p.x, p.z, p.surfUp ? p.y : null);
}
function placeAt(it, x, z){ commitPlace(it, x, z); }
function commitPlace(it, x, z, y){
  var cc = it.g.userData.cc || [x, z];
  it.g.position.x += (x - cc[0]);
  it.g.position.z += (z - cc[1]);
  it.g.userData.cc = [x, z];
  if (y !== undefined && y !== null && it.g.userData.baseOff !== undefined){
    it.g.position.y = y - it.g.userData.baseOff;
  }""")

p.write_text(s, encoding='utf-8')
print('O1 ok')
