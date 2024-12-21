import sys
import os
import shutil
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QListWidget, QVBoxLayout,
    QHBoxLayout, QFileDialog, QMessageBox, QTextEdit, QLabel, QListView
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QListView, QTreeView

# 定义字幕文件的后缀名
SUBTITLE_EXTENSIONS = ['.srt', '.sub', '.ass', '.ssa']

class SubtitleAdjuster(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("字幕文件调整工具")
        self.resize(900, 700)
        self.selected_files = []
        self.selected_folders = []
        self.init_ui()

    def init_ui(self):
        # 创建按钮
        self.select_files_btn = QPushButton("选择文件")
        self.select_folders_btn = QPushButton("选择文件夹")
        self.start_btn = QPushButton("开始调整")

        # 连接信号和槽
        self.select_files_btn.clicked.connect(self.select_files)
        self.select_folders_btn.clicked.connect(self.select_folders)
        self.start_btn.clicked.connect(self.start_adjustment)

        # 创建列表展示区域
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.NoSelection)

        # 创建日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        # 布局设置
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_files_btn)
        button_layout.addWidget(self.select_folders_btn)
        button_layout.addWidget(self.start_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(QLabel("已选择的文件和文件夹:"))
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(QLabel("操作日志:"))
        main_layout.addWidget(self.log_text)

        self.setLayout(main_layout)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择字幕文件", "",
            "Subtitle Files (*.srt *.sub *.ass *.ssa);;All Files (*)"
        )
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    self.list_widget.addItem(file)
                    self.log(f"选择字幕文件: {file}")

    def select_folders(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        # 设置为可以多选
        for view in dialog.findChildren((QListView, QTreeView)):
            view.setSelectionMode(QAbstractItemView.MultiSelection)
        if dialog.exec_():
            folders = dialog.selectedFiles()
            for folder in folders:
                if folder not in self.selected_folders:
                    self.selected_folders.append(folder)
                    self.list_widget.addItem(folder)
                    self.log(f"选择文件夹: {folder}")

    def log(self, message):
        self.log_text.append(message)
        self.log_text.ensureCursorVisible()
        QApplication.processEvents()

    def extract_se_pattern(self, filename):
        """
        从文件名中提取SxxExx或sxxexx模式的字符串，并返回大写形式
        """
        pattern = re.compile(r'[Ss]\d{2}[Ee]\d{2}')
        match = pattern.search(filename)
        if match:
            return match.group(0).upper()
        return None

    def is_subtitle_file(self, filename):
        _, ext = os.path.splitext(filename)
        return ext.lower() in SUBTITLE_EXTENSIONS

    def start_adjustment(self):
        # 收集所有字幕文件
        all_subtitle_files = set()

        # 添加选中的字幕文件
        for file in self.selected_files:
            if self.is_subtitle_file(file):
                all_subtitle_files.add(os.path.abspath(file))
            else:
                self.log(f"警告: 选中的文件 '{file}' 不是字幕文件，已忽略。")

        # 遍历选中的文件夹，收集所有字幕文件
        for folder in self.selected_folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if self.is_subtitle_file(file):
                        full_path = os.path.abspath(os.path.join(root, file))
                        all_subtitle_files.add(full_path)

        if not all_subtitle_files:
            QMessageBox.warning(self, "警告", "没有找到任何字幕文件。")
            return

        # 收集所有非字幕文件
        all_non_subtitle_files = set()
        for folder in self.selected_folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if not self.is_subtitle_file(file):
                        full_path = os.path.abspath(os.path.join(root, file))
                        all_non_subtitle_files.add(full_path)

        self.log("开始调整字幕文件...")

        for subtitle_file in all_subtitle_files:
            subtitle_dir, subtitle_name = os.path.split(subtitle_file)
            subtitle_base, subtitle_ext = os.path.splitext(subtitle_name)
            self.log(f"处理字幕文件: {subtitle_file}")

            # 检查是否存在同名的非字幕文件
            same_name_non_sub = False
            for non_sub_file in all_non_subtitle_files:
                non_sub_dir, non_sub_name = os.path.split(non_sub_file)
                non_sub_base, _ = os.path.splitext(non_sub_name)
                if non_sub_base.lower() == subtitle_base.lower():
                    same_name_non_sub = True
                    self.log(f"发现同名的非字幕文件: {non_sub_file}，跳过此字幕文件。")
                    break
            if same_name_non_sub:
                continue  # 跳过此字幕文件

            # 提取字幕文件中的SxxExx模式
            se_pattern = self.extract_se_pattern(subtitle_name)
            if not se_pattern:
                self.log(f"字幕文件 '{subtitle_name}' 中未找到SxxExx模式，跳过。")
                continue

            # 查找匹配的非字幕文件
            matched = False
            for non_sub_file in all_non_subtitle_files:
                non_sub_dir, non_sub_name = os.path.split(non_sub_file)
                non_sub_se_pattern = self.extract_se_pattern(non_sub_name)
                if non_sub_se_pattern and non_sub_se_pattern == se_pattern:
                    matched = True
                    # 构造新的字幕文件名
                    new_subtitle_name = os.path.splitext(non_sub_name)[0] + subtitle_ext
                    new_subtitle_path = os.path.join(non_sub_dir, new_subtitle_name)

                    # 检查目标文件是否已存在
                    if os.path.exists(new_subtitle_path):
                        self.log(f"目标文件 '{new_subtitle_path}' 已存在，跳过复制。")
                        continue

                    try:
                        # 检查 "ori" 文件夹是否存在，如果不存在则创建
                        ori_folder_path = os.path.join(os.path.dirname(subtitle_file), "ori")
                        if not os.path.exists(ori_folder_path):
                            os.makedirs(ori_folder_path)
                            self.log(f"创建文件夹: {ori_folder_path}")

                        # 重命名原字幕文件，并移动到 "ori" 文件夹
                        ori_subtitle_path = os.path.join(ori_folder_path,
                                                         os.path.basename(subtitle_file) + "-ori" + subtitle_ext)
                        if not os.path.exists(ori_subtitle_path):
                            os.rename(subtitle_file, ori_subtitle_path)
                            self.log(f"重命名并移动原字幕文件到 'ori' 文件夹: {ori_subtitle_path}")
                        else:
                            self.log(f"'ori' 文件夹中的备份文件 '{ori_subtitle_path}' 已存在，跳过重命名。")

                        # 复制字幕文件到目标位置
                        shutil.copy2(ori_subtitle_path, new_subtitle_path)
                        self.log(f"复制并重命名字幕文件为: {new_subtitle_path}")
                    except Exception as e:
                        self.log(f"处理字幕文件 '{subtitle_file}' 时出错: {str(e)}")
            if not matched:
                self.log(f"字幕文件 '{subtitle_name}' 未找到匹配的非字幕文件，跳过。")

        self.log("字幕文件调整完成。")
        QMessageBox.information(self, "完成", "所有字幕文件已处理完毕。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubtitleAdjuster()
    window.show()
    sys.exit(app.exec_())
