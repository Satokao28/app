import datetime
import streamlit as st

# 1. 画面のタイトルと説明
st.title("🎨 モチベキャンパス (テスト版)")
st.write("課題を追加して、カレンダーや一覧と正しく連動するかテストしましょう！")

# 2. データの初期化（アプリ起動時に1回だけ実行される、簡易的なデータ置き場）
if "tasks" not in st.session_state:
    # テスト用のダミーデータを最初から入れておく
    st.session_state.tasks = [
        {
            "id": 1,
            "title": "プログラミング基礎レポート",
            "date": datetime.date(2026, 7, 10),
            "status": "未完了",
        },
        {
            "id": 2,
            "title": "英語スピーチ準備",
            "date": datetime.date(2026, 7, 15),
            "status": "未完了",
        },
    ]

# 画面を「課題追加・一覧」と「カレンダー・時間割」のタブに分ける
tab1, tab2 = st.tabs(["📝 課題マネージャー", "📅 カレンダー・時間割"])

# --- タブ1: 課題マネージャー ---
with tab1:
    st.header("課題の一覧と追加")

    # 新しい課題の入力フォーム
    with st.form("add_task_form"):
        new_title = st.text_input("課題名を入力してください")
        new_date = st.date_input("締切日", datetime.date(2026, 7, 8))
        submit_button = st.form_submit_button("課題を追加")

        if submit_button and new_title:
            # 新しい課題をデータに追加
            new_id = (
                max([t["id"] for t in st.session_state.tasks]) + 1
                if st.session_state.tasks
                else 1
            )
            st.session_state.tasks.append(
                {
                    "id": new_id,
                    "title": new_title,
                    "date": new_date,
                    "status": "未完了",
                }
            )
            st.success(f"「{new_title}」を追加しました！")
            st.rerun()

    st.subheader("現在の未完了課題一覧")
    # 課題をループ処理で表示
    for task in st.session_state.tasks:
        if task["status"] == "未完了":
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{task['title']}** (締切: {task['date']})")
            # 「完了」ボタンが押されたらステータスを更新
            if col2.button("完了にする", key=f"complete_{task['id']}"):
                task["status"] = "完了"
                st.success(f"「{task['title']}」を完了しました！")
                st.rerun()

# --- タブ2: カレンダー・時間割 ---
with tab2:
    st.header("スケジュール確認")
    st.write("※未完了の課題だけがここに連動して表示されます。")

    # カレンダーの代わりに、日付順に並んだスケジュールを表示（テスト用）
    incomplete_tasks = [
        t for t in st.session_state.tasks if t["status"] == "未完了"
    ]

    if not incomplete_tasks:
        st.info("現在、予定されている課題はありません。モチベーション最高！")
    else:
        # 日付順に並び替え
        sorted_tasks = sorted(incomplete_tasks, key=lambda x: x["date"])
        for task in sorted_tasks:
            # マークダウンを使って少しデコレーション
            st.info(f"📅 **{task['date']}** ➔ ⚠️ 課題: {task['title']}")

