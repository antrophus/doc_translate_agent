# 문서 번역 에이전트

Word 문서를 다양한 언어로 번역하는 AI 기반 번역 에이전트입니다.

## 주요 기능

- Word 문서(.docx, .doc) 업로드 및 번역
- 다중 LLM 기반 번역 (OpenAI, Gemini, DeepSeek)
- Failover 메커니즘을 통한 안정적인 번역
- 문서 서식 유지
- 웹 기반 사용자 인터페이스

## 지원 언어

- 중국어 간체
- 영어
- 일본어
- 베트남어
- 태국어
- 인도네시아어

## 설치 방법

1. 저장소 클론
```bash
git clone [repository-url]
cd doc-translate-agent
```

2. Conda 환경 생성 및 활성화
```bash
conda create -n doc_translate python=3.12
conda activate doc_translate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 API 키들을 설정하세요:
```
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

## 실행 방법

```bash
streamlit run src/app.py
```

## 사용 방법

1. 웹 브라우저에서 `http://localhost:8501` 접속
2. "번역할 Word 문서를 업로드하세요" 버튼을 클릭하여 문서 선택
3. 번역할 언어 선택
4. "번역 시작" 버튼 클릭
5. 번역이 완료되면 "번역된 문서 다운로드" 버튼을 클릭하여 결과물 저장

## 라이선스

MIT License 