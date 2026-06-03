import random

class Enemy:
    def __init__(self, name: str, hp: int, attack: int, defense: int, exp: int, gold: int, is_boss: bool = False):
        self.name    = name
        self.hp      = hp
        self.max_hp  = hp
        self.attack  = attack
        self.defense = defense
        self.exp     = exp
        self.gold    = gold
        self.is_boss = is_boss

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
    "泥怪":       {"hp": 20,  "attack": 5,  "defense": 1,  "exp": 10,  "gold": 5},
    "小鬼":       {"hp": 35,  "attack": 10, "defense": 3,  "exp": 25,  "gold": 12},
    # 森エリア
    "狼妖":       {"hp": 45,  "attack": 14, "defense": 4,  "exp": 35,  "gold": 18},
    "骸武者":     {"hp": 55,  "attack": 18, "defense": 8,  "exp": 50,  "gold": 25},
    "闇烏":       {"hp": 65,  "attack": 22, "defense": 10, "exp": 70,  "gold": 35},
    # 砂漠エリア
    "砂蠍":       {"hp": 70,  "attack": 25, "defense": 12, "exp": 90,  "gold": 45},
    "呪術師":     {"hp": 80,  "attack": 28, "defense": 14, "exp": 110, "gold": 55},
    "砂龍":       {"hp": 100, "attack": 32, "defense": 16, "exp": 140, "gold": 70},
    # 雪山エリア
    "氷鬼":       {"hp": 120, "attack": 35, "defense": 20, "exp": 180, "gold": 90},
    "雪狼":       {"hp": 110, "attack": 38, "defense": 18, "exp": 200, "gold": 100},
    "山鬼":       {"hp": 80,  "attack": 22, "defense": 10, "exp": 80,  "gold": 40},
    # 中ボス
    "鬼将軍":     {"hp": 180, "attack": 30, "defense": 15, "exp": 250, "gold": 150, "is_boss": True},
    "死武者":     {"hp": 250, "attack": 42, "defense": 22, "exp": 400, "gold": 250, "is_boss": True},
    "妖術師":     {"hp": 220, "attack": 50, "defense": 18, "exp": 500, "gold": 300, "is_boss": True},
    # ラスボス
    "👹夜叉羅":   {"hp": 500, "attack": 65, "defense": 30, "exp": 1000, "gold": 1000, "is_boss": True},
}

def create_enemy(enemy_type: str) -> Enemy:
    d = ENEMY_DATA.get(enemy_type)
    if not d:
        raise ValueError(f"未知の敵: {enemy_type}")
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
    "grassland": ["泥怪", "小鬼"],
    "forest":    ["狼妖", "骸武者", "闇烏"],
    "desert":    ["砂蠍", "呪術師", "砂龍"],
    "snow":      ["氷鬼", "雪狼"],
}

AREA_BOSSES = {
    "forest_boss": "鬼将軍",
    "desert_boss": "死武者",
    "snow_boss":   "妖術師",
    "last_boss":   "👹夜叉羅",
}