import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase     = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_game(player):
    data = {
        "name":         player.name,
        "player_class": player.player_class,
        "level":        player.level,
        "exp":          player.exp,
        "exp_to_next":  player.exp_to_next,
        "max_hp":       player.max_hp,
        "hp":           player.hp,
        "max_mp":       player.max_mp,
        "mp":           player.mp,
        "attack":       player.attack,
        "defense":      player.defense,
        "speed":        player.speed,
        "gold":         player.gold,
        "inventory":    player.inventory,
        "equipment":    player.equipment,
        "skills":       player.skills,
        "boss_cleared": player.boss_cleared,
    }
    # 既存データを確認
    existing = supabase.table("save_data") \
        .select("id") \
        .eq("player_name", player.name) \
        .execute()

    now = datetime.now(timezone.utc).isoformat()

    if existing.data:
        # 更新
        supabase.table("save_data") \
            .update({"data": data, "updated_at": now}) \
            .eq("player_name", player.name) \
            .execute()
    else:
        # 新規作成
        supabase.table("save_data") \
            .insert({"player_name": player.name, "data": data, "updated_at": now}) \
            .execute()

    print(f"💾 {player.name}のデータをクラウドに保存しました！")

def load_game(player_name: str):
    result = supabase.table("save_data") \
        .select("data") \
        .eq("player_name", player_name) \
        .execute()

    if not result.data:
        print("セーブデータが見つかりません")
        return None

    print("📂 クラウドからデータをロードしました！")
    return result.data[0]["data"]

def delete_save(player_name: str):
    supabase.table("save_data") \
        .delete() \
        .eq("player_name", player_name) \
        .execute()
    print("🗑️  セーブデータを削除しました")