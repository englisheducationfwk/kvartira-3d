"""M2: мышь как в игре — ЛКМ активация, СКМ взять, ПКМ поставить; инвентарь как
в MY VISION (9 слотов, номер, эмодзи, подсветка, подсказка, тост); старт сразу
в игре (walk); в отметки — место и откуда смотрел."""
import pathlib

p = pathlib.Path('_tools/template.html')
s = p.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global s
    assert old in s, 'NOT FOUND: ' + old[:140]
    s = s.replace(old, new, count)


# ---------- 1) CSS инвентаря — как в MY VISION ----------
rep(""".slot{border:1.5px solid rgba(255,255,255,.25);background:rgba(255,255,255,.08);border-radius:8px;""",
    """#invBar{position:absolute;left:50%;bottom:16px;transform:translateX(-50%);display:flex;gap:6px;z-index:29;}
#invBar .s{width:54px;height:54px;border:1.5px solid rgba(79,217,255,.28);border-radius:10px;background:rgba(8,14,24,.72);
  display:flex;align-items:center;justify-content:center;position:relative;cursor:pointer;padding:0;}
#invBar .s.on{border-color:#4fd9ff;box-shadow:0 0 0 1px rgba(79,217,255,.4),0 0 16px rgba(79,217,255,.25);}
#invBar .s .e{font-size:22px;line-height:1;pointer-events:none;}
#invBar .s .n{position:absolute;top:1px;left:5px;font-size:9px;color:#7e93ab;font-family:monospace;}
#invHint{position:absolute;left:50%;bottom:78px;transform:translateX(-50%);color:#4fd9ff;font-size:12px;
  background:rgba(8,14,24,.78);border:1px solid rgba(79,217,255,.25);border-radius:9px;padding:3px 12px;
  z-index:29;opacity:0;transition:opacity .15s;pointer-events:none;letter-spacing:.4px;white-space:nowrap;}
#invHint.on{opacity:1;}
.slot{border:1.5px solid rgba(255,255,255,.25);background:rgba(255,255,255,.08);border-radius:8px;""")

# ---------- 2) разметка: фиксированные 9 слотов + подсказка ----------
rep("""        <div class="bigplay hidden" id="bigplay"><div>🎮 Войти в квартиру — WASD + мышь</div></div>""",
    """        <div class="bigplay hidden" id="bigplay"><div>🎮 Войти в квартиру — клик, затем WASD + мышь</div></div>
        <div id="invHint"></div>""")

# ---------- 3) invRender как в MY VISION ----------
rep("""function invRender(){
  var bar = $('#invBar');
  bar.innerHTML = '';
  bar.classList.toggle('hidden', inv.length === 0);
  if (!inv.length) return;
  inv.forEach(function(it, i){
    var b = document.createElement('button');
    b.className = 'slot' + (i === held ? ' on' : '');
    b.title = it.name + ' · клавиша ' + (i+1);
    b.innerHTML = '<i>' + it.icon + '</i><span>' + it.name + '</span>';
    b.addEventListener('click', function(){ invSelect(i); });
    bar.appendChild(b);
  });
  if (held >= 0 && inv[held]){
    var tip = document.createElement('div'); tip.className = 'slot tip';
    tip.textContent = (state.mode === 'walk' ? 'ПКМ — поставить' : 'клик по полу — поставить') + ' · R — повернуть';
    bar.appendChild(tip);
  }
}""",
    """function invRender(){
  var bar = $('#invBar');
  if (!bar.children.length){
    for (var i = 0; i < 9; i++){
      (function(i){
        var b = document.createElement('button');
        b.className = 's';
        b.innerHTML = '<span class="n">' + (i+1) + '</span><span class="e"></span>';
        b.addEventListener('click', function(){ invSelect(i); });
        bar.appendChild(b);
      })(i);
    }
  }
  for (var j = 0; j < 9; j++){
    var el = bar.children[j];
    var it = inv[j];
    el.classList.toggle('on', j === held);
    el.querySelector('.e').textContent = it ? it.icon : '';
    el.title = it ? (it.name + ' · клавиша ' + (j+1)) : '';
  }
}
/* подсказка как в MY VISION: что под прицелом и что нажать */
function invHintTick(){
  var el = $('#invHint');
  if (!el || state.mode !== 'walk'){ if (el) el.classList.remove('on'); return; }
  var txt = null;
  if (held >= 0 && inv[held]){
    txt = '[ПКМ] поставить · [R] поворот · [1-9] слоты';
  } else {
    var d = doorUnder(0, 0);
    if (d){
      if (d.kind === 'sofa') txt = '[ЛКМ] разложить/сложить диван';
      else if (d.kind === 'hinge') txt = '[ЛКМ] открыть: ' + (d.name || 'шкафчик');
      else if (d.kind === 'tap') txt = '[ЛКМ] ' + (d.sub === 'switch' ? 'свет' : (d.sub === 'tub' ? 'налить ванну' : (d.sub === 'shower' ? 'душ' : 'вода')));
      else txt = '[ЛКМ] открыть дверь';
    } else {
      var g = itemUnder(0, 0);
      if (g && g.userData.pick) txt = '[СКМ] взять: ' + g.userData.pick.icon + ' ' + g.userData.pick.name;
    }
  }
  if (txt){ el.textContent = txt; el.classList.add('on'); } else el.classList.remove('on');
}""")

