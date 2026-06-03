import random
from game.player import Player
from game.party import Party
from game.enemy import create_enemy
from game.battle import BattleSystem
from game.dungeon import Dungeon
from game.save import save_game, load_game

COMPANIONS = [
    {"name": "エリス",  "class": "魔法使い"},
    {"name": "ガレス",  "class": "戦士"},
    {"name": "ニナ",    "class": "盗賊"},
]

class World:
    def __init__(self, party: Party):
        self.party    = party
        self.location = "町"
        self.recruited = []

    def run(self):
        print(f"\n🌬️  {self.party.leader.name}の冒険が始まった！")
        while self.party.is_alive():
            if self.location == "町":
                self._town_menu()
            elif self.location == "フィールド":
                self._field_action()

    def _town_menu(self):
        print(f"\n🏘️  === 風の町 ===")
        self.party.show_status()
        print("1: フィールドへ出る")
        print("2: ダンジョンへ行く🏚️")
        print("3: 宿屋（HP/MP全回復 10G）")
        print("4: 武器屋")
        print("5: 防具屋")
        print("6: 酒場（仲間を探す）")
        print("7: セーブ")
        print("8: ゲーム終了")

        choice = input("> ")
        if choice == "1":
            self.location = "フィールド"
        elif choice == "2":
            dungeon = Dungeon(self.party)
            dungeon.enter()
        elif choice == "3":
            self._inn()
        elif choice == "4":
            self._weapon_shop()
        elif choice == "5":
            self._armor_shop()
        elif choice == "6":
            self._tavern()
        elif choice == "7":
            save_game(self.party.leader)
        elif choice == "8":
            print("またね！🌬️")
            exit()

    def _inn(self):
        if self.party.leader.gold >= 10:
            self.party.leader.gold -= 10
            for m in self.party.members:
                m.hp = m.max_hp
                m.mp = m.max_mp
            print("💤 宿屋に泊まった！ 全員のHP・MPが全回復！")
        else:
            print("💰 ゴールドが足りない！（10G必要）")

    def _weapon_shop(self):
        weapons = {
            "1": ("ブロンズソード",   80),
            "2": ("アイアンソード",  200),
            "3": ("フレイムブレード", 500),
            "4": ("風の剣",          800),
        }
        print("\n⚔️  === 武器屋 ===")
        for key, (name, price) in weapons.items():
            print(f"{key}: {name} ({price}G)")
        print("0: もどる")
        choice = input("> ")
        if choice in weapons:
            name, price = weapons[choice]
            if self.party.leader.gold >= price:
                self.party.leader.gold -= price
                self.party.leader.equip(name, "weapon")
            else:
                print("💰 ゴールドが足りない！")

    def _armor_shop(self):
        armors = {
            "1": ("レザーアーマー",    60),
            "2": ("チェインメイル",   180),
            "3": ("プレートアーマー", 450),
            "4": ("風の鎧",           750),
        }
        print("\n🛡️  === 防具屋 ===")
        for key, (name, price) in armors.items():
            print(f"{key}: {name} ({price}G)")
        print("0: もどる")
        choice = input("> ")
        if choice in armors:
            name, price = armors[choice]
            if self.party.leader.gold >= price:
                self.party.leader.gold -= price
                self.party.leader.equip(name, "armor")
            else:
                print("💰 ゴールドが足りない！")

    def _tavern(self):
        available = [c for c in COMPANIONS if c["name"] not in self.recruited]
        if not available:
            print("🍺 今は仲間になれる人がいない...")
            return
        print("\n🍺 === 酒場 ===")
        print("仲間に誘える冒険者：")
        for i, c in enumerate(available, 1):
            print(f"{i}: {c['name']}（{c['class']}）")
        print("0: もどる")
        choice = input("> ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                companion_data = available[idx]
                companion = Player(companion_data["name"], companion_data["class"])
                if self.party.add_member(companion):
                    self.recruited.append(companion_data["name"])
        except ValueError:
            pass

    def _field_action(self):
        print(f"\n🌿 === フィールド ===")
        print("1: 町に戻る  2: 進む（エンカウント）")
        choice = input("> ")
        if choice == "1":
            self.location = "町"
        elif choice == "2":
            self._random_encounter()

    def _random_encounter(self):
        enemies = ["スライム", "ゴブリン", "おおかみ", "がいこつ", "オーク"]
        enemy   = create_enemy(random.choice(enemies))
        battle  = BattleSystem(self.party, enemy)
        battle.start()
        if not self.party.is_alive():
            print("\n💀 ゲームオーバー...")