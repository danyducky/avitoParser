""" Database using mySql for dispatching data from Avito"""
from openpyxl import load_workbook, Workbook

class excelBuilder:
    def __init__(self):
        """ Creating excel file """
        self.fileName = 'data.xlsx'
        self.book = load_workbook(self.fileName)
        self.sheet = self.book.active


    def addRow(self, *data):
        """ Add table row to current working file """
        self.sheet.append(data)


    def save(self):
        """ Save working file """
        self.book.save(self.fileName)