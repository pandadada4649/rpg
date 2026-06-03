QUESTS = {
    "q001": {
        "id":          "q001",
        "title":       "泥怪退治",
        "desc":        "草原に出没する泥怪を3体討伐してほしい",
        "target":      "泥怪",
        "count":       3,
        "reward_exp":  50,
        "reward_gold": 100,
    },
    "q002": {
        "id":          "q002",
        "title":       "森の狼妖",
        "desc":        "森に潜む狼妖を5体討伐してほしい",
        "target":      "狼妖",
        "count":       5,
        "reward_exp":  150,
        "reward_gold": 200,
    },
    "q003": {
        "id":          "q003",
        "title":       "砂漠の砂龍",
        "desc":        "砂漠に巣食う砂龍を3体討伐してほしい",
        "target":      "砂龍",
        "count":       3,
        "reward_exp":  300,
        "reward_gold": 400,
    },
    "q004": {
        "id":          "q004",
        "title":       "鬼将軍討伐",
        "desc":        "森を支配する鬼将軍を討ち取ってほしい",
        "target":      "鬼将軍",
        "count":       1,
        "reward_exp":  500,
        "reward_gold": 600,
    },
    "q005": {
        "id":          "q005",
        "title":       "夜叉羅討伐",
        "desc":        "幽霧国に侵攻する魔王・夜叉羅を討て！",
        "target":      "👹夜叉羅",
        "count":       1,
        "reward_exp":  2000,
        "reward_gold": 3000,
    },
}

def get_all_quests():
    return list(QUESTS.values())

def get_quest(quest_id):
    return QUESTS.get(quest_id)