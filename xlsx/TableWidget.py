import json
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QAbstractItemView, QHeaderView, QMenu, QMessageBox, QDialog, QFormLayout, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout

"""
继承QWidget
"""


class TableWidget(QWidget):
    table_widget = None

    def __init__(self):
        super().__init__()
        self.init_ui()

    def keyPressEvent(self, event) -> None:
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_S:
            print(self.customer_list)
            print('Ctrl+S was pressed')

    def save_data(self):
        collect_list = []
        for customer in self.customer_list:
            data = {
                'carNo': customer[0],
                'ratedLoadingMass': customer[1],
                'name': customer[2],
                'contact': customer[3]
            }
            collect_list.append(data)
        self.save_btn.setEnabled(False)
        with open("user_info.json", 'w', encoding='utf-8') as fw:
            json.dump(collect_list, fw, indent=4, ensure_ascii=False)

    def closeEvent(self, event):
        if self.save_btn.isEnabled():
            r = QMessageBox.warning(self, "警告", "你还有操作没保存，请保存后退出！", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.No:
                event.accept()
            else:
                event.ignore()

    def init_ui(self):

        if not os.path.exists('user_info.json'):
            QMessageBox.warning(self, "警告", "user_info文件不存在，请检查配置文件是否存在！！！", QMessageBox.Ok)
            sys.exit()

        with open("user_info.json", encoding='utf-8') as fw:
            items = json.load(fw)
            self.customer_list = [tuple(item.values()) for item in items]
        # 设置布局
        layout = QVBoxLayout()
        table_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()
        self.table_widget = QTableWidget(len(self.customer_list), 4)
        self.table_widget.setHorizontalHeaderLabels(['车号', '核定载质量', '驾驶员姓名', '联系方式'])
        # 最后一列自动拉伸
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        # 输入内容
        for (row, customer) in enumerate(self.customer_list):
            for column in range(len(customer)):
                self.table_widget.setItem(row, column,
                                          QTableWidgetItem(customer[column]))
        table_layout.addWidget(self.table_widget)
        # 单元格不能修改
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        # 选择单行
        self.table_widget.setSelectionBehavior(QAbstractItemView
                                               .SelectRows)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.generate_menu)

        self.save_btn = QPushButton("保存")
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet("QPushButton{\n"
                               "    background:orange;\n"
                               "    color:white;\n"
                               "    box-shadow: 1px 1px 3px;font-size:18px;border-radius: 24px;font-family: 微软雅黑;\n"
                               "}\n"
                               "QPushButton:pressed{\n"
                               "    background:black;\n"
                               "}")
        self.save_btn.setFixedSize(150, 50)
        self.save_btn.clicked.connect(self.save_data)

        btn_layout.addStretch(1)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(table_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        # 调整窗口大小
        self.resize(900, 500)
        # 窗口居中
        self.center()
        # 窗口标题
        self.setWindowTitle("数据管理器")
        # 显示窗口
        self.show()

    # 实现居中
    def center(self):
        f = self.frameGeometry()
        c = QDesktopWidget().availableGeometry().center()
        f.moveCenter(c)
        self.move(f.topLeft())

    def insert_row(self, row, car_no, rated_loading_mass, name, contact):
        car_no_item = QTableWidgetItem(car_no)
        rated_loading_mass_item = QTableWidgetItem(rated_loading_mass)
        name_item = QTableWidgetItem(name)
        contact_item = QTableWidgetItem(contact)
        self.table_widget.insertRow(row)
        self.table_widget.setItem(row, 0, car_no_item)
        self.table_widget.setItem(row, 1, rated_loading_mass_item)
        self.table_widget.setItem(row, 2, name_item)
        self.table_widget.setItem(row, 3, contact_item)

    def insert_slot(self):
        di = QInputDialog()
        ok = di.exec_()
        if ok:
            car_no = di.car_no_line.text()
            rated_loading_mass = di.rated_loading_mass_line.text() + 'kg'
            name = di.name_line.text()
            contact = di.contact_line.text()
            row_count = self.table_widget.rowCount()
            self.insert_row(row_count, car_no, rated_loading_mass, name, contact)
            self.customer_list.append((car_no, rated_loading_mass, name, contact))
            self.table_widget.verticalScrollBar().setValue(self.table_widget.verticalScrollBar().maximum())
            self.save_btn.setEnabled(True)

    def delete_slot(self):
        row_select = self.table_widget.selectedItems()
        if len(row_select) != 0:
            row = row_select[0].row()
            self.table_widget.removeRow(row)
            del self.customer_list[row]
            self.save_btn.setEnabled(True)

    def generate_menu(self):
        # 构造菜单
        menu = QMenu()
        # 添加菜单的选项
        item1 = menu.addAction('新增联系人')
        item3 = menu.addAction("删除联系人")
        item1.triggered.connect(self.insert_slot)
        item3.triggered.connect(self.delete_slot)
        menu.exec_(QCursor.pos())


class QInputDialog(QDialog):
    def __init__(self):
        super(QInputDialog, self).__init__()
        self.layout = QFormLayout()
        self.car_no = QLabel("车号")
        self.car_no_line = QLineEdit()
        self.rated_loading_mass = QLabel("核定载质量")
        self.rated_loading_mass_line = QLineEdit()
        self.rated_loading_mass_line.setValidator(QIntValidator())
        self.name = QLabel("驾驶员姓名")
        self.name_line = QLineEdit()
        self.contact = QLabel("联系方式")
        self.contact_line = QLineEdit()
        self.contact_line.setValidator(QIntValidator())
        self.qbtn = QPushButton("保存")
        self.init_ui()

    def init_ui(self):
        self.resize(300, 100)
        self.setWindowTitle("新增数据")
        # '车号', '核定载质量', '驾驶员姓名', '联系方式'
        self.layout.addRow(self.car_no, self.car_no_line)
        self.layout.addRow(self.rated_loading_mass, self.rated_loading_mass_line)
        self.layout.addRow(self.name, self.name_line)
        self.layout.addRow(self.contact, self.contact_line)
        self.layout.addRow(self.qbtn)
        self.qbtn.clicked.connect(self.check)
        self.setLayout(self.layout)

    def check(self):
        if not self.car_no_line.text():
            QMessageBox.warning(self, "警告", "车号为必填项!", QMessageBox.Ok)
            return
        if not self.rated_loading_mass_line.text():
            QMessageBox.warning(self, "警告", "核定载质量为必填项!", QMessageBox.Ok)
            return
        if not self.name_line.text():
            QMessageBox.warning(self, "警告", "驾驶员姓名为必填项!", QMessageBox.Ok)
            return
        if not self.contact_line.text():
            QMessageBox.warning(self, "警告", "联系方式为必填项!", QMessageBox.Ok)
            return
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TableWidget()
    sys.exit(app.exec_())
