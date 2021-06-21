import os, sys, xlrd, xlwt
from xlutils.copy import copy

import csv


CurrentPath = os.getcwd()

def SearchMITRE(text, version):
    csvPATH = CurrentPath + '\DB\mitre.csv'

    Results = []

    # read csv, and split on "," the line
    csv_file = csv.reader(open(csvPATH, "rb"), delimiter=",")

    # loop through csv list
    print(csv_file)

    for row in csv_file:

        # if current rows 2nd value is equal to input, print that row
        if (text.lower() in row.lower()) and (version.lower() in row.lower()):
            Results.append(str(row[0])+ " (" + str(row) + ")")

    return Results



def SearchNVD(text, version):
    csvPATH = CurrentPath + '/DB/nvd.csv'

    Results = []

    # read csv, and split on "," the line
    csv_file = csv.reader(open(csvPATH, "rt"), delimiter=",")

    # loop through csv list
    for row in csv_file:
        # if current rows 2nd value is equal to input, print that row
        #ExcelRow = str(row[1] + row[2] + row[3]).lower()
        if (text.lower() in str(row)) and (version.lower() in str(row)):
            Results.append(str(row[0])+ " (" + str(row) + ")")
    print(Results)
    return Results


def ProcessExcelDB(FileName):
    ExcelFile = xlrd.open_workbook(FileName)


    Sheets = [sheet.name for sheet in ExcelFile.sheets()]
    SheetData = Sheets.index('Processed')
    Sheet = ExcelFile.sheet_by_index(SheetData)

    # Extracting number of rows
    Rows = Sheet.nrows
    print("Rows: " + str(Rows))
    # Extracting number of columns
    Columns = Sheet.ncols
    print("Columns: " + str(Columns))

    f = open(FileName.replace('.xlsx', '.txt'), "a")
    for i in range(1, Rows):
        Product = str(Sheet.cell_value(i, 0))
        Version = str(Sheet.cell_value(i, 2))
        if len(Version)>0:
            #MITRE = " ".join(SearchMITRE(Product, Version))

            NIST = " ".join(SearchNVD(Product,Version))
            # print('[*] Mitre: ' + FileName.split('\\')[-1], Product, Version, len(MITRE), MITRE)
            print('[*] Nist NVD: ' + FileName.split('\\')[-1], Product, Version, len(NIST), NIST)

            #f.write(Product + "\n" + Version + "\n" + MITRE + "\n" + NIST + '\r\n\r\n\r\n')
            if len(NIST) > 0:
                f.write(Product + "\n" + Version + "\n" + NIST + '\r\n\r\n\r\n')
    f.close()


files = []

for r, d, f in os.walk(CurrentPath + '/Files/'):
    for file in f:
        if ('.xlsx' in file.lower()) or '.xls' in file.lower():
            files.append(os.path.join(r, file))

for file in files:
    if ('B2B_CPE_FW status T-HT_CPE_26.04.2021.xlsx' in file) and '~' not in file:
        print(file)
        ProcessExcelDB(file)
