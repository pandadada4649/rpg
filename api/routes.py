from flask import Blueprint, request, jsonify, session
from game.player import Player
from game.party import Party
from game.enemy import create_enemy, AREA_ENEMIES, AREA_BOSSES
from game.quest import get_all_quests, get_quest
from game.save import save_game, load_game
import random

bp = Blueprint("api", __name__, url_prefix="/api")

def save_session(party):
    members = []
    for m in party.members:
        members.append({
            "name":         m.name,
            "player_class": m.player_class,
            "level":        m.level,
            "exp":          m.exp,
            "exp_to_next":  m.exp_to_next,
            "hp":           m.hp,
            "max_hp":       m.max_hp,
            "mp":           m.mp,
            "max_mp":       m.max_mp,
            "attack":       m.attack,
            "defense":      m.defense,
            "speed":        m.speed,
            "gold":         m.gold,
            "inventory":    m.inventory,
            "equipment":    m.equipment,
            "skills":       m.skills,
            "boss_cleared": m.boss_cleared,
        })
    session["party"] = members

def load_session():
    members_data = session.get("party")
    if not members_data:
        return None
    members = []
    for data in members_data:
        p = Player(data["name"], data["player_class"])
        p.load_from_data(data)
        members.append(p)
    party = Party(members[0])
    party.members = members
    return party

def update_quest_progress(enemy_name):
    quests     = session.get("quests", {})
    completed  = session.get("completed_quests", [])
    quest_logs = []

    for qid, progress in quests.items():
        if progress["done"]:
            continue
        quest = get_quest(qid)
        if not quest:
            continue
        if quest["target"] == enemy_name:
            progress["count"] += 1
            remaining = quest["count"] - progress["count"]
            if remaining > 0:
                quest_logs.append(f"📋 クエスト「{quest['title']}」進捗: {progress['count']}/{quest['count']}")
            if progress["count"] >= quest["count"]:
                progress["done"] = True
                quest_logs.append(f"✨ クエスト「{quest['title']}」達成！報告で報酬がもらえる！")

    session["quests"]    = quests
    return quest_logs

@bp.route("/start", methods=["POST"])
def start():
    data         = request.json
    name         = data.get("name", "勇者")
    player_class = data.get("player_class", "戦士")
    hero  = Player(name, player_class)
    party = Party(hero)
    save_session(party)
    session["quests"]           = {}
    session["completed_quests"] = []
    session["bestiary"]         = {}
    return jsonify({"message": f"🌬️ {name}の冒険が始まった！", "party": session["party"]})

@bp.route("/status", methods=["GET"])
def status():
    party = load_session()
    if not party:
        return jsonify({"error": "ゲームが開始されていません"}), 400
    return jsonify({"party": session["party"]})

@bp.route("/battle/start", methods=["POST"])
def battle_start():
    party = load_session()
    if not party:
        return jsonify({"error": "ゲームが開始されていません"}), 400

    data     = request.json or {}
    area     = data.get("area", "grassland")
    boss_key = data.get("boss")

    if boss_key and boss_key in AREA_BOSSES:
        enemy_type = AREA_BOSSES[boss_key]
    elif area in AREA_ENEMIES:
        enemy_type = random.choice(AREA_ENEMIES[area])
    else:
        enemy_type = "スライム"

    enemy = create_enemy(enemy_type)
    session["enemy"] = {
        "name":    enemy.name,
        "hp":      enemy.hp,
        "max_hp":  enemy.max_hp,
        "attack":  enemy.attack,
        "defense": enemy.defense,
        "exp":     enemy.exp,
        "gold":    enemy.gold,
        "is_boss": enemy.is_boss,
    }
    return jsonify({
        "message": f"{'⚠️ ボス' if enemy.is_boss else '⚔️'} {enemy.name}があらわれた！",
        "enemy":   session["enemy"],
        "party":   session["party"],
    })

