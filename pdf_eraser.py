import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import os

class PDFEraser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF 마지막 페이지 삭제 프로그램")
        self.root.geometry("600x350")  # 높이를 약간 늘림
        
        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure('TButton', padding=10)
        
        # 변수 초기화
        self.pdf_path_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.status_var.set("PDF 파일을 선택해주세요")
        self.rename_var = tk.BooleanVar(value=True)  # 파일명 수정 체크박스 변수
        
        self._create_widgets()
        
    def _create_widgets(self):
        """GUI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 파일 선택 버튼
        select_btn = ttk.Button(
            main_frame, 
            text="PDF 파일 선택",
            command=self.select_pdf_file
        )
        select_btn.pack(pady=10)
        
        # 파일 경로 표시 레이블
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=10)
        
        path_label = ttk.Label(
            path_frame,
            textvariable=self.pdf_path_var,
            wraplength=500
        )
        path_label.pack()
        
        # 파일명 수정 체크박스 추가
        rename_check = ttk.Checkbutton(
            main_frame,
            text="파일명에서 마지막 11글자 제거",
            variable=self.rename_var
        )
        rename_check.pack(pady=5)
        
        # 삭제 버튼
        delete_btn = ttk.Button(
            main_frame,
            text="마지막 페이지 삭제",
            command=self.remove_last_page
        )
        delete_btn.pack(pady=10)
        
        # 상태 표시 레이블
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            foreground="blue"
        )
        status_label.pack(pady=10)

    def select_pdf_file(self):
        """PDF 파일 선택 다이얼로그"""
        file_path = filedialog.askopenfilename(
            title="PDF 파일 선택",
            filetypes=[("PDF 파일", "*.pdf")]
        )
        if file_path:
            self.pdf_path_var.set(file_path)
            self.status_var.set("PDF 파일이 선택되었습니다")

    def process_filename(self, filename):
        """파일명 처리 로직"""
        # 확장자 분리
        name, ext = os.path.splitext(filename)
        
        # 파일명 수정이 체크되어 있고, 길이가 충분한 경우에만 처리
        if self.rename_var.get() and len(name) > 11:
            # 마지막 11글자 제거
            name = name[:-11]
        
        # modified_ 접두사 추가 및 확장자 붙이기
        return f"modified_{name}{ext}"

    def remove_last_page(self):
        """PDF 마지막 페이지 삭제 처리"""
        pdf_path = self.pdf_path_var.get()
        
        if not pdf_path or not os.path.isfile(pdf_path):
            messagebox.showerror("오류", "유효한 PDF 파일을 선택해주세요")
            return
            
        try:
            # PDF 파일 열기
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                page_count = len(reader.pages)
                
                # 페이지 수 확인
                if page_count <= 1:
                    messagebox.showwarning(
                        "경고", 
                        "PDF가 1페이지 이하입니다. 삭제할 수 없습니다."
                    )
                    return
                
                # 새 PDF 생성
                writer = PyPDF2.PdfWriter()
                
                # 페이지 복사 (마지막 페이지 제외)
                for i in range(page_count - 1):
                    writer.add_page(reader.pages[i])
                
                # 메타데이터 복사
                if reader.metadata:
                    writer.add_metadata(reader.metadata)
                    
                # 아웃라인(목차) 복사
                try:
                    outlines = reader.outline
                    if outlines:
                        writer.add_outline(outlines)
                except Exception as e:
                    print(f"목차 복사 중 오류: {str(e)}")
                
                # 저장할 파일명 생성
                file_dir = os.path.dirname(pdf_path)
                file_name = os.path.basename(pdf_path)
                new_name = self.process_filename(file_name)
                save_path = os.path.join(file_dir, new_name)
                
                # 새 PDF 저장
                with open(save_path, 'wb') as output:
                    writer.write(output)
                
                self.status_var.set("마지막 페이지 삭제 완료!")
                messagebox.showinfo(
                    "완료", 
                    f"새 PDF가 저장되었습니다:\n{save_path}"
                )
                
        except Exception as e:
            messagebox.showerror("오류", f"PDF 처리 중 오류가 발생했습니다:\n{str(e)}")
            self.status_var.set("오류가 발생했습니다")

    def run(self):
        """프로그램 실행"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFEraser()
    app.run() 