import random

class BattleSystem:
    def __init__(self, party, enemy):
        self.party = party
        self.enemy = enemy

    def start(self):
        print(f"\n{'='*30}")
        print(f"⚔️  {self.enemy.name}があらわれた！")
        print(f"{'='*30}")

        while self.party.is_alive() and self.enemy.is_alive:
            for member in self.party.alive_members():
                if not self.enemy.is_alive:
                    break
                self._member_turn(member)
            if not self.enemy.is_alive or not self.party.is_alive():
                break
            self._enemy_turn()

        self._end()

    def _member_turn(self, player):
        print(f"\n--- {player.name}のターン ---")
        print(f"HP: {player.hp}/{player.max_hp}  MP: {player.mp}/{player.max_mp}")
        print("1: たたかう  2: まほう/スキル  3: アイテム  4: にげる")

        while True:
            choice = input("行動を選んでください > ")
            if choice in ["1", "2", "3", "4"]:
                break

        if choice == "1":
            damage = player.attack - self.enemy.defense
            actual = self.enemy.take_damage(damage)
            print(f"✅ {player.name}の攻撃！ {self.enemy.name}に {actual} ダメージ！")
            self.enemy.show_status()

        elif choice == "2":
            player.show_skills()
            s = input("> ")
            try:
                skill_name = player.skills[int(s) - 1]
                if not player.use_skill(skill_name, self.enemy):
                    self._member_turn(player)
            except (IndexError, ValueError):
                print("キャンセル")
                self._member_turn(player)

        elif choice == "3":
            player.show_inventory()
            item = input("使うアイテム名を入力 > ")
            if not player.use_item(item):
                self._member_turn(player)

        elif choice == "4":
            print(f"🏃 {player.name}は逃げ出した！")
            for m in self.party.members:
                m.hp = max(1, m.hp)
            self.enemy.hp = 0
            return

    def _enemy_turn(self):
        print(f"\n--- {self.enemy.name}のターン ---")
        action = self.enemy.choose_action()
        target = random.choice(self.party.alive_members())

        if action == "attack":
            actual = target.take_damage(self.enemy.attack)
            print(f"💥 {self.enemy.name}の攻撃！ {target.name}に {actual} ダメージ！")
        elif action == "special":
            actual = target.take_damage(self.enemy.attack * 2)
            print(f"💥 {self.enemy.name}の強攻撃！ {target.name}に {actual} ダメージ！")

        if not target.is_alive:
            print(f"💀 {target.name}は倒れた...")

    def _end(self):
        print(f"\n{'='*30}")
        if self.party.is_alive() and not self.enemy.is_alive:
            print(f"🎉 {self.enemy.name}を倒した！")
            total_exp  = self.enemy.exp
            total_gold = self.enemy.gold
            for member in self.party.alive_members():
                member.gain_exp(total_exp // len(self.party.alive_members()))
                member.gold += total_gold // len(self.party.alive_members())
            print(f"💰 {total_gold}G を獲得！")
        elif not self.party.is_alive():
            print(f"💀 パーティは全滅した...")
        print(f"{'='*30}")