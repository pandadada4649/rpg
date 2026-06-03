const $ = id => document.getElementById(id);

const log = (msg) => {
  const box = $("log-box");
  const p   = document.createElement("p");
  p.textContent = msg;
  box.appendChild(p);
  box.scrollTop = box.scrollHeight;
};

const clearLog = () => { $("log-box").innerHTML = ""; };

const updateStatus = (party) => {
  const p     = party[0];
  const hpPct = Math.max(0, (p.hp / p.max_hp) * 100);
  const mpPct = Math.max(0, (p.mp / p.max_mp) * 100);
  $("s-name").textContent   = `${p.name}（${p.player_class} Lv.${p.level}）`;
  $("s-hp-txt").textContent = `${p.hp}/${p.max_hp}`;
  $("s-mp-txt").textContent = `${p.mp}/${p.max_mp}`;
  $("s-hp-bar").style.width = hpPct + "%";
  $("s-mp-bar").style.width = mpPct + "%";
  $("s-atk").textContent    = p.attack;
  $("s-def").textContent    = p.defense;
  $("s-exp").textContent    = `${p.exp}/${p.exp_to_next}`;
  $("s-gold").textContent   = `💰 ${p.gold} G`;
};

const updateEnemy = (enemy) => {
  if (!enemy) { $("enemy-box").style.display = "none"; return; }
  $("enemy-box").style.display = "block";
  $("e-name").textContent      = enemy.is_boss ? `👑 ${enemy.name}` : enemy.name;
  $("e-hp-txt").textContent    = `${enemy.hp}/${enemy.max_hp}`;
  const pct = Math.max(0, (enemy.hp / enemy.max_hp) * 100);
  $("e-hp-bar").style.width    = pct + "%";
  $("e-hp-bar").style.background = enemy.is_boss
    ? "linear-gradient(90deg, #800080, #cc00cc)"
    : "linear-gradient(90deg, #c03030, #e05555)";
};

const shakeStatus = () => {
  const box = $("status-box");
  box.classList.remove("shake");
  void box.offsetWidth;
  box.classList.add("shake");
};

const showTown = () => {
  $("town-buttons").style.display   = "block";
  $("action-buttons").style.display = "none";
  $("skill-buttons").style.display  = "none";
  $("map-screen").style.display     = "none";
  updateEnemy(null);
};

const showBattle = () => {
  $("town-buttons").style.display   = "none";
  $("action-buttons").style.display = "block";
  $("skill-buttons").style.display  = "none";
  $("map-screen").style.display     = "none";
};

$("start-btn").addEventListener("click", async () => {
  const name         = $("hero-name").value.trim() || "旅人";
  const player_class = $("hero-class").value;
  const res  = await fetch("/api/start", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ name, player_class }),
  });
  const data = await res.json();
  clearLog();
  log(data.message);
  updateStatus(data.party);
  $("start-screen").style.display = "none";
  $("game-screen").style.display  = "block";
  showTown();
});

const startBattle = async (area = "grassland", boss = null) => {
  exitMap();
  const body = { area };
  if (boss) body.boss = boss;
  const res  = await fetch("/api/battle/start", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body),
  });
  const data = await res.json();
  clearLog();
  log(data.message);
  updateStatus(data.party);
  updateEnemy(data.enemy);
  showBattle();
};

