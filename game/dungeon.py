import random
from game.enemy import create_enemy
from game.battle import BattleSystem

RARE_ITEMS = ["フェニックスの羽", "エリクサー", "ドラゴンの鱗", "風の結晶"]

DUNGEON_FLOORS = {
    1: {"name": "浅い洞窟",   "enemies": ["スライム", "ゴブリン"],              "boss": None},
    2: {"name": "霧の森",     "enemies": ["おおかみ", "がいこつ"],              "boss": None},
    3: {"name": "魔王の塔",   "enemies": ["おおかみ", "がいこつ", "オーク"],    "boss": "ドラゴン"},
}

class Dungeon:
    def __init__(self, party):
        self.party       = party
        self.current_floor = 1
        self.max_floor     = len(DUNGEON_FLOORS)

    def enter(self):
        print(f"\n🏚️  ダンジョンに入った！")
        while self.current_floor <= self.max_floor:
            floor_data = DUNGEON_FLOORS[self.current_floor]
            print(f"\n{'='*30}")
            print(f"⚔️  {self.current_floor}階層：{floor_data['name']}")
            print(f"{'='*30}")
            print("1: 進む  2: 探索（宝箱を探す）  3: 引き返す")
            choice = input("> ")

            if choice == "1":
                self._encounter(floor_data["enemies"])
                if not self.party.is_alive():
                    print("💀 パーティが全滅した...")
                    return
                if floor_data["boss"] and self.current_floor == self.max_floor:
                    self._boss_encounter(floor_data["boss"])
                    return
                self.current_floor += 1

            elif choice == "2":
                self._search_treasure()

            elif choice == "3":
                print("🏃 ダンジョンから脱出した！")
                return

        print("\n🎊 ダンジョンを制覇した！！")

    def _encounter(self, enemy_list):
        enemy = create_enemy(random.choice(enemy_list))
        battle = BattleSystem(self.party, enemy)
        battle.start()

    def _boss_encounter(self, boss_name):
        print(f"\n🐉 ボス：{boss_name}があらわれた！")
        boss = create_enemy(boss_name)
        battle = BattleSystem(self.party, boss)
        battle.start()
        if not boss.is_alive:
            self.party.leader.boss_cleared = True
            print("\n🎊 ボスを倒した！ダンジョン制覇！！")

    def _search_treasure(self):
        roll = random.random()
        leader = self.party.leader
        if roll < 0.4:
            gold = random.randint(20, 100) * self.current_floor
            leader.gold += gold
            print(f"💰 宝箱を見つけた！ {gold}G 獲得！")
        elif roll < 0.65:
            item = random.choice(RARE_ITEMS)
            leader.inventory[item] = leader.inventory.get(item, 0) + 1
            print(f"✨ レアアイテム「{item}」を手に入れた！")
        elif roll < 0.85:
            potion_count = random.randint(1, 3)
            leader.inventory["ポーション"] = leader.inventory.get("ポーション", 0) + potion_count
            print(f"💊 ポーションx{potion_count}を見つけた！")
        else:
            print("📦 空の宝箱だった...")