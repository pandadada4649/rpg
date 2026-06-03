import random

class Enemy:
    def __init__(self, name: str, hp: int, attack: int, defense: int, exp: int, gold: int, is_boss: bool = False):
        self.name     = name
        self.hp       = hp
        self.max_hp   = hp
        self.attack   = attack
        self.defense  = defense
        self.exp      = exp
        self.gold     = gold
        self.is_boss  = is_boss

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        actual = max(1, amount - self.defense)
        self.hp = max(0, self.hp - actual)
        return actual

    def choose_action(self) -> str:
        if self.is_boss:
            return random.choice(["attack", "attack", "special", "special"])
        return random.choice(["attack", "attack", "attack", "special"])

    def show_status(self):
        bar_len = 20
        filled  = int(bar_len * self.hp / self.max_hp)
        bar     = "█" * filled + "░" * (bar_len - filled)
        print(f"{self.name} [{bar}] {self.hp}/{self.max_hp}")


ENEMY_DATA = {
    # 草原エリア
    "スライム":       {"hp": 20,  "attack": 5,  "defense": 1,  "exp": 10,  "gold": 5},
    "ゴブリン":       {"hp": 35,  "attack": 10, "defense": 3,  "exp": 25,  "gold": 12},
    # 森エリア
    "おおかみ":       {"hp": 45,  "attack": 14, "defense": 4,  "exp": 35,  "gold": 18},
    "がいこつ":       {"hp": 55,  "attack": 18, "defense": 8,  "exp": 50,  "gold": 25},
    "ダークエルフ":   {"hp": 65,  "attack": 22, "defense": 10, "exp": 70,  "gold": 35},
    # 砂漠エリア
    "サソリ":         {"hp": 70,  "attack": 25, "defense": 12, "exp": 90,  "gold": 45},
    "ミイラ":         {"hp": 80,  "attack": 28, "defense": 14, "exp": 110, "gold": 55},
    "サンドワーム":   {"hp": 100, "attack": 32, "defense": 16, "exp": 140, "gold": 70},
    # 雪山エリア
    "アイスゴーレム": {"hp": 120, "attack": 35, "defense": 20, "exp": 180, "gold": 90},
    "フロストウルフ": {"hp": 110, "attack": 38, "defense": 18, "exp": 200, "gold": 100},
    "オーク":         {"hp": 80,  "attack": 22, "defense": 10, "exp": 80,  "gold": 40},
    # 中ボス
    "ゴブリンキング":  {"hp": 180, "attack": 30, "defense": 15, "exp": 250, "gold": 150, "is_boss": True},
    "デスナイト":      {"hp": 250, "attack": 42, "defense": 22, "exp": 400, "gold": 250, "is_boss": True},
    "闇の賢者":        {"hp": 220, "attack": 50, "defense": 18, "exp": 500, "gold": 300, "is_boss": True},
    # ラスボス
    "🐉魔王ゾルダン": {"hp": 500, "attack": 65, "defense": 30, "exp": 1000, "gold": 1000, "is_boss": True},
}

def create_enemy(enemy_type: str) -> Enemy:
    d = ENEMY_DATA.get(enemy_type)
    if not d:
        raise ValueError(f"Unknown enemy: {enemy_type}")
    return Enemy(
        name     = enemy_type,
        hp       = d["hp"],
        attack   = d["attack"],
        defense  = d["defense"],
        exp      = d["exp"],
        gold     = d["gold"],
        is_boss  = d.get("is_boss", False),
    )

# エリア別エンカウントテーブル
AREA_ENEMIES = {
    "grassland": ["スライム", "ゴブリン"],
    "forest":    ["おおかみ", "がいこつ", "ダークエルフ"],
    "desert":    ["サソリ", "ミイラ", "サンドワーム"],
    "snow":      ["アイスゴーレム", "フロストウルフ"],
}

AREA_BOSSES = {
    "forest_boss": "ゴブリンキング",
    "desert_boss": "デスナイト",
    "snow_boss":   "闇の賢者",
    "last_boss":   "🐉魔王ゾルダン",
}