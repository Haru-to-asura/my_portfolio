import streamlit as st
from openai import OpenAI

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="김민석의 포트폴리오",
    page_icon="🤖",
    layout="wide"
)

# 2. AI에게 주입할 '나의 정보' (시스템 프롬프트)
# 면접관이 물어봤을 때 AI가 참고할 핵심 데이터입니다.
SYSTEM_PROMPT = """
당신은 메카트로닉스 공학 전공생 '김민석'의 AI 페르소나입니다.
방문자(면접관, 채용 담당자)의 질문에 대해 김민석 본인인 것처럼 예의 바르고 자신감 있게, 기술적인 내용은 구체적으로 답변하세요.

[기본 정보]
- 전공: 한국공학대학교 메카트로닉스 전공 (4학년)
- 핵심 역량: 임베디드 시스템, 로봇 제어(PID, Motor), 안드로이드 앱 개발(Kotlin), 드론 제작
- 성격: 문제를 끝까지 파고들어 해결하는 집요함, 팀 프로젝트 리더십 보유

[주요 프로젝트 1: GPS 기반 불법 주정차 단속 드론]
- 개요: PX4 펌웨어 기반의 자율주행 드론 제작 (F450 프레임 활용)
- 핵심 기술: 
    1. 통신 모듈 직접 제작: ESP-01 모듈에 납땜 및 쇼트를 주어 MAVLink용 펌웨어를 직접 굽고 FC와 통신 성공 (기성품 대신 직접 구현)
    2. 제어: PID 튜닝을 위해 드론을 줄로 묶어 안전하게 고정한 상태에서 수동으로 게인 값을 조절하며 비행 안정성 확보
- 진행 중인 작업:
    1. 2축 짐벌 설계 및 제작 (3D 프린팅 출력, Nucleo 보드와 뎁스 카메라 IMU 센서를 활용한 자동 제어 예정)
    2. 컴퓨터 비전(OpenCV)을 활용한 번호판 자동 인식 및 서버 전송 기능 개발 중

[주요 프로젝트 2: 복지관 관리 로봇 'Via Temi']
- 성과: 2025 지역사회참여교과 총장상(대상 격) 수상, 수강후기 공모전 최우수상(2등) 수상
- 역할: 팀장 (6명 팀 리딩), 하드웨어 제어 및 전체 시스템 통합
- 핵심 기능:
    1. Temi 로봇의 자율주행(SLAM) 및 내비게이션 기능 활용
    2. 앱 개발: Kotlin과 Firebase를 연동하여 자체 예약 및 관제 앱 제작
    3. 하드웨어 확장: Arduino와 Firebase를 연동하여 로봇에 부착된 '간식 제공 박스' 등의 추가 하드웨어 제어
- 에피소드: 시흥장곡종합사회복지관에서 실제 필드 테스트 진행. 어르신들을 위한 직관적인 UI/UX 설계.

[답변 스타일]
- 기술적인 질문에는 사용한 보드(Nucleo, ESP-01), 언어(C++, Kotlin, Python), 통신 방식(MAVLink, Firebase DB)을 구체적으로 언급할 것.
- 모르는 내용이 나오면 "그 부분은 아직 경험해보지 못했지만, 현재 진행 중인 드론 프로젝트에서 비전 처리를 공부하며 관련 역량을 키우고 있습니다."라고 답변할 것.
"""

# 3. 사이드바 (프로필 영역)
with st.sidebar:
    # 프로필 사진이 없으면 생략 가능
    try:
        st.image("images/profile.jpg", width=150)
    except:
        st.write("📷 (프로필 사진을 images/profile.jpg로 넣어주세요)")
        
    st.title("김민석")
    st.caption("메카트로닉스 엔지니어링 / Robot Developer")
    
    st.write("---")
    st.write("📧 email@address.com") # 본인 이메일로 수정
    st.write("🐙 GitHub Link") # 깃허브 링크 추가
    
    st.write("---")
    # API 키 처리 (자동 감지)
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
    else:
        api_key = st.text_input("OpenAI API Key", type="password")
        
    if not api_key:
        st.info("⚠️ 챗봇을 사용하려면 API 키가 필요합니다.")