@bp.route("/battle/action", methods=["POST"])
def battle_action():
    party = load_session()
    if not party:
        return jsonify({"error": "ゲームが開始されていません"}), 400

    enemy_data = session.get("enemy")
    if not enemy_data:
        return jsonify({"error": "戦闘中ではありません"}), 400

    enemy    = create_enemy(enemy_data["name"])
    enemy.hp = enemy_data["hp"]

    data   = request.json
    action = data.get("action")
    logs   = []
    player = party.members[0]

    if action == "attack":
        damage = max(1, player.attack - enemy.defense)
        enemy.hp = max(0, enemy.hp - damage)
        logs.append(f"✅ {player.name}の攻撃！ {enemy.name}に {damage} ダメージ！")

    elif action == "skill":
        skill_name = data.get("skill")
        if skill_name in player.skills:
            old_hp = enemy.hp
            player.use_skill(skill_name, enemy)
            damage = old_hp - enemy.hp
            logs.append(f"🔮 {skill_name}！ {enemy.name}に {damage} ダメージ！")
        else:
            logs.append("そのスキルは使えない！")

    elif action == "item":
        item_name = data.get("item")
        player.use_item(item_name)
        logs.append(f"💊 {item_name}を使った！")

    elif action == "run":
        session.pop("enemy", None)
        save_session(party)
        return jsonify({"message": "🏃 逃げ出した！", "battle_end": True, "party": session["party"]})

    if enemy.hp > 0:
        action_type = enemy.choose_action()
        if action_type == "attack":
            dmg = max(1, enemy.attack - player.defense)
            player.hp = max(0, player.hp - dmg)
            logs.append(f"💥 {enemy.name}の攻撃！ {player.name}に {dmg} ダメージ！")
        else:
            dmg = max(1, enemy.attack * 2 - player.defense)
            player.hp = max(0, player.hp - dmg)
            logs.append(f"💥 {enemy.name}の強攻撃！ {player.name}に {dmg} ダメージ！")

    battle_end = False
    if enemy.hp <= 0:
        party.members[0].gain_exp(enemy_data["exp"])
        party.members[0].gold += enemy_data["gold"]
        logs.append(f"🎉 {enemy.name}を倒した！ {enemy_data['exp']}EXP・{enemy_data['gold']}G獲得！")
        if enemy_data.get("is_boss"):
            logs.append("🏆 ボスを撃破！")
            party.members[0].boss_cleared = True

        # 魔物図鑑
        bestiary = session.get("bestiary", {})
        bestiary[enemy_data["name"]] = bestiary.get(enemy_data["name"], 0) + 1
        session["bestiary"] = bestiary

        # クエスト進捗
        quest_logs = update_quest_progress(enemy_data["name"])
        logs.extend(quest_logs)

        session.pop("enemy", None)
        battle_end = True
    elif not player.is_alive:
        logs.append(f"💀 {player.name}は倒れた...")
        session.pop("enemy", None)
        battle_end = True
    else:
        session["enemy"]["hp"] = enemy.hp

    save_session(party)
    return jsonify({
        "logs":       logs,
        "party":      session["party"],
        "enemy":      session.get("enemy"),
        "battle_end": battle_end,
    })

@bp.route("/inn", methods=["POST"])
def inn():
    party = load_session()
    if not party:
        return jsonify({"error": "ゲームが開始されていません"}), 400
    leader = party.members[0]
    if leader.gold < 10:
        return jsonify({"message": "💰 ゴールドが足りない！（10G必要）"})
    leader.gold -= 10
    for m in party.members:
        m.hp = m.max_hp
        m.mp = m.max_mp
    save_session(party)
    return jsonify({"message": "💤 HP・MPが全回復！", "party": session["party"]})

