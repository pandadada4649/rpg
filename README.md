# 🌬️ 風の旅人

ブラウザで遊べるフルスタックRPGゲームです。

🎮 **プレイURL**: https://rpg-fwhn.onrender.com

---

## 概要

ドラクエ風のターン制RPGをPython/Flaskでフルスタック開発。
フィールドマップを矢印キーで歩き回り、ランダムエンカウントや
ボス討伐・クエストなど本格的なゲーム要素を実装しました。

---

## 機能

- 🗺️ フィールドマップ（4エリア：草原・森・砂漠・雪山）
- ⚔️ ターン制戦闘（魔法・スキル・アイテム）
- 👑 中ボス3体・ラスボス（魔王ゾルダン）
- 📋 クエストシステム
- 🔨 鍛冶屋（武器・防具強化）
- 📖 魔物図鑑
- 💾 クラウドセーブ（Supabase）
- 🎭 職業選択（戦士・魔法使い・盗賊）

---

## 使用技術

| カテゴリ | 技術 |
|---|---|
| バックエンド | Python 3.x, Flask |
| フロントエンド | HTML5, CSS3, JavaScript |
| データベース | PostgreSQL（Supabase） |
| インフラ | Render, Git/GitHub |

---

## ローカル実行方法

```bash
git clone https://github.com/pandadada4649/rpg.git
cd rpg
pip install -r requirements.txt

# .envファイルを作成
echo "SUPABASE_URL=your_url" > .env
echo "SUPABASE_KEY=your_key" >> .env

python3 app.py
```

ブラウザで `http://127.0.0.1:5000` を開く。
