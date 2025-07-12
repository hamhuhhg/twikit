import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)

class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('التحليلات والمشاهدات')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['النسخة', 'الموضوع', 'عدد المشاهدات'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        # In a real application, you would fetch data from the database
        data = [
            {'version': 'النسخة الرئيسية', 'topic': 'عام', 'views': 1500},
            {'version': 'نسخة العاملين', 'topic': 'تقنية', 'views': 2500},
            {'version': 'النسخة الرئيسية', 'topic': 'رياضة', 'views': 1000}
        ]
        self.table.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            self.table.setItem(row_num, 0, QTableWidgetItem(row_data['version']))
            self.table.setItem(row_num, 1, QTableWidgetItem(row_data['topic']))
            self.table.setItem(row_num, 2, QTableWidgetItem(str(row_data['views'])))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnalyticsWindow()
    window.show()
    sys.exit(app.exec_())
