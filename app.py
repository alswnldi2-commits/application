import streamlit as st
import json
import random
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="SAT 영어 단어 학습",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'words' not in st.session_state:
    with open('sat_words.json', 'r', encoding='utf-8') as f:
        st.session_state.words = json.load(f)
    
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if 'favorites' not in st.session_state:
    st.session_state.favorites = set()

if 'quiz_words' not in st.session_state:
    st.session_state.quiz_words = []

if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = {'correct': 0, 'total': 0}

if 'learned_words' not in st.session_state:
    st.session_state.learned_words = set()

# CSS 스타일
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .word-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .meaning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .example-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stats-box {
        background: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown('<div class="main-header">📚 SAT 영어 단어 학습</div>', unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.header("📖 메뉴")
    page = st.radio(
        "학습 모드 선택",
        ["🏠 홈", "📇 단어 목록", "🃏 플래시카드", "✏️ 퀴즈", "🔍 검색", "⭐ 즐겨찾기"],
        index=0
    )
    
    st.divider()
    
    # 통계
    st.subheader("📊 학습 통계")
    st.markdown(f"""
    <div class="stats-box">
        <strong>전체 단어:</strong> {len(st.session_state.words)}개<br>
        <strong>학습한 단어:</strong> {len(st.session_state.learned_words)}개<br>
        <strong>즐겨찾기:</strong> {len(st.session_state.favorites)}개<br>
        <strong>학습 진행도:</strong> {len(st.session_state.learned_words) / len(st.session_state.words) * 100:.1f}%
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 초기화 버튼
    if st.button("🔄 진행도 초기화"):
        st.session_state.learned_words = set()
        st.session_state.favorites = set()
        st.session_state.quiz_score = {'correct': 0, 'total': 0}
        st.rerun()

# 홈 페이지
if page == "🏠 홈":
    st.markdown("""
    ## 환영합니다! 👋
    
    **SAT 영어 단어 학습 사이트**에 오신 것을 환영합니다.
    
    ### 주요 기능:
    - 📇 **단어 목록**: 모든 SAT 빈출 단어를 한눈에 확인
    - 🃏 **플래시카드**: 카드 형식으로 단어 학습
    - ✏️ **퀴즈**: 단어 실력을 테스트
    - 🔍 **검색**: 원하는 단어를 빠르게 찾기
    - ⭐ **즐겨찾기**: 중요한 단어를 저장
    
    ### 사용 방법:
    1. 왼쪽 사이드바에서 원하는 학습 모드를 선택하세요.
    2. 플래시카드 모드에서 단어를 학습하세요.
    3. 퀴즈 모드에서 실력을 확인하세요.
    4. 학습한 단어는 자동으로 기록됩니다.
    
    **좋은 학습 되세요!** 🎓
    """)

# 단어 목록 페이지
elif page == "📇 단어 목록":
    st.header("📇 단어 목록")
    
    # 필터 옵션
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("🔍 단어 검색", placeholder="단어나 뜻으로 검색...")
    with col2:
        show_only_favorites = st.checkbox("⭐ 즐겨찾기만 보기")
        show_only_learned = st.checkbox("✅ 학습한 단어만 보기")
    
    # 단어 필터링
    filtered_words = st.session_state.words
    
    if show_only_favorites:
        filtered_words = [w for w in filtered_words if w['word'] in st.session_state.favorites]
    
    if show_only_learned:
        filtered_words = [w for w in filtered_words if w['word'] in st.session_state.learned_words]
    
    if search_term:
        filtered_words = [
            w for w in filtered_words
            if search_term.lower() in w['word'].lower() or search_term.lower() in w['meaning'].lower()
        ]
    
    st.info(f"총 {len(filtered_words)}개의 단어가 표시됩니다.")
    
    # 단어 카드 표시
    for idx, word_data in enumerate(filtered_words):
        with st.expander(f"**{word_data['word']}** - {word_data['meaning']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**뜻:** {word_data['meaning']}")
                st.markdown(f"**예문:** {word_data['example']}")
            with col2:
                is_favorite = word_data['word'] in st.session_state.favorites
                favorite_emoji = "⭐" if is_favorite else "☆"
                if st.button(favorite_emoji, key=f"fav_{idx}_{word_data['word']}"):
                    if is_favorite:
                        st.session_state.favorites.discard(word_data['word'])
                    else:
                        st.session_state.favorites.add(word_data['word'])
                    st.rerun()
                
                is_learned = word_data['word'] in st.session_state.learned_words
                if st.button("✅ 학습 완료" if not is_learned else "✅ 완료됨", key=f"learn_{idx}_{word_data['word']}"):
                    if not is_learned:
                        st.session_state.learned_words.add(word_data['word'])
                        st.rerun()

# 플래시카드 페이지
elif page == "🃏 플래시카드":
    st.header("🃏 플래시카드 학습")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # 현재 단어
        current_word = st.session_state.words[st.session_state.current_index]
        
        # 카드 표시
        st.markdown(f"""
        <div class="word-card">
            <h1 style="font-size: 3rem; margin: 1rem 0;">{current_word['word']}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # 뜻 보기/숨기기
        show_meaning = st.checkbox("뜻 보기", key="show_meaning")
        
        if show_meaning:
            st.markdown(f"""
            <div class="meaning-card">
                <h2>{current_word['meaning']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="example-card">
                <strong>예문:</strong><br>
                <em>{current_word['example']}</em>
            </div>
            """, unsafe_allow_html=True)
        
        # 컨트롤 버튼
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
        
        with col_btn1:
            if st.button("⏮️ 처음"):
                st.session_state.current_index = 0
                st.rerun()
        
        with col_btn2:
            if st.button("◀️ 이전"):
                st.session_state.current_index = (st.session_state.current_index - 1) % len(st.session_state.words)
                st.rerun()
        
        with col_btn3:
            if st.button("다음 ▶️"):
                st.session_state.current_index = (st.session_state.current_index + 1) % len(st.session_state.words)
                st.rerun()
        
        with col_btn4:
            if st.button("🔀 랜덤"):
                st.session_state.current_index = random.randint(0, len(st.session_state.words) - 1)
                st.rerun()
        
        # 추가 기능
        col_fav, col_learn = st.columns(2)
        with col_fav:
            is_favorite = current_word['word'] in st.session_state.favorites
            if st.button("⭐ 즐겨찾기 추가" if not is_favorite else "⭐ 즐겨찾기 제거"):
                if is_favorite:
                    st.session_state.favorites.discard(current_word['word'])
                else:
                    st.session_state.favorites.add(current_word['word'])
                st.rerun()
        
        with col_learn:
            is_learned = current_word['word'] in st.session_state.learned_words
            if st.button("✅ 학습 완료" if not is_learned else "✅ 완료됨"):
                if not is_learned:
                    st.session_state.learned_words.add(current_word['word'])
                    st.rerun()
        
        # 진행도
        progress = (st.session_state.current_index + 1) / len(st.session_state.words)
        st.progress(progress)
        st.caption(f"{st.session_state.current_index + 1} / {len(st.session_state.words)}")

# 퀴즈 페이지
elif page == "✏️ 퀴즈":
    st.header("✏️ 퀴즈 모드")
    
    # 퀴즈 설정
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider("문제 수", 5, 20, 10)
        quiz_type = st.radio("퀴즈 유형", ["단어 → 뜻", "뜻 → 단어"])
    with col2:
        if st.button("🔄 새 퀴즈 시작"):
            st.session_state.quiz_words = random.sample(st.session_state.words, min(num_questions, len(st.session_state.words)))
            st.session_state.quiz_score = {'correct': 0, 'total': 0}
            st.session_state.quiz_answers = {}
            st.rerun()
    
    # 퀴즈 진행
    if 'quiz_words' in st.session_state and len(st.session_state.quiz_words) > 0:
        if 'quiz_answers' not in st.session_state:
            st.session_state.quiz_answers = {}
        
        current_quiz_idx = len(st.session_state.quiz_answers)
        
        if current_quiz_idx < len(st.session_state.quiz_words):
            current_word = st.session_state.quiz_words[current_quiz_idx]
            
            st.markdown(f"### 문제 {current_quiz_idx + 1} / {len(st.session_state.quiz_words)}")
            
            if quiz_type == "단어 → 뜻":
                st.markdown(f"#### 단어: **{current_word['word']}**")
                st.write("이 단어의 뜻은 무엇일까요?")
                
                # 선택지 생성
                all_words = [w for w in st.session_state.words if w['word'] != current_word['word']]
                wrong_answers = random.sample([w['meaning'] for w in all_words], 3)
                options = [current_word['meaning']] + wrong_answers
                random.shuffle(options)
                
                selected = st.radio("답을 선택하세요:", options, key=f"quiz_{current_quiz_idx}")
                
                if st.button("제출"):
                    is_correct = selected == current_word['meaning']
                    st.session_state.quiz_answers[current_quiz_idx] = is_correct
                    st.session_state.quiz_score['total'] += 1
                    if is_correct:
                        st.session_state.quiz_score['correct'] += 1
                        st.success(f"✅ 정답입니다! 예문: {current_word['example']}")
                        st.session_state.learned_words.add(current_word['word'])
                    else:
                        st.error(f"❌ 틀렸습니다. 정답: {current_word['meaning']}")
                        st.info(f"예문: {current_word['example']}")
                    st.rerun()
            
            else:  # 뜻 → 단어
                st.markdown(f"#### 뜻: **{current_word['meaning']}**")
                st.write("이 뜻에 해당하는 단어는 무엇일까요?")
                
                # 선택지 생성
                all_words = [w for w in st.session_state.words if w['word'] != current_word['word']]
                wrong_answers = random.sample([w['word'] for w in all_words], 3)
                options = [current_word['word']] + wrong_answers
                random.shuffle(options)
                
                selected = st.radio("답을 선택하세요:", options, key=f"quiz_{current_quiz_idx}")
                
                if st.button("제출"):
                    is_correct = selected == current_word['word']
                    st.session_state.quiz_answers[current_quiz_idx] = is_correct
                    st.session_state.quiz_score['total'] += 1
                    if is_correct:
                        st.session_state.quiz_score['correct'] += 1
                        st.success(f"✅ 정답입니다! 예문: {current_word['example']}")
                        st.session_state.learned_words.add(current_word['word'])
                    else:
                        st.error(f"❌ 틀렸습니다. 정답: {current_word['word']}")
                        st.info(f"예문: {current_word['example']}")
                    st.rerun()
        else:
            # 퀴즈 결과
            st.balloons()
            st.markdown("### 🎉 퀴즈 완료!")
            
            score = st.session_state.quiz_score['correct']
            total = st.session_state.quiz_score['total']
            percentage = (score / total * 100) if total > 0 else 0
            
            st.metric("점수", f"{score} / {total}", f"{percentage:.1f}%")
            
            # 결과 상세
            st.subheader("📊 결과 상세")
            for idx, word in enumerate(st.session_state.quiz_words):
                is_correct = st.session_state.quiz_answers.get(idx, False)
                emoji = "✅" if is_correct else "❌"
                st.write(f"{emoji} {word['word']} - {word['meaning']}")
    else:
        st.info("👆 '새 퀴즈 시작' 버튼을 눌러 퀴즈를 시작하세요!")

# 검색 페이지
elif page == "🔍 검색":
    st.header("🔍 단어 검색")
    
    search_query = st.text_input("검색어 입력", placeholder="단어나 뜻을 입력하세요...")
    
    if search_query:
        results = [
            w for w in st.session_state.words
            if search_query.lower() in w['word'].lower() or search_query.lower() in w['meaning'].lower()
        ]
        
        if results:
            st.success(f"{len(results)}개의 결과를 찾았습니다.")
            for word_data in results:
                with st.expander(f"**{word_data['word']}** - {word_data['meaning']}"):
                    st.markdown(f"**뜻:** {word_data['meaning']}")
                    st.markdown(f"**예문:** {word_data['example']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        is_favorite = word_data['word'] in st.session_state.favorites
                        if st.button("⭐ 즐겨찾기" if not is_favorite else "⭐ 즐겨찾기 제거", key=f"search_fav_{word_data['word']}"):
                            if is_favorite:
                                st.session_state.favorites.discard(word_data['word'])
                            else:
                                st.session_state.favorites.add(word_data['word'])
                            st.rerun()
                    with col2:
                        is_learned = word_data['word'] in st.session_state.learned_words
                        if st.button("✅ 학습 완료" if not is_learned else "✅ 완료됨", key=f"search_learn_{word_data['word']}"):
                            if not is_learned:
                                st.session_state.learned_words.add(word_data['word'])
                                st.rerun()
        else:
            st.warning("검색 결과가 없습니다.")
    else:
        st.info("검색어를 입력하세요.")

# 즐겨찾기 페이지
elif page == "⭐ 즐겨찾기":
    st.header("⭐ 즐겨찾기")
    
    if st.session_state.favorites:
        favorite_words = [w for w in st.session_state.words if w['word'] in st.session_state.favorites]
        st.info(f"총 {len(favorite_words)}개의 즐겨찾기 단어가 있습니다.")
        
        for word_data in favorite_words:
            with st.expander(f"**{word_data['word']}** - {word_data['meaning']}"):
                st.markdown(f"**뜻:** {word_data['meaning']}")
                st.markdown(f"**예문:** {word_data['example']}")
                
                if st.button("❌ 즐겨찾기 제거", key=f"remove_fav_{word_data['word']}"):
                    st.session_state.favorites.discard(word_data['word'])
                    st.rerun()
    else:
        st.info("즐겨찾기한 단어가 없습니다. 단어 목록이나 플래시카드에서 ⭐ 버튼을 눌러 즐겨찾기에 추가하세요!")

