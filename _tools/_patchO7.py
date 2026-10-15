# -*- coding: utf-8 -*-
"""O7: (1) сохраняется и высота предметов (полки/подоконники) — всё как оставил, до сброса;
(2) фон за окном больше не «висит» — опущен до земли и расширен;
(3) клавиша P — точная подгонка: стрелки вверх/вниз/влево/вправо по 5 см,
можно ставить сквозь предметы (без проверок)."""
import pathlib

p = pathlib.Path(__file__).with_name('template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    assert s.count(old) == 1, 'NOT UNIQUE: ' + old[:140]
    s = s.replace(old, new, 1)


# ---------- 1) высота предмета сохраняется ----------
rep("  state.moved[it.name] = [x, z, state.mirror];",
    "  state.moved[it.name] = [x, z, state.mirror, +it.g.position.y.toFixed(3)];")

rep("""      g.userData.cc = [tx, mv[1]];
    }
  });""",
"""      g.userData.cc = [tx, mv[1]];
      if (mv.length > 3 && isFinite(mv[3])) g.position.y = mv[3];   /* высота как оставил */
    }
  });""")

# ---------- 2) фон за окном — до земли, не висит ----------
rep("  var HZ = h*0.53;                       /* линия горизонта — примерно на уровне глаз */",
    "  var HZ = h*0.405;                      /* линия горизонта — примерно на уровне глаз */")

rep("  outside:   new THREE.MeshBasicMaterial({ map:texOutside }),",
    "  outside:   new THREE.MeshBasicMaterial({ map:texOutside, side:THREE.DoubleSide }),")

rep("""  var outP = new THREE.Mesh(new THREE.PlaneGeometry(34, 14), M.outside);
  outP.position.set(mx(3.2), 3.4, -7.6); gRoom.add(outP);""",
"""  var outP = new THREE.Mesh(new THREE.PlaneGeometry(140, 60), M.outside);
  outP.position.set(mx(3.2), -3.9, -7.6); gRoom.add(outP);   /* низ до земли (−33.9) — не висит */""")

rep("  var yard = new THREE.Mesh(new THREE.PlaneGeometry(220, 220),",
    "  var yard = new THREE.Mesh(new THREE.PlaneGeometry(420, 420),")

# ---------- 3) P — точная подгонка стрелками ----------
rep("var pickables = [], inv = [], held = -1;",
    "var pickables = [], inv = [], held = -1;\nvar fineMode = false;   /* P: предмет двигается стрелками по 5 см, без проверок */")

rep("""  if (pinv[0] !== undefined){}""", """  if (pinv[0] !== undefined){}""") if False else None

rep("""  walk.keys[e.code] = true;
  if (state.mode === 'walk' && ['Space','KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(e.code) >= 0) e.preventDefault();""",
"""  if (fineMode && held >= 0 && ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(e.code) >= 0){
    e.preventDefault();                 /* стрелки двигают вещь, а не игрока */
    moveHeldFine(e.code);
    return;
  }
  if (e.code === 'KeyP'){
    if (held < 0 || !inv[held]){ toast('Сначала возьми предмет (СКМ)'); return; }
    fineMode = !fineMode;
    toast(fineMode
      ? '🎯 Подгонка: ↑↓ — вверх/вниз, ←→ — влево/вправо (по 5 см), ПКМ — поставить на месте, можно сквозь предметы'
      : 'Подгонка выключена — вещь снова ходит за прицелом');
    return;
  }
  walk.keys[e.code] = true;
  if (state.mode === 'walk' && ['Space','KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(e.code) >= 0) e.preventDefault();""")

rep("""    if (e.key==='ArrowRight') applyStage(clamp(state.stage+1,0,5));
    if (e.key==='ArrowLeft') applyStage(clamp(state.stage-1,0,5));""",
"""    if (e.key==='ArrowRight' && !(fineMode && held >= 0)) applyStage(clamp(state.stage+1,0,5));
    if (e.key==='ArrowLeft' && !(fineMode && held >= 0)) applyStage(clamp(state.stage-1,0,5));""")

rep("""function placeHeld(nx, ny){
  if (held < 0 || !inv[held]){ toast('Сначала выбери вещь в слотах (1–9)'); return; }
  var p = aimTarget(nx, ny);""",
"""/* точная подгонка: двигаем вещь стрелками по 5 см */
function moveHeldFine(code){
  if (held < 0 || !inv[held]) return;
  var g = inv[held].g, st = 0.05;
  if (code === 'ArrowUp'){ g.position.y += st; }
  else if (code === 'ArrowDown'){ g.position.y -= st; }
  else {
    var f = new THREE.Vector3(-Math.sin(walk.yaw), 0, -Math.cos(walk.yaw));
    var r = new THREE.Vector3(-f.z, 0, f.x);
    var d = (code === 'ArrowRight') ? 1 : -1;
    g.position.x += r.x * st * d;
    g.position.z += r.z * st * d;
    var cc = g.userData.cc || [g.position.x, g.position.z];
    g.userData.cc = [cc[0] + r.x * st * d, cc[1] + r.z * st * d];
  }
  g.visible = true;
  paint();
}
function placeHeld(nx, ny){
  if (held < 0 || !inv[held]){ toast('Сначала выбери вещь в слотах (1–9)'); return; }
  if (fineMode){
    var itF = inv[held], ccF = itF.g.userData.cc || [itF.g.position.x, itF.g.position.z];
    fineMode = false;
    commitPlace(itF, ccF[0], ccF[1]);      /* ставим где стоит — без проверок, сквозь предметы */
    return;
  }
  var p = aimTarget(nx, ny);""")

rep("  if (held >= 0 && state.mode === 'walk') updateHeldPreview(false);",
    "  if (held >= 0 && state.mode === 'walk' && !fineMode) updateHeldPreview(false);")

rep("    txt = '[ПКМ] поставить · [R] поворот · [1-9] слоты';",
    "    txt = fineMode\n      ? '🎯 Стрелки — сдвинуть по чуть-чуть · ПКМ — поставить · P — выйти из подгонки'\n      : '[ПКМ] поставить · [R] поворот · P — точная подгонка · [1-9] слоты';")

rep("· 1–9 слоты · R — поворот · J — полёт",
    "· 1–9 слоты · R — поворот · P — подгонка · J — полёт")

# выход из подгонки при взятии нового предмета
rep("""  inv.push({ g:g, name:g.userData.pick.name, icon:g.userData.pick.icon });
  held = inv.length - 1;""",
"""  inv.push({ g:g, name:g.userData.pick.name, icon:g.userData.pick.icon });
  held = inv.length - 1;
  fineMode = false;""")

p.write_text(s, encoding='utf-8')
print('O7 ok')
