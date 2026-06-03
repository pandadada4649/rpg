from game.player import Player
from game.party import Party
from game.world import World
from game.save import load_game

# ゲームタイトル
GAME_TITLE = "鬼灯の剣士"

def select_class() -> str:
    print("=== 職を選べ ===")
    print("1: 侍　　（HP高め・力強い一太刀）")
    print("2: 陰陽師（霊力高め・術技特化）")
    print("3: 忍　　（素早さ高め・暗殺術）")
    classes = {"1": "侍", "2": "陰陽師", "3": "忍"}
    while True:
        choice = input("> ")
        if choice in classes:
            return classes[choice]
        print("1〜3を入力せよ")

def main():
    print(f"\n{'='*35}")
    print(f"🏮  ～ {GAME_TITLE} ～  ⚔️")
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

    name = input("汝の名は > ")
    player_class = select_class()
    hero  = Player(name, player_class)
    party = Party(hero)
    world = World(party)
    world.run()

if __name__ == "__main__":
    main()