# ---------- 4) мышь: ЛКМ активация, СКМ взять, ПКМ поставить ----------
rep("""canvas.addEventListener('mousedown', function(e){
  if (state.mode !== 'walk' || !walk.locked) return;
  if (state.bugmode){
    updateBugAim();
    if (e.button === 0 && bugAim.last) openBugDlg(bugAim.last);
    return;
  }
  if (e.button === 0){
    var d = doorUnder(0, 0);
    if (d && held < 0){ useThing(d); return; }
    var g = itemUnder(0, 0);
    if (g) pickUp(g);
  } else if (e.button === 2){
    var d2 = doorUnder(0, 0);
    if (d2){ useThing(d2); return; }
    placeHeld(0, 0);
  }
});""",
    """canvas.addEventListener('mousedown', function(e){
  if (state.mode !== 'walk' || !walk.locked){
    /* обзор: СКМ — взять, ПКМ — поставить */
    if (state.mode === 'orbit'){
      if (e.button === 1){ e.preventDefault(); var go = itemUnder(ndc.x, ndc.y); if (go) pickUp(go); }
      else if (e.button === 2){ placeHeld(ndc.x, ndc.y); }
    }
    return;
  }
  if (state.bugmode){
    updateBugAim();
    if (e.button === 0 && bugAim.last) openBugDlg(bugAim.last);
    return;
  }
  if (e.button === 0){                  /* ЛКМ — активация: дверь, ящик, кран, выключатель */
    var d = doorUnder(0, 0);
    if (d) useThing(d);
  } else if (e.button === 1){           /* СКМ — взять предмет */
    e.preventDefault();
    var g = itemUnder(0, 0);
    if (g) pickUp(g);
  } else if (e.button === 2){           /* ПКМ — поставить */
    placeHeld(0, 0);
  }
});
canvas.addEventListener('auxclick', function(e){ if (e.button === 1) e.preventDefault(); });""")
rep("""  var d = doorUnder(ndc.x, ndc.y);
  if (d && held < 0){ useThing(d); return; }
  if (held >= 0){ placeHeld(ndc.x, ndc.y); return; }
  var g = itemUnder(ndc.x, ndc.y);
  if (g) pickUp(g);
});""",
    """  var d = doorUnder(ndc.x, ndc.y);
  if (d) useThing(d);
});""")

# ---------- 5) тик: подсказка инвентаря ----------
rep("""  doorTick(dt);
  bugAim.cnt++;""",
    """  doorTick(dt);
  if (state.mode === 'walk' && (++bugAim.cnt % 6 === 0)) invHintTick();
  bugAim.cnt++;""")

# ---------- 6) старт сразу в игре ----------
rep("""var state = { stage:0, mode:'orbit', mirror:false,""",
    """var state = { stage:0, mode:'walk', mirror:false,""")
rep("""try { var saved = JSON.parse(localStorage.getItem(LS)||'{}'); for (var k in saved) if (k in state) state[k]=saved[k]; } catch(e){}""",
    """try { var saved = JSON.parse(localStorage.getItem(LS)||'{}'); for (var k in saved) if (k in state) state[k]=saved[k]; } catch(e){}
state.mode = 'walk';   /* грузимся сразу в игру, обзор — по V */""")

# ---------- 7) отметки: место и откуда смотрел ----------
rep("""function saveBug(){
  var t = bugAim.last;
  var note = $('#bugText').value.trim();
  if (!t || !note){ toast('Напиши пару слов, что не так'); return; }
  var e = { n: t.name, x: +t.pt.x.toFixed(3), y: +t.pt.y.toFixed(3), z: +t.pt.z.toFixed(3),
            note: note, t: new Date().toLocaleString('ru-RU'), mirror: state.mirror };""",
    """function flatPlace(x, z){
  if (x > K.x0 && x < K.x1 && z < 0) return 'эркер';
  if (x > K.x0 && x < K.x1 && z >= 0 && z < K.z1) return 'кухня';
  if (x > P.room.x0 && x < P.room.x1 && z > P.room.z0 && z < P.room.z1) return 'комната';
  if (x > P.room.x0 && x < P.room.x1 && z < 0) return 'лоджия';
  if (x > BA.x0 && x < BA.x1 && z > BA.z0 && z < BA.z1) return 'санузел';
  if (x > HA.x0 && x < HA.x1 && z > HA.z0) return 'коридор';
  if (x > HA.x0 && x < BA.x1 && z >= BA.z1) return 'коридор у входа';
  if (z > P.room.z1 + P.LOAD) return 'площадка';
  return 'вне квартиры';
}
function saveBug(){
  var t = bugAim.last;
  var note = $('#bugText').value.trim();
  if (!t || !note){ toast('Напиши пару слов, что не так'); return; }
  var eye = (state.mode === 'walk') ? [walk.pos.x, walk.pos.y + 1.62, walk.pos.z] : [camera.position.x, camera.position.y, camera.position.z];
  var e = { n: t.name, x: +t.pt.x.toFixed(3), y: +t.pt.y.toFixed(3), z: +t.pt.z.toFixed(3),
            note: note, t: new Date().toLocaleString('ru-RU'), mirror: state.mirror,
            place: flatPlace(t.pt.x, t.pt.z),
            from: [+eye[0].toFixed(2), +eye[1].toFixed(2), +eye[2].toFixed(2)],
            look: [+walk.yaw.toFixed(2), +walk.pitch.toFixed(2)] };""")

# ---------- 8) строка подсказки управления снизу ----------
rep("""  $('#hint').textContent = walking""",
    """  $('#hint').textContent = walking""")
p.write_text(s, encoding='utf-8')
print('M2 ok')
