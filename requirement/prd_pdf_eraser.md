
# 📝 **Product Requirements Document (PRD): PDF 마지막 페이지 삭제 GUI 프로그램**

## **Project Overview (프로젝트 개요):**

이 프로젝트는 사용자가 **PDF 파일의 마지막 페이지를 손쉽게 삭제**할 수 있는 GUI 프로그램을 개발하는 것을 목표로 합니다. 사용자는 **파일 탐색기**를 통해 PDF 파일을 선택하고, 버튼을 클릭하여 **변경된 PDF 파일을 저장**할 수 있습니다.

이를 통해 터미널 명령어 없이도 **직관적인 GUI 환경**에서 PDF 파일을 관리할 수 있으며, 반복적인 수작업을 줄이고 생산성을 높일 수 있습니다.

---

## **Core Functionalities (핵심 기능):**

1. **PDF 파일 선택**: 파일 탐색기에서 PDF 파일을 선택할 수 있는 기능을 제공합니다.
2. **마지막 페이지 삭제**: 선택한 PDF 파일의 **마지막 페이지**를 삭제하고, 새로운 PDF 파일로 저장합니다.
3. **변환된 PDF 저장**: 수정된 PDF 파일을 사용자가 원하는 경로에 저장할 수 있도록 지원합니다.
4. **실시간 상태 표시**: 작업 진행 상태(파일 선택, 변환 완료 등)를 **라벨**로 실시간 표시합니다.

---

## **Doc (문서):**

### **사용 기술 스택:**

1. **Frontend (GUI)**: Tkinter
    
    - Tkinter를 사용하여 **간단하고 직관적인 GUI** 인터페이스를 구축합니다.
2. **Backend (PDF 처리)**: PyPDF2
    
    - PyPDF2 라이브러리를 사용하여 **PDF 파일의 마지막 페이지를 삭제**하는 로직을 구현합니다.
3. **Python 패키지:**
    
    - **PyPDF2**: PDF 파일 읽기 및 쓰기를 위한 필수 라이브러리.
    - **Tkinter**: Python 내장 GUI 라이브러리.
    - **os**: 파일 경로 관리에 사용.

---

## **GUI Layout:**

1. **파일 선택 버튼**: PDF 파일을 선택할 수 있는 버튼.
2. **삭제 버튼**: 마지막 페이지를 삭제하고, 변환된 PDF 파일을 저장하는 버튼.
3. **상태 표시 라벨**: 파일 처리 상태(예: "PDF 파일 선택됨", "변환 완료")를 나타냅니다.

---

## **Current File Structure (현재 파일 구조):**

bash



예시 코드 

import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os

def select_pdf_file():
    """PDF 파일을 선택하는 파일 다이얼로그를 연다."""
    file_path = filedialog.askopenfilename(
        title="PDF 파일 선택",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if file_path:
        pdf_path_var.set(file_path)

def remove_last_page():
    """PyPDF2를 사용하여 선택한 PDF의 마지막 페이지를 삭제한 후 새 PDF로 저장한다."""
    pdf_path = pdf_path_var.get()
    
    # PDF가 정상적으로 선택되지 않았을 경우 처리
    if not pdf_path or not os.path.isfile(pdf_path):
        messagebox.showerror("오류", "유효한 PDF 파일을 선택하세요.")
        return

    # PDF 열기
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)

            # 페이지가 1장 이하라면 마지막 페이지 삭제 불가 처리
            if num_pages <= 1:
                messagebox.showwarning("경고", "페이지가 1장 이하인 경우 마지막 페이지를 삭제할 수 없습니다.")
                return

            # 마지막 페이지 삭제
            # PyPDF2 버전에 따라 remove() 등을 통해 직접 제거할 수도 있음
            writer = PyPDF2.PdfWriter()
            for page_num in range(num_pages - 1):  # 마지막 페이지를 제외하고 순회
                writer.add_page(reader.pages[page_num])
            
        # 새 파일명 지정 및 저장(원본 파일과 구분)
        new_pdf_path = pdf_path.replace(".pdf", "_modified.pdf")
        with open(new_pdf_path, 'wb') as out:
            writer.write(out)

        messagebox.showinfo("완료", f"마지막 페이지를 삭제한 PDF가 생성되었습니다.\n\n{new_pdf_path}")

    except Exception as e:
        messagebox.showerror("오류", f"PDF 처리 중 오류가 발생했습니다.\n{e}")

# 메인 윈도우 생성
root = tk.Tk()
root.title("PDF 마지막 페이지 삭제")

# PDF 파일 경로 표시용 문자열 변수
pdf_path_var = tk.StringVar()

# PDF 파일 선택 버튼
btn_select = tk.Button(root, text="PDF 파일 선택", command=select_pdf_file)
btn_select.pack(pady=10)

# 선택된 파일 경로 표시용 라벨
lbl_path = tk.Label(root, textvariable=pdf_path_var, width=80, anchor="w")
lbl_path.pack(padx=10)

# 마지막 페이지 삭제 실행 버튼
btn_remove = tk.Button(root, text="마지막 페이지 삭제", command=remove_last_page)
btn_remove.pack(pady=10)

root.mainloop()
