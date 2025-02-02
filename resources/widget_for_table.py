from PyQt5.QtWidgets import QWidget #, QApplication, QDoubleSpinBox
from PyQt5.uic import loadUi

from .dict import table1_en, table2_en

class Table1Widget(QWidget):
    def __init__(self, lang="es"):
        super().__init__()
        loadUi("resources/views/ui/table_1.ui", self)
        self.lang = lang
        if self.lang != "es":
            self.update_language()
        self.setWindowTitle('TABLA 1')

    def update_language(self):
        self.label_table.setText(table1_en[self.label_table.text()])
        self.label_table_description.setText(table1_en[self.label_table_description.text()])
        self.label_table_source.setText(self.label_table_source.text().replace("Tabla", "Table"))
        for row in range(self.table1_widget.rowCount()):
            for col in range(self.table1_widget.columnCount()):
                es_text = self.table1_widget.item(row, col).text()
                if "," not in es_text:
                    en_tans = table1_en[es_text]
                    self.table1_widget.item(row, col).setText(en_tans)

class Table2Widget(QWidget):
    def __init__(self, lang="es"):
        super().__init__()
        loadUi("resources/views/ui/table_2.ui", self)
        self.lang = lang
        self.table2_widget_0.setColumnWidth(0, 280)
        self.table2_widget_0.setRowHeight(0, 70)
        
        self.table2_widget_1.setSpan(0, 1, 1, 4)
        self.table2_widget_1.setSpan(0, 0, 2, 1)

        self.table2_widget_2.setRowHeight(0, 55)
        self.rows_to_change_span = {1: 2, 3: 3, 6: 2, 8: 2, 10: 1, 11: 1, 12: 1, 13: 3, 16: 1}
        for row, span in self.rows_to_change_span.items():
            if span != 1:
                self.table2_widget_2.setSpan(row, 0, span, 1)

        if self.lang != "es":
            self.update_language()

        self.setWindowTitle('TABLA 2')

    def update_language(self):
        self.label_table.setText(table2_en[self.label_table.text()])

        self.label_table_description_0.setText(table2_en[self.label_table_description_0.text()])
        self.label_table_description_1.setText(table2_en[self.label_table_description_1.text()])
        self.label_table_description_2.setText(table2_en[self.label_table_description_2.text()])

        self.label_table_source_0.setText(self.label_table_source_0.text().replace("Tabla", "Table"))
        self.label_table_source_1.setText(self.label_table_source_1.text().replace("Tabla", "Table"))
        self.label_table_source_2.setText(self.label_table_source_2.text().replace("Tabla", "Table"))

        # change items of the widget
        for col in range(3):
            es_text = self.table2_widget_0.item(0, col).text()
            en_tans = table2_en[es_text]
            self.table2_widget_0.item(0, col).setText(en_tans)

        for col in range(2):
            es_text = self.table2_widget_1.item(0, col).text()
            en_tans = table2_en[es_text]
            self.table2_widget_1.item(0, col).setText(en_tans)    
        
        for col in range(3):
            es_text = self.table2_widget_2.item(0, col).text()
            en_tans = table2_en[es_text]
            self.table2_widget_2.item(0, col).setText(en_tans)
        
        for row in self.rows_to_change_span.keys():
            es_text = self.table2_widget_2.item(row, 0).text()
            en_tans = table2_en[es_text]
            self.table2_widget_2.item(row, 0).setText(en_tans)