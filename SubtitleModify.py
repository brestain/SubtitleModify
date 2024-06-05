import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QMessageBox
import pysubs2
import os

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

        # 显示选择的文件路径
        self.label_file = QLabel('请选择一个字幕文件')
        layout.addWidget(self.label_file)

        # 输入时间偏移
        self.input_time = QLineEdit()
        self.input_time.setPlaceholderText('输入时间偏移量（秒，可以是负数）')
        layout.addWidget(self.input_time)

        # 按钮：应用时间偏移
        self.btn_apply = QPushButton('应用时间偏移')
        self.btn_apply.clicked.connect(self.applyOffset)
        layout.addWidget(self.btn_apply)

        self.setLayout(layout)
        self.resize(400, 200)
        self.setWindowTitle('字幕时间偏移调整器')

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择字幕文件", "",
                                                  "Subtitle Files (*.srt *.ass);;All Files (*)", options=options)
        if fileName:
            self.label_name = os.path.basename(fileName)
            self.label_file.setText(fileName)

    def applyOffset(self):
        file_path = self.label_file.text()
        if not file_path or file_path.startswith('请选择'):
            QMessageBox.warning(self, '错误', '请先选择一个字幕文件')
            return

        try:
            offset = float(self.input_time.text())
        except ValueError:
            QMessageBox.warning(self, '错误', '时间偏移量必须是一个数字')
            return

        confirm_msg = QMessageBox()
        confirm_msg.setIcon(QMessageBox.Question)
        confirm_msg.setWindowTitle('确认时间偏移')
        confirm_msg.setText(f'确定要将字幕时间偏移 {offset} 秒吗？')
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = confirm_msg.exec_()
        if retval == QMessageBox.Yes:
            self.adjustSubtitles(file_path, offset)

    def adjustSubtitles(self, file_path, offset):
        subs = pysubs2.load(file_path)
        subs.shift(s=offset)
        file_extension = os.path.splitext(file_path)[1]  # 获取文件扩展名
        new_file_path = f"{file_path[:-len(file_extension)]} {offset}{file_extension}"
        subs.save(new_file_path)
        QMessageBox.information(self, '完成', f'已保存调整后的字幕文件到 {new_file_path}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SubtitleAdjuster()
    ex.show()
    sys.exit(app.exec_())
