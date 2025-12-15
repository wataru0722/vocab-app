import streamlit as st
import csv
import random
import os

# ページ設定
st.set_page_config(page_title="単語学習アプリ", layout="centered")

# セッション状態の初期化
if 'current_word' not in st.session_state:
    st.session_state.current_word = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'words' not in st.session_state:
    st.session_state.words = []

# --- サイドバー：設定 ---
st.sidebar.header("設定")
file_option = st.sidebar.radio(
    "学習するファイルを選択:",
    ("word_list.csv", "zenntisi.csv")
)


# データを読み込む関数（Pandasを使わず、標準のcsvモジュールを使用）
def load_data(filename):
    if not os.path.exists(filename):
        return []
    try:
        data = []
        # utf-8-sig で読み込むことで文字化け防止
        with open(filename, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                # データが2列以上ある行だけを読み込む
                if len(row) >= 2:
                    data.append(row)
        return data
    except Exception as e:
        st.error(f"読み込みエラー: {e}")
        return []


# ファイルが変更されたらデータを再読み込み
if 'last_file' not in st.session_state or st.session_state.last_file != file_option:
    st.session_state.words = load_data(file_option)
    st.session_state.last_file = file_option
    st.session_state.current_word = None

# --- メイン画面 ---
st.title("📱 スマホで単語学習")
st.caption(f"現在のモード: {file_option}")

words = st.session_state.words

# 単語データがない場合
if not words:
    st.warning(f"フォルダに {file_option} が見つかりません。")
    st.info("CSVファイルを同じフォルダに配置してください。")
else:
    # --- 学習画面 ---

    if st.session_state.current_word is None:
        st.session_state.current_word = random.choice(words)
        st.session_state.show_answer = False

    # 現在の問題
    eng = st.session_state.current_word[0]
    jpn = st.session_state.current_word[1]

    # --- UI表示 ---
    st.markdown("---")

    # 英語を大きく表示
    st.markdown(f"<h1 style='text-align: center; color: #1E88E5;'>{eng}</h1>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("答えを見る", use_container_width=True):
            st.session_state.show_answer = True

    with col2:
        if st.button("次の単語へ", use_container_width=True):
            st.session_state.current_word = random.choice(words)
            st.session_state.show_answer = False
            st.rerun()  # ボタンを押した瞬間に画面を更新

    # 答えの表示
    if st.session_state.show_answer:
        st.markdown(
            f"<div style='text-align: center; font-size: 24px; color: #2E7D32; font-weight: bold; margin-top: 20px;'>{jpn}</div>",
            unsafe_allow_html=True)

    st.markdown("---")
    st.text(f"収録単語数: {len(words)} 語")