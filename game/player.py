# 職業ごとの初期ステータス
CLASS_STATS = {
    "侍":    {"max_hp": 130, "max_mp": 15, "attack": 14, "defense": 8,  "speed": 6,  "skills": ["豪力撃", "盾砕き", "回復術"]},
    "陰陽師": {"max_hp": 70,  "max_mp": 60, "attack": 6,  "defense": 3,  "speed": 8,  "skills": ["火炎斬", "氷結陣", "雷鳴斬", "天魔滅", "回復術"]},
    "忍":    {"max_hp": 100, "max_mp": 20, "attack": 12, "defense": 5,  "speed": 14, "skills": ["掏摸", "急所突き", "回復術"]},
}

# スキルデータ
SKILL_DATA = {
    "火炎斬":   {"cost": 8,  "type": "attack", "power": 2.0,  "desc": "🔥 炎を纏った一撃"},
    "氷結陣":   {"cost": 12, "type": "attack", "power": 2.8,  "desc": "❄️  氷の結界で攻撃"},
    "雷鳴斬":   {"cost": 10, "type": "attack", "power": 2.5,  "desc": "⚡ 雷を帯びた斬撃"},
    "天魔滅":   {"cost": 25, "type": "attack", "power": 4.5,  "desc": "☄️  天より降る滅びの術"},
    "豪力撃":   {"cost": 6,  "type": "attack", "power": 1.8,  "desc": "💪 全力を込めた一撃"},
    "盾砕き":   {"cost": 8,  "type": "attack", "power": 1.5,  "desc": "🛡️  盾ごと叩き砕く"},
    "急所突き": {"cost": 5,  "type": "attack", "power": 2.2,  "desc": "🗡️  急所を狙い撃つ"},
    "掏摸":     {"cost": 4,  "type": "steal",  "power": 1.0,  "desc": "👜 懐から金を盗む"},
    "回復術":   {"cost": 5,  "type": "heal",   "power": 40,   "desc": "✨ 傷を癒す回復術"},
}

class Player:
    def __init__(self, name: str, player_class: str = "侍"):
        self.name         = name
        self.player_class = player_class
        self.level        = 1
        self.exp          = 0
        self.exp_to_next  = 100
        self.boss_cleared = False

        stats = CLASS_STATS[player_class]
        self.max_hp  = stats["max_hp"]
        self.hp      = self.max_hp
        self.max_mp  = stats["max_mp"]
        self.mp      = self.max_mp
        self.attack  = stats["attack"]
        self.defense = stats["defense"]
        self.speed   = stats["speed"]
        self.skills  = stats["skills"][:]

        self.gold      = 50
        self.inventory = {"傷薬": 2, "霊水": 1}
        self.equipment = {"weapon": None, "armor": None}

    def load_from_data(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

    def show_status(self):
        weapon = self.equipment["weapon"] or "なし"
        armor  = self.equipment["armor"]  or "なし"
        print(f"=== {self.name}（{self.player_class} Lv.{self.level}）===")
        print(f"HP : {self.hp}/{self.max_hp}  MP: {self.mp}/{self.max_mp}")
        print(f"攻撃: {self.attack}  防御: {self.defense}  素早さ: {self.speed}")
        print(f"経験値: {self.exp}/{self.exp_to_next}  所持金: {self.gold}両")
        print(f"武器: {weapon}  防具: {armor}")

    def show_inventory(self):
        print("--- 所持品 ---")
        for item, count in self.inventory.items():
            if count > 0:
                print(f"  {item} x{count}")

    def show_skills(self):
        print("--- 術技一覧 ---")
        for i, skill in enumerate(self.skills, 1):
            data = SKILL_DATA.get(skill, {})
            cost = data.get("cost", "?")
            desc = data.get("desc", "")
            print(f"  {i}: {skill}（霊力{cost}）{desc}")

    def equip(self, item_name: str, slot: str):
        self.equipment[slot] = item_name
        if slot == "weapon":
            self.attack += 5
            print(f"⚔️  {item_name}を装備！ 攻撃+5")
        elif slot == "armor":
            self.defense += 4
            print(f"🛡️  {item_name}を装備！ 防御+4")

    def use_item(self, item_name: str) -> bool:
        if self.inventory.get(item_name, 0) <= 0:
            print(f"{item_name}は持っていない！")
            return False
        self.inventory[item_name] -= 1
        if item_name == "傷薬":
            self.heal(50)
            print(f"💊 傷薬を使った！ HPが50回復！")
        elif item_name == "霊水":
            self.mp = min(self.max_mp, self.mp + 20)
            print(f"🧪 霊水を使った！ 霊力が20回復！")
        elif item_name == "不死鳥の羽":
            self.hp = self.max_hp // 2
            print(f"🪶 不死鳥の羽を使った！ HPが半分で復活！")
        elif item_name == "万能薬":
            self.hp = self.max_hp
            self.mp = self.max_mp
            print(f"💎 万能薬を使った！ HP・霊力が全回復！")
        return True

    def use_skill(self, skill_name: str, target) -> bool:
        data = SKILL_DATA.get(skill_name)
        if not data:
            return False
        if self.mp < data["cost"]:
            print("霊力が足りない！")
            return False
        self.mp -= data["cost"]

        if data["type"] == "attack":
            actual = target.take_damage(int(self.attack * data["power"]))
            print(f"{data['desc']}！ {target.name}に {actual} ダメージ！")
        elif data["type"] == "steal":
            actual = target.take_damage(int(self.attack * data["power"]))
            stolen = target.gold // 3
            target.gold -= stolen
            self.gold   += stolen
            print(f"{data['desc']}！ {target.name}に {actual} ダメージ＆{stolen}両盗んだ！")
        elif data["type"] == "heal":
            self.heal(int(data["power"]))
            print(f"{data['desc']}！ HPが{int(data['power'])}回復！")
        return True

    def take_damage(self, amount: int) -> int:
        actual = max(1, amount - self.defense)
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def gain_exp(self, amount: int):
        self.exp += amount
        print(f"{self.name}は {amount} 経験値を獲得！")
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self._level_up()

    def _level_up(self):
        self.level       += 1
        self.exp_to_next  = int(self.exp_to_next * 1.5)
        self.max_hp      += 20
        self.hp           = self.max_hp
        self.max_mp      += 5
        self.mp           = self.max_mp
        self.attack      += 3
        self.defense     += 2
        print(f"★ {self.name}は{self.level}段位になった！")