# 4. 메인 화면 구성 (탭 방식)
st.title("안녕하세요! 로봇 공학도 김민석입니다 🤖")
st.write("하드웨어 제어부터 소프트웨어 통합까지, **직접 만들고 부딪히며 배우는 엔지니어**입니다.")

tab1, tab2, tab3 = st.tabs(["🚀 주요 프로젝트", "🏆 수상 및 활동", "💬 AI 챗봇 인터뷰"])

# --- 탭 1: 프로젝트 소개 ---
with tab1:
    st.header("1. 자율주행 주정차 단속 드론 (진행 중)")
    col1, col2 = st.columns([1, 1.5])
    with col1:
        try:
            st.image("images/drone.jpg", caption="직접 제작한 F450 기반 드론", use_container_width=True)
        except:
            st.info("이미지 준비중 (images/drone.jpg)")
    with col2:
        st.write("""
        **"기성품을 쓰기보다 원리를 이해하고 직접 만드는 것을 선호합니다."**
        
        * **MCU/FC:** Pixhawk 4 (PX4 Firmware)
        * **Telemetry:** ESP-01 모듈 커스텀 (MAVLink 펌웨어 플래싱 및 납땜)
        * **Frame:** F450 Kit
        * **주요 성과:**
            * 고가의 텔레메트리 모듈 대신 ESP-01을 해킹하여 와이파이 통신 구현 성공
            * '줄 묶음 테스트'를 통한 수동 PID 게인 튜닝으로 비행 안정성 확보
        * **Future Plan:** Nucleo 보드 기반 2축 짐벌 제어 및 번호판 인식 비전 시스템 탑재 예정
        """)
        
    st.divider()
    
    st.header("2. 복지관 관리 로봇 'Via Temi'")
    col3, col4 = st.columns([1.5, 1])
    with col4:
        try:
            st.image("images/temi_robot.jpg", caption="시흥장곡종합사회복지관 실증 테스트", use_container_width=True)
        except:
            st.info("이미지 준비중 (images/temi_robot.jpg)")
    with col3:
        st.write("""
        **"기술을 넘어 사람을 향하는 로봇을 만듭니다."**
        
        시흥장곡종합사회복지관과 협력하여 어르신들을 위한 안내 및 예약 관리 로봇을 개발했습니다.
        
        * **Role:** 팀장 (PM), HW/SW 통합 제어
        * **Tech Stack:** Temi SDK, Android (Kotlin), Firebase, Arduino
        * **Key Feature:**
            * **자율주행:** 복지관 맵핑 및 길 안내 기능
            * **IoT 연동:** 아두이노로 제어되는 '간식 박스'를 로봇에 부착, 앱과 연동하여 특정 미션 수행 시 간식 제공
            * **앱 개발:** 어르신 맞춤형 UI/UX 예약 어플리케이션 개발
        """)

# --- 탭 2: 수상 경력 ---
with tab2:
    st.header("🏆 Awards")
    st.info("""
    **2025 지역사회참여교과 성과발표회 - 총장상 (대상)** 한국공학대학교 | 복지관 관리 로봇 'Via Temi' 프로젝트의 기술적 완성도와 사회적 기여도 인정
    """)
    
    st.success("""
    **2025 지역사회참여교과 수강후기 공모전 - 최우수상 (2등)** 한국공학대학교 | 엔지니어로서 현장에서 느낀 점과 기술적 성장을 담은 에세이 수상
    """)
    
    st.write("---")
    try:
        st.image("images/temi_team.jpg", caption="팀 'Via Temi' 단체 사진", width=500)
    except:
        pass

# --- 탭 3: AI 챗봇 ---
with tab3:
    st.subheader("🤖 AI 김민석에게 물어보세요!")
    st.markdown("Try asking: **'드론 만들 때 뭐가 제일 힘들었어?'** or **'Temi 로봇 프로젝트에서 어떤 역할을 했어?'**")

    # 채팅 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    # 이전 대화 출력 (시스템 메시지 제외)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("질문을 입력해주세요..."):
        if not api_key:
            st.error("⚠️ 먼저 왼쪽 사이드바에 OpenAI API Key를 입력해주세요!")
        else:
            # 사용자 메시지 UI 표시 및 저장
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # OpenAI API 호출
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                bot_reply = response.choices[0].message.content

                # 봇 응답 UI 표시 및 저장
                with st.chat_message("assistant"):
                    st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")