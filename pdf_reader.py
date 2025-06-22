import os
import PyPDF2
import pdfplumber
from typing import List, Dict, Any, Union, Optional


class PDFReader:
    """
    PDF 파일을 페이지 단위로 읽어오는 클래스
    """
    
    def __init__(self, pdf_path: str):
        """
        PDFReader 클래스 초기화
        
        Args:
            pdf_path (str): PDF 파일 경로
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        
        self.pdf_path = pdf_path
    
    def read_pages_with_pypdf2(self) -> List[str]:
        """
        PyPDF2 라이브러리를 사용하여 PDF 페이지 내용을 읽어옵니다.
        텍스트 추출에 최적화되어 있으나 레이아웃 정보는 유지되지 않습니다.
        
        Returns:
            List[str]: 각 페이지 텍스트를 담은 리스트
        """
        pages = []
        
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            for page_num in range(total_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                pages.append(text)
                
        return pages
    
    def read_pages_with_pdfplumber(self) -> List[Dict[str, Any]]:
        """
        pdfplumber 라이브러리를 사용하여 PDF 페이지 내용을 읽어옵니다.
        텍스트, 테이블, 이미지 등의 정보를 더 정교하게 추출할 수 있습니다.
        
        Returns:
            List[Dict[str, Any]]: 각 페이지 정보를 담은 딕셔너리 리스트
                - 'text': 페이지 전체 텍스트
                - 'page_number': 페이지 번호 (1부터 시작)
                - 'width': 페이지 너비
                - 'height': 페이지 높이
        """
        pages_info = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                page_info = {
                    'text': text,
                    'page_number': i + 1,  # 1-based page numbering
                    'width': page.width,
                    'height': page.height
                }
                pages_info.append(page_info)
                
        return pages_info
    
    def extract_text_by_page_range(self, start_page: int = 1, end_page: Optional[int] = None) -> List[str]:
        """
        특정 페이지 범위의 텍스트를 추출합니다.
        
        Args:
            start_page (int): 시작 페이지 (1부터 시작)
            end_page (Optional[int]): 끝 페이지, None이면 마지막 페이지까지
            
        Returns:
            List[str]: 지정된 페이지 범위의 텍스트 리스트
        """
        pages = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            # 페이지 범위 확인 및 조정
            total_pages = len(pdf.pages)
            
            if start_page < 1:
                start_page = 1
                
            if end_page is None or end_page > total_pages:
                end_page = total_pages
                
            # 0-based 인덱싱을 위해 조정
            start_idx = start_page - 1
            end_idx = end_page
            
            for i in range(start_idx, end_idx):
                page = pdf.pages[i]
                text = page.extract_text()
                pages.append(text)
                
        return pages
    
    def extract_tables_by_page(self, page_num: int) -> List[List[List[str]]]:
        """
        특정 페이지에서 표(테이블)를 추출합니다.
        
        Args:
            page_num (int): 페이지 번호 (1부터 시작)
            
        Returns:
            List[List[List[str]]]: 추출된 테이블 목록
        """
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            if page_num < 1 or page_num > total_pages:
                raise ValueError(f"유효하지 않은 페이지 번호: {page_num}. 총 페이지 수: {total_pages}")
            
            # 0-based 인덱싱을 위해 조정
            page_idx = page_num - 1
            page = pdf.pages[page_idx]
            
            tables = page.extract_tables()
            return tables


def main():
    """
    PDFReader 클래스 사용 예제
    """
    # 사용 예제를 위한 PDF 파일 경로 설정
    # pdf_path = "example.pdf" # 실제 PDF 파일 경로로 변경하세요
    
    # 아래 주석을 해제하고 실제 PDF 파일 경로를 입력하여 테스트할 수 있습니다
    """
    try:
        pdf_path = "example.pdf"  # 실제 PDF 파일 경로로 변경하세요
        reader = PDFReader(pdf_path)
        
        # PyPDF2로 모든 페이지 읽기
        pages_pypdf2 = reader.read_pages_with_pypdf2()
        print(f"PyPDF2로 읽은 총 페이지 수: {len(pages_pypdf2)}")
        print("첫 번째 페이지 내용 (PyPDF2):")
        print(pages_pypdf2[0][:500] + "...\n")
        
        # pdfplumber로 모든 페이지 읽기
        pages_pdfplumber = reader.read_pages_with_pdfplumber()
        print(f"pdfplumber로 읽은 총 페이지 수: {len(pages_pdfplumber)}")
        print("첫 번째 페이지 정보 (pdfplumber):")
        print(f"페이지 크기: {pages_pdfplumber[0]['width']} x {pages_pdfplumber[0]['height']}")
        print(f"페이지 내용: {pages_pdfplumber[0]['text'][:500]}...\n")
        
        # 특정 페이지 범위 읽기 (예: 2-4 페이지)
        specific_pages = reader.extract_text_by_page_range(2, 4)
        print(f"페이지 2-4 추출 결과: {len(specific_pages)} 페이지")
        
        # 특정 페이지에서 테이블 추출 (예: 1페이지)
        tables = reader.extract_tables_by_page(1)
        print(f"1페이지에서 발견된 테이블 수: {len(tables)}")
        if tables:
            print("첫 번째 테이블 내용:")
            for row in tables[0]:
                print(row)
    
    except FileNotFoundError as e:
        print(f"오류: {e}")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
    """


if __name__ == "__main__":
    main()
