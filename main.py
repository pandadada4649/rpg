from game.player import Player
from game.party import Party
from game.world import World
from game.save import load_game

GAME_TITLE = "風の旅人"

def select_class() -> str:
    print("=== 職業を選んでください ===")
    print("1: 戦士    （HP高め・物理攻撃特化）")
    print("2: 魔法使い（MP高め・魔法攻撃特化）")
    print("3: 盗賊    （素早さ高め・ぬすむ）")
    classes = {"1": "戦士", "2": "魔法使い", "3": "盗賊"}
    while True:
        choice = input("> ")
        if choice in classes:
            return classes[choice]
        print("1〜3を入力してください")

def main():
    print(f"\n{'='*35}")
    print(f"🌬️  ～ {GAME_TITLE} ～  ⚔️")
    print(f"{'='*35}")
    print("1: はじめから  2: つづきから")
    choice = input("> ")

    if choice == "2":
        data = load_game()
        if data:
            hero = Player(data["name"], data["player_class"])
            hero.load_from_data(data)
            party = Party(hero)
            world = World(party)
            world.run()
            return

    name = input("勇者の名前を入力してください > ")
    player_class = select_class()
    hero  = Player(name, player_class)
    party = Party(hero)
    world = World(party)
    world.run()

if __name__ == "__main__":
    main()