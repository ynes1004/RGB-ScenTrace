import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import platform

# 1. 한글 폰트 설정 (폰트 깨짐 방지)
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic' # 윈도우용 맑은 고딕
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'   # 맥용 애플고딕
plt.rcParams['axes.unicode_minus'] = False        # 마이너스 기호 깨짐 방지

# 2. 페이지 설정 및 다크 테마 커스텀
st.set_page_config(page_title="ScenTrace | RGB Team", layout="centered")

st.markdown("""
    <style>
    /* 전체 배경: 블랙 / 글자: 화이트 */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* 사이드바 가독성 개선 */
    section[data-testid="stSidebar"] {
        background-color: #050505 !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p, 
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    /* 제목 스타일: 노란색(Gold) */
    .main-title {
        color: #F1C40F;
        font-family: 'serif';
        font-weight: 800;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* RGB 팀명: 화이트로 통일 */
    .rgb-logo { 
        text-align: center; 
        font-weight: bold; 
        font-size: 1.1rem; 
        letter-spacing: 5px; 
        color: #FFFFFF; 
        margin-bottom: 20px; 
    }

    /* 컨텐츠 박스 */
    .content-box {
        background-color: #111111;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #444444;
        margin-top: 25px;
        color: #FFFFFF;
    }
    .guide-text { line-height: 1.9; color: #FFFFFF; font-size: 15px; }

    /* 사이드바 내 버튼 스타일 (화이트 버튼) */
    div.stButton > button:first-child {
        width: 100%;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 5px;
        font-weight: bold;
        border: none;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 섹션 (RGB 화이트 통일)
st.markdown("<div class='rgb-logo'>RGB TEAM</div>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>ScenTrace Match Guide</h1>", unsafe_allow_html=True)
st.write("")

# 4. 사이드바: 입력 데이터 및 분석 버튼
st.sidebar.header("👤 Personal Bio-Metrics")
st.sidebar.write("생체 데이터를 조절한 후 분석을 시작하세요.")

skin_val = st.sidebar.select_slider("피부 타입 (Skin Type)", options=["건성", "중성", "지성"], value="중성")
temp_level = st.sidebar.select_slider("현재 체온 (Temperature)", options=["낮음", "보통", "높음"], value="보통")
sebum_level = st.sidebar.select_slider("피지 분비량 (Sebum)", options=["적음", "보통", "많음"], value="보통")

# 🚀 피지 분비량 바로 밑에 버튼 추가
analyze_btn = st.sidebar.button("시뮬레이션 분석 시작")

st.sidebar.divider()
st.sidebar.caption("Data calibrated by RGB Lab.")

# 5. 알고리즘 계산 로직
f_temp = {"낮음": 0.85, "보통": 1.0, "높음": 1.35}[temp_level]
f_sebum = {"적음": 0.75, "보통": 1.0, "많음": 1.45}[sebum_level]
f_skin = {"건성": 1.25, "중성": 1.0, "지성": 0.85}[skin_val]

t = np.linspace(0, 12, 100)
k_total = 0.2 * f_temp * f_skin / f_sebum
i_total = 100 * np.exp(-k_total * t)

# 6. 결과 출력 제어
if analyze_btn:
    # 7. 그래프 시각화 (화이트 라인)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#000000')
    ax.set_facecolor('#000000')
    ax.plot(t, i_total, color='white', linewidth=3)
    ax.fill_between(t, i_total, color='white', alpha=0.1)

    ax.set_ylabel("발향 강도 (%)")
    ax.set_xlabel("시간 (Hours)")
    ax.set_title(f"Simulation: {skin_val} / 체온 {temp_level} / 피지 {sebum_level}", fontsize=14, pad=20)
    ax.grid(True, linestyle=':', alpha=0.2)
    st.pyplot(fig)
    
    # 8. 그래프 하단 4줄 핵심 가이드
    st.markdown(f"""
    <div class='content-box'>
        <p class='guide-text'>
        💡 <b>그래프 해석 및 분석 결과</b><br>
        1. 이 그래프는 당신의 <b>피부 타입, 체온, 유분</b> 환경에 따른 향기의 시간별 감쇄 변화를 시뮬레이션한 결과입니다.<br>
        2. 흰색 선의 높이는 전체적인 발향 강도를 의미하며, 아래로 내려갈수록 향기가 연해짐을 뜻합니다.<br>
        3. 현재 입력하신 데이터에 따르면, 초기 발향 이후 당신의 고유한 살냄새와 섞여 안정적인 잔향 궤도에 진입합니다.<br>
        4. 당신의 상태에서 이 향수는 약 <b>{8 * (1/f_skin * f_sebum):.1f}시간</b> 동안 피부 위에 머물 것으로 예측됩니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("👈 사이드바의 슬라이더를 조절하고 '시뮬레이션 분석 시작' 버튼을 눌러주세요.")

# 9. ScenTrace 핵심 용어 정의
st.write("")
st.write("---")
st.subheader("📑 ScenTrace 주요 정의")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**1. 예상 지속 시간 (Longevity)** 향료 분자가 피부의 피지(Sebum)와 결합하여 고착되는 시간입니다. 유분이 있는 피부일수록 향기가 더 오래 유지됩니다.")
with col2:
    st.markdown("**2. 초기 발향력 (Projection)** 체온(Temperature) 에너지가 향기를 공기 중으로 확산시키는 힘입니다. 체온이 높을수록 초기 발향은 강렬해집니다.")

# 10. 푸터
st.divider()
st.caption("© 2026 L'Oreal Brandstorm Project | Developed by Team RGB")