const doAction = async (action, extra = null) => {
  const body = { action };
  if (action === "skill") body.skill = extra;
  if (action === "item")  body.item  = extra;
  const res  = await fetch("/api/battle/action", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (data.error) { log("⚠️ " + data.error); return; }
  if (data.logs)  data.logs.forEach(l => {
    log(l);
    if (l.includes("ダメージ") && l.includes(data.party?.[0]?.name)) shakeStatus();
  });
  updateStatus(data.party);
  updateEnemy(data.enemy);
  if (data.battle_end) setTimeout(() => showTown(), 800);
};

const showSkills = () => {
  fetch("/api/status").then(r => r.json()).then(data => {
    const skills = data.party[0].skills;
    const box    = $("skill-buttons");
    box.innerHTML = "";
    skills.forEach(skill => {
      const btn = document.createElement("button");
      btn.textContent = skill;
      btn.onclick = () => {
        doAction("skill", skill);
        box.style.display = "none";
        $("action-buttons").style.display = "block";
      };
      box.appendChild(btn);
    });
    const back = document.createElement("button");
    back.textContent = "← もどる";
    back.onclick = () => {
      box.style.display = "none";
      $("action-buttons").style.display = "block";
    };
    box.appendChild(back);
    $("action-buttons").style.display = "none";
    box.style.display = "flex";
  });
};

const saveGame = async () => {
  const res  = await fetch("/api/save", { method: "POST" });
  const data = await res.json();
  log(data.message || data.error);
};

const useInn = async () => {
  const res  = await fetch("/api/inn", { method: "POST" });
  const data = await res.json();
  log(data.message);
  if (data.party) updateStatus(data.party);
};

// ── フィールドマップ ──────────────────────────────────
const TILE = 32;

// エリア定義
const AREAS = {
  grassland: {
    name: "🌿 草原エリア",
    cols: 16, rows: 12,
    bgColor: "#1a2e1a",
    enemies: "grassland",
    map: [
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
      [1,0,0,4,0,0,0,0,0,0,0,6,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,3,3,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,3,3,0,0,0,0,0,0,0,0,7,0,0,1],
      [1,0,0,0,0,0,0,0,5,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
  },
  forest: {
    name: "🌲 深い森エリア",
    cols: 16, rows: 12,
    bgColor: "#0d1a0d",
    enemies: "forest",
    map: [
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1],
      [1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1],
      [1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,8,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,7,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
  },
  desert: {
    name: "🏜️ 砂漠エリア",
    cols: 16, rows: 12,
    bgColor: "#2a1e0d",
    enemies: "desert",
    map: [
      [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,3,3,0,0,0,0,0,0,0,0,2],
      [2,0,0,4,0,3,3,0,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,2,2,0,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,8,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,7,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    ],
  },
  snow: {
    name: "❄️ 雪山エリア",
    cols: 16, rows: 12,
    bgColor: "#0d1a2a",
    enemies: "snow",
    map: [
      [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,0,0,4,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,2,2,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,2,2,2,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,9,0,0,0,0,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,7,0,0,2],
      [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
      [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    ],
  },
};

// タイル定義
// 0=草/砂, 1=森/壁, 2=山/岩, 3=水, 4=町, 5=ダンジョン
// 6=森エリアへ, 7=次エリアへ, 8=中ボス, 9=ラスボス
const TILE_COLORS = {
  0: "#3a5c3a",
  1: "#1a3a1a",
  2: "#6a5a4a",
  3: "#2a4a7a",
  4: "#8a6a3a",
  5: "#4a2a6a",
  6: "#2a5a2a",
  7: "#5a3a7a",
  8: "#7a1a1a",
  9: "#4a0a4a",
};

const TILE_ICONS = {
  4: "🏘", 5: "🏚", 6: "🌲",
  7: "🚪", 8: "💀", 9: "👑",
};

let playerPos  = { x: 4, y: 4 };
let currentArea = "grassland";
let mapLoopId  = null;
let keys       = {};
let stepCount  = 0;
let lastKey    = {};

const getArea = () => AREAS[currentArea];

const drawMap = () => {
  const area   = getArea();
  const canvas = $("map-canvas");
  canvas.width  = area.cols * TILE;
  canvas.height = area.rows * TILE;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let row = 0; row < area.rows; row++) {
    for (let col = 0; col < area.cols; col++) {
      const tile = area.map[row][col];
      ctx.fillStyle = TILE_COLORS[tile] || "#3a5c3a";
      ctx.fillRect(col * TILE, row * TILE, TILE, TILE);
      ctx.strokeStyle = "#00000033";
      ctx.strokeRect(col * TILE, row * TILE, TILE, TILE);
      if (TILE_ICONS[tile]) {
        ctx.font = "18px serif";
        ctx.textAlign = "center";
        ctx.fillText(TILE_ICONS[tile], col * TILE + TILE/2, row * TILE + TILE/1.4);
      }
    }
  }

  // エリア名表示
  ctx.fillStyle = "#ffffff99";
  ctx.font = "12px sans-serif";
  ctx.textAlign = "left";
  ctx.fillText(area.name, 8, 16);

  // プレイヤー
  const px = playerPos.x * TILE + TILE/2;
  const py = playerPos.y * TILE + TILE/2;
  ctx.beginPath();
  ctx.arc(px, py, TILE/2.8, 0, Math.PI * 2);
  ctx.fillStyle = "#7eb8d4";
  ctx.fill();
  ctx.strokeStyle = "#ffffff88";
  ctx.lineWidth = 2;
  ctx.stroke();
  ctx.font = "16px serif";
  ctx.textAlign = "center";
  ctx.fillText("🧍", px, py + 6);
};

const movePlayer = () => {
  let moved = false;
  let nx = playerPos.x;
  let ny = playerPos.y;

  if      (keys["ArrowUp"]    || keys["w"] || keys["W"]) { ny--; moved = true; }
  else if (keys["ArrowDown"]  || keys["s"] || keys["S"]) { ny++; moved = true; }
  else if (keys["ArrowLeft"]  || keys["a"] || keys["A"]) { nx--; moved = true; }
  else if (keys["ArrowRight"] || keys["d"] || keys["D"]) { nx++; moved = true; }

  if (!moved) return;

  const keyStr = `${nx},${ny}`;
  if (lastKey.pos === keyStr) return;
  lastKey.pos = keyStr;
  setTimeout(() => { lastKey.pos = null; }, 180);

  const area = getArea();
  if (nx < 0 || nx >= area.cols || ny < 0 || ny >= area.rows) return;
  const tile = area.map[ny][nx];
  if (tile === 1 || tile === 2 || tile === 3) return;

  playerPos.x = nx;
  playerPos.y = ny;
  stepCount++;

  // タイルイベント
  if (tile === 4) {
    log("🏘️ 町に入った！");
    exitMap();
    return;
  }
  if (tile === 5) {
    log("🏚️ ダンジョンの入口だ！");
    exitMap();
    startBattle(area.enemies);
    return;
  }
  if (tile === 6) {
    log("🌲 深い森エリアへ入った！");
    currentArea = "forest";
    playerPos = { x: 4, y: 4 };
    stepCount = 0;
    return;
  }
  if (tile === 7) {
    const next = { grassland: "forest", forest: "desert", desert: "snow", snow: "grassland" };
    currentArea = next[currentArea] || "grassland";
    playerPos = { x: 4, y: 4 };
    stepCount = 0;
    log(`✨ ${getArea().name}へ移動した！`);
    return;
  }
  if (tile === 8) {
    const bosses = { forest: "forest_boss", desert: "desert_boss", snow: "snow_boss" };
    const bossKey = bosses[currentArea];
    if (bossKey) {
      log("💀 中ボスが立ちはだかる！");
      exitMap();
      startBattle(area.enemies, bossKey);
    }
    return;
  }
  if (tile === 9) {
    log("👑 ラスボス：魔王ゾルダンが現れた！");
    exitMap();
    startBattle(area.enemies, "last_boss");
    return;
  }

  // ランダムエンカウント
  if (tile === 0 && stepCount >= 5 && Math.random() < 0.10) {
    stepCount = 0;
    log("⚔️ 魔物があらわれた！");
    exitMap();
    startBattle(area.enemies);
  }
};

const mapLoop = () => {
  movePlayer();
  drawMap();
};

const enterMap = () => {
  $("town-buttons").style.display = "none";
  $("map-screen").style.display   = "block";
  drawMap();
  if (mapLoopId) return;
  mapLoopId = setInterval(mapLoop, 150);
};

const resetMap = () => {
  playerPos   = { x: 4, y: 4 };
  currentArea = "grassland";
  stepCount   = 0;
};

const exitMap = () => {
  stopMapLoop();
  $("map-screen").style.display   = "none";
  $("town-buttons").style.display = "block";
};

const stopMapLoop = () => {
  if (mapLoopId) { clearInterval(mapLoopId); mapLoopId = null; }
};

document.addEventListener("keydown", e => {
  keys[e.key] = true;
  if (["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].includes(e.key)) e.preventDefault();
  if (e.key === "Escape") exitMap();
});
document.addEventListener("keyup", e => { keys[e.key] = false; });
// ── クエスト ──────────────────────────────────────────
const showQuests = async () => {
  const res  = await fetch("/api/quests");
  const data = await res.json();
  const panel = $("sub-panel");
  panel.style.display = "block";

  let html = `<div class="panel-title">📋 QUEST BOARD</div>`;
  data.quests.forEach(q => {
    const isDone      = q.status === "completed";
    const isActive    = q.status === "active";
    const isAvailable = q.status === "available";
    const canComplete = isActive && q.progress >= q.count;

    html += `<div style="border:1px solid #2a2a4a;border-radius:8px;padding:10px;margin:6px 0;">`;
    html += `<div style="color:${isDone ? '#55cc88' : isActive ? '#f0c040' : '#dde0f0'};font-weight:bold;">${isDone ? '✅' : isActive ? '🔄' : '📋'} ${q.title}</div>`;
    html += `<div style="font-size:0.82rem;color:#8888aa;margin:4px 0;">${q.desc}</div>`;
    if (isActive) html += `<div style="font-size:0.82rem;color:#f0c040;">進捗: ${q.progress}/${q.count}</div>`;
    html += `<div style="font-size:0.8rem;color:#7eb8d4;">報酬: ${q.reward_exp}EXP・${q.reward_gold}G</div>`;

    if (isAvailable) {
      html += `<button onclick="acceptQuest('${q.id}')" style="margin-top:6px;">受注する</button>`;
    } else if (canComplete) {
      html += `<button onclick="completeQuest('${q.id}')" style="margin-top:6px;color:#55cc88;border-color:#55cc88;">報告する🎊</button>`;
    } else if (isDone) {
      html += `<div style="color:#55cc88;font-size:0.82rem;margin-top:4px;">完了済み</div>`;
    }
    html += `</div>`;
  });

  html += `<button onclick="closeSubPanel()" style="margin-top:8px;">✕ 閉じる</button>`;
  panel.innerHTML = html;
};

const acceptQuest = async (qid) => {
  const res  = await fetch("/api/quests/accept", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ quest_id: qid }),
  });
  const data = await res.json();
  log(data.message);
  showQuests();
};

const completeQuest = async (qid) => {
  const res  = await fetch("/api/quests/complete", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ quest_id: qid }),
  });
  const data = await res.json();
  log(data.message);
  if (data.party) updateStatus(data.party);
  showQuests();
};

// ── 鍛冶屋 ────────────────────────────────────────────
const showForge = async () => {
  const panel = $("sub-panel");
  panel.style.display = "block";
  panel.innerHTML = `
    <div class="panel-title">🔨 FORGE</div>
    <div style="margin:8px 0;font-size:0.88rem;color:#8888aa;">武器や防具を強化できる</div>
    <div style="border:1px solid #2a2a4a;border-radius:8px;padding:10px;margin:6px 0;">
      <div style="color:#f0c040;font-weight:bold;">⚔️ 武器強化</div>
      <div style="font-size:0.82rem;color:#8888aa;margin:4px 0;">ATK+3 コスト: 100G</div>
      <button onclick="forgeUpgrade('weapon')">強化する</button>
    </div>
    <div style="border:1px solid #2a2a4a;border-radius:8px;padding:10px;margin:6px 0;">
      <div style="color:#7eb8d4;font-weight:bold;">🛡️ 防具強化</div>
      <div style="font-size:0.82rem;color:#8888aa;margin:4px 0;">DEF+2 コスト: 100G</div>
      <button onclick="forgeUpgrade('armor')">強化する</button>
    </div>
    <button onclick="closeSubPanel()" style="margin-top:8px;">✕ 閉じる</button>
  `;
};

const forgeUpgrade = async (type) => {
  const url  = type === "weapon" ? "/api/forge/upgrade" : "/api/forge/armor";
  const res  = await fetch(url, { method: "POST" });
  const data = await res.json();
  log(data.message);
  if (data.party) updateStatus(data.party);
};

// ── 魔物図鑑 ──────────────────────────────────────────
const showBestiary = async () => {
  const res   = await fetch("/api/bestiary");
  const data  = await res.json();
  const panel = $("sub-panel");
  panel.style.display = "block";

  const entries = Object.entries(data.bestiary);
  let html = `<div class="panel-title">📖 BESTIARY</div>`;

  if (entries.length === 0) {
    html += `<div style="color:#8888aa;font-size:0.88rem;padding:10px;">まだ魔物を倒していない...</div>`;
  } else {
    entries.forEach(([name, count]) => {
      html += `
        <div style="display:flex;justify-content:space-between;align-items:center;
                    border:1px solid #2a2a4a;border-radius:8px;padding:8px 12px;margin:4px 0;">
          <span>⚔️ ${name}</span>
          <span style="color:#f0c040;">${count}体討伐</span>
        </div>`;
    });
  }

  html += `<button onclick="closeSubPanel()" style="margin-top:8px;">✕ 閉じる</button>`;
  panel.innerHTML = html;
};

// ── サブパネルを閉じる ────────────────────────────────
const closeSubPanel = () => {
  $("sub-panel").style.display = "none";
};
// ── クラウドセーブ・ロード ─────────────────────────────
const cloudSave = async () => {
  const res  = await fetch("/api/save", { method: "POST" });
  const data = await res.json();
  log(data.message || data.error);
};

document.getElementById("load-btn").addEventListener("click", async () => {
  const name = document.getElementById("load-name").value.trim();
  if (!name) { alert("名前を入力してください"); return; }
  const res  = await fetch("/api/load", {
    method:  "POST",
    headers: {"Content-Type": "application/json"},
    body:    JSON.stringify({ name }),
  });
  const data = await res.json();
  if (data.error) { alert(data.error); return; }
  alert(data.message);
  updateStatus(data.party);
  document.getElementById("start-screen").style.display = "none";
  document.getElementById("game-screen").style.display  = "block";
  showTown();
});