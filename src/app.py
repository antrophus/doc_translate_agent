import streamlit as st
from translator import DocumentTranslator
import os
from docx import Document
import tempfile
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_text_from_table(table):
    """표에서 텍스트를 추출합니다."""
    text = []
    for row in table.rows:
        row_text = []
        for cell in row.cells:
            if cell.text.strip():
                row_text.append(cell.text.strip())
        if row_text:
            text.append(" | ".join(row_text))
    return "\n".join(text)

def validate_docx(file_content):
    """업로드된 파일이 유효한 Word 문서인지 확인합니다."""
    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name
        
        # 문서 열기 시도
        doc = Document(tmp_file_path)
        
        # 문서 내용 상세 로깅
        total_paragraphs = len(doc.paragraphs)
        total_tables = len(doc.tables)
        non_empty_paragraphs = len([p for p in doc.paragraphs if p.text.strip()])
        
        logger.info(f"문서 검증 - 전체 단락 수: {total_paragraphs}, 표 수: {total_tables}, 내용이 있는 단락 수: {non_empty_paragraphs}")
        
        # 표 내용 로깅
        for i, table in enumerate(doc.tables):
            table_text = extract_text_from_table(table)
            if table_text:
                logger.info(f"표 {i+1} 내용 샘플:\n{table_text[:500]}...")
        
        # 각 단락 내용 로깅
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                logger.info(f"단락 {i+1} 길이: {len(para.text)}, 내용: '{para.text[:100]}...'")
                for j, run in enumerate(para.runs):
                    logger.info(f"  - Run {j+1}: 텍스트: '{run.text}', 글꼴: {run.font.name}")
        
        # 임시 파일 삭제
        os.unlink(tmp_file_path)
        
        return total_tables > 0 or total_paragraphs > 0
    except Exception as e:
        logger.error(f"문서 검증 실패: {str(e)}")
        return False

def main():
    st.title("문서 번역기")
    st.write("Word 문서를 선택한 언어로 번역합니다.")
    
    # 파일 업로드
    uploaded_file = st.file_uploader("번역할 Word 문서를 업로드하세요", type=['docx'])
    
    if uploaded_file is not None:
        # 파일 크기 표시
        file_size = len(uploaded_file.getvalue())
        st.info(f"업로드된 파일 크기: {file_size / 1024:.2f} KB")
        
        # 파일 내용 미리보기
        try:
            # 파일 포인터 초기화
            uploaded_file.seek(0)
            
            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # 문서 열기
            doc = Document(tmp_file_path)
            
            # 문서 내용 확인
            paragraphs = []
            
            # 표 내용 추출
            for table in doc.tables:
                table_text = extract_text_from_table(table)
                if table_text:
                    paragraphs.append(table_text)
            
            # 일반 단락 내용 추출
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
            
            total_paragraphs = len(doc.paragraphs)
            total_tables = len(doc.tables)
            non_empty_content = len(paragraphs)
            
            logger.info(f"문서 미리보기 - 전체 단락 수: {total_paragraphs}, 표 수: {total_tables}, 내용이 있는 섹션 수: {non_empty_content}")
            
            if paragraphs:
                preview_text = "\n\n".join(paragraphs[:5])
                st.text_area("문서 미리보기 (처음 5개 섹션)", preview_text, height=300)
                st.info(f"전체 단락 수: {total_paragraphs}, 표 수: {total_tables}, 내용이 있는 섹션 수: {non_empty_content}")
            else:
                st.warning("문서에 텍스트 내용이 없습니다. 문서가 이미지나 특수 형식으로만 구성되어 있을 수 있습니다.")
                # 문서 구조 정보 표시
                st.info("문서 구조 정보:")
                structure_info = []
                for i, table in enumerate(doc.tables):
                    structure_info.append(f"표 {i+1}: {len(table.rows)}행 x {len(table.columns)}열")
                for i, para in enumerate(doc.paragraphs):
                    structure_info.append(f"단락 {i+1}: 길이={len(para.text)}, 스타일={para.style.name}")
                st.code("\n".join(structure_info))
            
            # 임시 파일 삭제
            os.unlink(tmp_file_path)
            
        except Exception as e:
            logger.error(f"문서 미리보기 실패: {str(e)}")
            st.error(f"문서 미리보기 실패: {str(e)}")
    
    # 번역할 언어 선택
    target_lang = st.selectbox(
        "번역할 언어를 선택하세요",
        ["중국어 간체", "영어", "일본어", "베트남어", "태국어", "인도네시아어"]
    )
    
    if uploaded_file is not None and st.button("번역 시작"):
        try:
            # 파일 검증
            if not validate_docx(uploaded_file.getvalue()):
                st.error("유효하지 않은 Word 문서입니다. 내용이 있는 Word 문서를 업로드해주세요.")
                return
            
            # 임시 파일로 업로드된 파일 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # 번역기 초기화
            translator = DocumentTranslator()
            
            # 진행 상태 표시
            with st.spinner("번역 중입니다..."):
                # 문서 번역
                translated_doc = translator.translate_document(tmp_file_path, target_lang)
                
                # 번역된 문서 저장
                output_filename = f"translated_{uploaded_file.name}"
                output_path = os.path.join("data", output_filename)
                
                # data 디렉토리가 없으면 생성
                os.makedirs("data", exist_ok=True)
                
                # 번역된 문서 저장
                translated_doc.save(output_path)
                st.success(f"번역이 완료되었습니다. 파일이 다음 경로에 저장되었습니다: {output_path}")
                
                # 번역된 파일 다운로드 버튼
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="번역된 문서 다운로드",
                        data=file,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                # 임시 파일 삭제
                os.unlink(tmp_file_path)
                
        except Exception as e:
            logger.error(f"번역 중 오류 발생: {str(e)}")
            st.error(f"번역 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main() 