import streamlit as st
import random
import time
import pandas as pd

# ---------------------------------
# 기본 설정
# ---------------------------------
st.set_page_config(page_title="💌너에게 전하는 비혼 프로포즈 게임", layout="wide")

PASTEL_COLORS = [
    "#A8DADC", "#FBC4AB", "#BDE0FE", "#FFAFCC", "#C8E7ED", "#FFE5B4",
    "#D7ECD9", "#E0BBE4", "#C1D3FF", "#F7D9C4", "#D9F7BE", "#F6C6EA"
]

# 항상 표시할 12개 단어
BASE_WORDS = pd.read_csv("base_cards.csv", encoding="utf-8")["base"].tolist()

BASE_COLORS = [
    "#A8DADC", "#FBC4AB", "#BDE0FE", "#FFAFCC",
    "#C8E7ED", "#FFE5B4", "#D7ECD9", "#E0BBE4",
    "#C1D3FF", "#F7D9C4", "#D9F7BE", "#F6C6EA"
]

# 전체 80개 단어 (예시 — 여기에 본인 단어 목록 추가)
WORDS = pd.read_csv("word_cards.csv", encoding="utf-8")["words"].tolist()

# ---------------------------------
# 유틸 함수
# ---------------------------------
def pastel_block(word, color, width="100%"):
    """파스텔톤 단어 블록"""
    return f"""
    <div style='background-color:{color};
                padding:10px;
                border-radius:12px;
                text-align:center;
                font-size:16px;
                font-weight:500;
                margin:6px 0;
                width:{width};
                box-shadow:0 2px 4px rgba(0,0,0,0.1);'>
        {word}
    </div>
    """

def show_word_blocks(words, columns=4):
    """단어들을 grid 형태로 표시 (랜덤 색상)"""
    rows = [words[i:i+columns] for i in range(0, len(words), columns)]
    for row in rows:
        cols = st.columns(columns)
        for i, w in enumerate(row):
            with cols[i]:
                color = random.choice(PASTEL_COLORS)
                st.markdown(pastel_block(w, color), unsafe_allow_html=True)

# ---------------------------------
# 세션 상태 초기화
# ---------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "random_words" not in st.session_state:
    st.session_state.random_words = []

# ---------------------------------
# 사이드바 - 항상 표시되는 12단어
# ---------------------------------
st.sidebar.title("📚 기본 카드")
for w, c in zip(BASE_WORDS, BASE_COLORS):
    st.sidebar.markdown(pastel_block(w, c), unsafe_allow_html=True)

# ---------------------------------
# 메인 헤더 (크고 중앙 정렬된 제목)
# ---------------------------------
st.markdown(
    """
    <h1 style='text-align:center; 
               font-size:48px; 
               font-weight:700; 
               margin-bottom:20px;
               color:#3C3C3C;'>
        💌 너에게 전하는 비혼 프로포즈 게임 체험판
    </h1>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# 메인 화면
# ---------------------------------
if st.session_state.page == "home":
    st.subheader("✨ 단어 카드 뽑기 ✨")
    st.write("버튼을 눌러 8개의 단어를 뽑아보세요.")

    if st.button("카드 뽑기"):
        st.session_state.random_words = random.sample(WORDS, 8)
        st.session_state.page = "show_random"
        st.rerun()

elif st.session_state.page == "show_random":
    st.subheader("✨ 단어 카드 8장 ✨")
    show_word_blocks(st.session_state.random_words, columns=4)

    timer_placeholder = st.empty()
    start_btn = st.button("⏱ 타이머 시작")

    if start_btn:
        for i in range(90, -1, -1):
            mins, secs = divmod(i, 60)
            timer_placeholder.markdown(f"### ⏳ 남은 시간: {mins:02d}:{secs:02d}")
            time.sleep(1)
        st.session_state.page = "write_sentence"
        st.rerun()

    if st.button("종료"):
        st.session_state.page = "home"
        st.rerun()

elif st.session_state.page == "write_sentence":
    st.subheader("📝 비혼 프로포즈를 적어주세요!")
    st.text_area("기본 카드와 단어 카드를 활용해 비혼 프로포즈를 작성해보세요.", height=150)

    if st.button("종료"):
        st.session_state.page = "home"
        st.rerun()