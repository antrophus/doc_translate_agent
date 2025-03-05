import streamlit as st

def apply_custom_styles():
    """커스텀 스타일을 적용합니다."""
    st.markdown("""
        <style>
        /* 모바일 최적화 */
        @media (max-width: 768px) {
            .stButton>button {
                width: 100%;
                margin: 5px 0;
            }
            .stSelectbox {
                width: 100%;
            }
            .stFileUploader {
                width: 100%;
            }
            .stTextArea {
                width: 100%;
            }
        }
        
        /* 전체적인 스타일 */
        .main {
            padding: 1rem;
        }
        
        /* 제목 스타일 */
        .stTitle {
            color: #1E3A8A;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        
        /* 파일 업로더 스타일 */
        .stFileUploader {
            border: 2px dashed #4A90E2;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* 버튼 스타일 */
        .stButton>button {
            background-color: #4A90E2;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #357ABD;
            transform: translateY(-2px);
        }
        
        /* 진행 상태 표시 스타일 */
        .stProgress {
            margin: 1rem 0;
        }
        
        /* 상태 메시지 스타일 */
        .stSuccess {
            background-color: #D4EDDA;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .stError {
            background-color: #F8D7DA;
            color: #721C24;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* 미리보기 영역 스타일 */
        .stTextArea {
            border: 1px solid #E0E0E0;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* 다운로드 버튼 스타일 */
        .download-button {
            background-color: #28A745;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            margin-top: 1rem;
        }
        
        .download-button:hover {
            background-color: #218838;
        }
        </style>
    """, unsafe_allow_html=True)

def create_mobile_friendly_layout():
    """모바일 친화적인 레이아웃을 생성합니다."""
    # 페이지 설정
    st.set_page_config(
        page_title="문서 번역기",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 스타일 적용
    apply_custom_styles()
    
    # 컨테이너 생성
    container = st.container()
    
    return container 