@bp.route("/quests", methods=["GET"])
def quests():
    all_quests   = get_all_quests()
    active       = session.get("quests", {})
    completed    = session.get("completed_quests", [])
    result = []
    for q in all_quests:
        qid      = q["id"]
        progress = active.get(qid, {})
        result.append({
            **q,
            "status":   "completed" if qid in completed else "active" if qid in active else "available",
            "progress": progress.get("count", 0),
        })
    return jsonify({"quests": result})

@bp.route("/quests/accept", methods=["POST"])
def accept_quest():
    qid   = request.json.get("quest_id")
    quest = get_quest(qid)
    if not quest:
        return jsonify({"error": "クエストが見つかりません"}), 400
    quests = session.get("quests", {})
    if qid in quests:
        return jsonify({"message": "すでに受注済みです"})
    quests[qid] = {"count": 0, "done": False}
    session["quests"] = quests
    return jsonify({"message": f"📋 クエスト「{quest['title']}」を受注した！"})

@bp.route("/quests/complete", methods=["POST"])
def complete_quest():
    party = load_session()
    if not party:
        return jsonify({"error": "ゲームが開始されていません"}), 400
    qid      = request.json.get("quest_id")
    quest    = get_quest(qid)
    quests   = session.get("quests", {})
    completed = session.get("completed_quests", [])

    if not quest or qid not in quests:
        return jsonify({"error": "クエストを受注していません"}), 400
    if not quests[qid]["done"]:
        return jsonify({"error": "まだ達成していません"}), 400
    if qid in completed:
        return jsonify({"message": "すでに報告済みです"})

    party.members[0].gain_exp(quest["reward_exp"])
    party.members[0].gold += quest["reward_gold"]
    completed.append(qid)
    session["completed_quests"] = completed
    save_session(party)
    return jsonify({
        "message": f"🎊 クエスト「{quest['title']}」完了！ {quest['reward_exp']}EXP・{quest['reward_gold']}G獲得！",
        "party":   session["party"],
    })

@bp.route("/bestiary", methods=["GET"])
def bestiary():
    return jsonify({"bestiary": session.get("bestiary", {})})

@bp.route("/save", methods=["POST"])
def save():
    party = load_session()
    if not party:
        return jsonify({"error": "ゲームが開始されていません"}), 400
    try:
        save_game(party.members[0])
        return jsonify({"message": "💾 クラウドにセーブしました！"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/load", methods=["POST"])
def load():
    name = request.json.get("name")
    if not name:
        return jsonify({"error": "名前を入力してください"}), 400
    try:
        data = load_game(name)
        if not data:
            return jsonify({"error": "セーブデータが見つかりません"}), 404
        hero = Player(data["name"], data["player_class"])
        hero.load_from_data(data)
        party = Party(hero)
        save_session(party)
        return jsonify({"message": f"📂 {name}のデータをロードしました！", "party": session["party"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/forge/upgrade", methods=["POST"])
def forge_upgrade():
    party = load_session()
    if not party:
        return jsonify({"error": "ゲームが開始されていません"}), 400
    leader = party.members[0]
    cost   = 100
    if leader.gold < cost:
        return jsonify({"message": f"💰 ゴールドが足りない！（{cost}G必要）"})
    leader.gold   -= cost
    leader.attack += 3
    save_session(party)
    return jsonify({
        "message": f"🔨 武器を強化した！ ATK+3（コスト{cost}G）",
        "party":   session["party"],
    })

@bp.route("/forge/armor", methods=["POST"])
def forge_armor():
    party = load_session()
    if not party:
        return jsonify({"error": "ゲームが開始されていません"}), 400
    leader = party.members[0]
    cost   = 100
    if leader.gold < cost:
        return jsonify({"message": f"💰 ゴールドが足りない！（{cost}G必要）"})
    leader.gold    -= cost
    leader.defense += 2
    save_session(party)
    return jsonify({
        "message": f"🛡️ 防具を強化した！ DEF+2（コスト{cost}G）",
        "party":   session["party"],
    })