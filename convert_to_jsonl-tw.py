import os
import json
import csv
from PyPDF2 import PdfFileReader
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QCheckBox


class ConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_folder = None
        self.output_file = None
        self.output_folder = None
        self.single_output = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('文件轉換')

        # 輸入資料夾
        self.input_folder_label = QLabel('輸入資料夾:')
        self.input_folder_button = QPushButton('瀏覽')
        self.input_folder_button.clicked.connect(self.browse_input_folder)

        # 輸出檔案
        self.output_file_label = QLabel('輸出檔案（單一）:')
        self.output_file_button = QPushButton('瀏覽')
        self.output_file_button.clicked.connect(self.browse_output_file)

        # 輸出資料夾
        self.output_folder_label = QLabel('輸出資料夾（多個檔案）:')
        self.output_folder_button = QPushButton('瀏覽')
        self.output_folder_button.clicked.connect(self.browse_output_folder)

        # 單一輸出核取方塊
        self.single_output_checkbox = QCheckBox('合併為單一檔案')

        # 轉換按鈕
        self.convert_button = QPushButton('轉換')
        self.convert_button.clicked.connect(self.convert_files)

        # 佈局
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.input_folder_label)
        layout.addWidget(self.input_folder_button)
        layout.addWidget(self.output_file_label)
        layout.addWidget(self.output_file_button)
        layout.addWidget(self.output_folder_label)
        layout.addWidget(self.output_folder_button)
        layout.addWidget(self.single_output_checkbox)
        layout.addWidget(self.convert_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_input_folder(self):
        self.input_folder = QFileDialog.getExistingDirectory(self, '選擇輸入資料夾')

    def browse_output_file(self):
        self.output_file, _ = QFileDialog.getSaveFileName(self, '選擇輸出檔案', '', 'JSONL 檔案 (*.jsonl)')

    def browse_output_folder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, '選擇輸出資料夾')

    def convert_files(self):
        if self.single_output and self.output_file:
            convert_files(self.input_folder, self.output_file, single_output=True)
        elif self.output_folder:
            convert_files(self.input_folder, self.output_folder)

    def set_single_output(self, checked):
        self.single_output = checked


def txt_to_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = [{'text': line.strip()} for line in lines]

    with open(output_file, 'a', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def csv_to_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    with open(output_file, 'a', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def json_to_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_file, 'a', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def pdf_to_jsonl(input_file, output_file):
    pdf = PdfFileReader(input_file)

    data = []
    for page_num in range(pdf.numPages):
        page = pdf.getPage(page_num)
        text = page.extractText().strip()
        data.append({'text': text})

    with open(output_file, 'a', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def convert_file(input_file, output_file, single_output=False):
    file_ext = os.path.splitext(input_file)[1].lower()

    if file_ext == '.txt':
        txt_to_jsonl(input_file, output_file)
    elif file_ext == '.csv':
        csv_to_jsonl(input_file, output_file)
    elif file_ext == '.json':
        json_to_jsonl(input_file, output_file)
    elif file_ext == '.pdf':
        pdf_to_jsonl(input_file, output_file)

    if single_output:
        os.remove(input_file)


def convert_files(input_folder, output_file, single_output=False):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for file_name in os.listdir(input_folder):
        input_file = os.path.join(input_folder, file_name)
        convert_file(input_file, output_file, single_output)


if __name__ == '__main__':
    app = QApplication([])
    window = ConverterWindow()
    window.show()
    app.exec_()
