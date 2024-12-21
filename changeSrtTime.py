import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QMessageBox, QScrollArea, QHBoxLayout, QTextEdit
import pysubs2
import os
import chardet
import codecs

class SubtitleAdjuster(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 按钮：选择字幕文件
        self.btn_open = QPushButton('选择字幕文件')
        self.btn_open.clicked.connect(self.openFileDialog)
        layout.addWidget(self.btn_open)

        # 文件显示区域 + 滚动条
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.label_file = QTextEdit('请选择字幕文件')
        self.label_file.setReadOnly(True)
        scroll_area.setWidget(self.label_file)
        layout.addWidget(scroll_area)

        # 输入时间偏移
        self.input_time = QLineEdit()
        self.input_time.setPlaceholderText('输入时间偏移量（秒，可以是负数）')
        layout.addWidget(self.input_time)

        # 按钮：应用时间偏移
        self.btn_apply = QPushButton('应用时间偏移')
        self.btn_apply.clicked.connect(self.applyOffset)
        layout.addWidget(self.btn_apply)

        # # 清空已选中文件按钮
        # self.btn_clear = QPushButton('清空选择')
        # self.btn_clear.clicked.connect(self.clearSelection)
        # layout.addWidget(self.btn_clear)

        self.setLayout(layout)
        self.setFixedWidth(400)  # 限制窗口宽度
        self.setWindowTitle('字幕时间偏移调整器')

    def openFileDialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "选择字幕文件", "",
                                                "Subtitle Files (*.srt *.ass);;All Files (*)", options=options)
        if files:
            file_names = ', '.join([os.path.basename(file) for file in files])
            self.label_file.setText('; '.join(files))  # Save all file paths separated by semicolon

    def applyOffset(self):
        file_paths = self.label_file.toPlainText().split('; ')
        if not file_paths or file_paths[0].startswith('请选择'):
            QMessageBox.warning(self, '错误', '请先选择一个或多个字幕文件')
            return

        try:
            offset = float(self.input_time.text())
        except ValueError:
            QMessageBox.warning(self, '错误', '时间偏移量必须是一个数字')
            return

        for file_path in file_paths:
            if file_path:
                self.adjustSubtitles(file_path, offset)

        QMessageBox.information(self, '完成', '所有选定的字幕文件已经调整完成。')

    def adjustSubtitles(self, file_path, offset):
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            encoding = chardet.detect(raw_data)['encoding']

        if encoding != 'utf-8':
            with codecs.open(file_path, 'r', encoding=encoding) as file:
                content = file.read()

            with codecs.open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

        subs = pysubs2.load(file_path)
        subs.shift(s=offset)
        file_extension = os.path.splitext(file_path)[1]
        new_file_path = f"{file_path[:-len(file_extension)]}{file_extension}"
        new_file_path_ori = f"{file_path[:-len(file_extension)]}-ori{file_extension}"
        os.rename(file_path, new_file_path_ori)
        subs.save(new_file_path)

    def clearSelection(self):
        self.label_file.setText('请选择字幕文件')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SubtitleAdjuster()
    ex.show()
    sys.exit(app.exec_())
