# クエスト定義
QUESTS = {
    "q001": {
        "id":       "q001",
        "title":    "スライム退治",
        "desc":     "草原に出るスライムを3匹倒してほしい",
        "target":   "スライム",
        "count":    3,
        "reward_exp":  50,
        "reward_gold": 100,
    },
    "q002": {
        "id":       "q002",
        "title":    "森の番人",
        "desc":     "森のおおかみを5匹倒してほしい",
        "target":   "おおかみ",
        "count":    5,
        "reward_exp":  150,
        "reward_gold": 200,
    },
    "q003": {
        "id":       "q003",
        "title":    "砂漠の脅威",
        "desc":     "砂漠のサンドワームを3匹倒してほしい",
        "target":   "サンドワーム",
        "count":    3,
        "reward_exp":  300,
        "reward_gold": 400,
    },
    "q004": {
        "id":       "q004",
        "title":    "ゴブリンキング討伐",
        "desc":     "森に潜むゴブリンキングを倒してほしい",
        "target":   "ゴブリンキング",
        "count":    1,
        "reward_exp":  500,
        "reward_gold": 600,
    },
    "q005": {
        "id":       "q005",
        "title":    "魔王討伐",
        "desc":     "雪山の奥に潜む魔王ゾルダンを倒せ！",
        "target":   "🐉魔王ゾルダン",
        "count":    1,
        "reward_exp":  2000,
        "reward_gold": 3000,
    },
}

def get_all_quests():
    return list(QUESTS.values())

def get_quest(quest_id):
    return QUESTS.get(quest_id)