import re
import json
import os
import sys

from numpy import true_divide
from lib.warrant import Warrant
from lib.certificate import Certificate
from lib.stock import Stock
from lib.dividend import Dividend
import pdfminer
from pdfminer.high_level import extract_text
import shutil
import pandas as pd

def determineDocument(pdf):
    """ Scans the pdf document for certain text lines and determines the type of investment vehicle traded"""
    if 'turbop' in pdf or 'turboc' in pdf:
        return 'certificate'
    elif 'minil' in pdf:
        return 'certificate'
    elif 'call' in pdf or 'put' in pdf:
        return 'warrant'
    elif 'dividende' in pdf:
        return 'dividend'
    elif 'ausschüttung' in pdf:
        return 'dividend'
    elif 'wertpapierabrechnung' in pdf:
        return 'stock'
    else:
        return 'stock'

def checkDocument(pdf):
    if 'trade' in pdf and 'republic' in pdf:
        return True 
    else:
        return False

sourceFolder = '/Downloads/'
destinationFolder = '/Wertpapierabrechnungen/'
os.makedirs(destinationFolder + "originals", exist_ok=True)

# entsprechend Portfolio Performance
header = ['date', 'type', 'note', 'ticker symbol', 'security name', 'shares', 'price', 'fees', 'taxes', 'value', 'ISIN', 'expiration date', 'strike price', 'warrant type', 'warrant underlying']
df = pd.DataFrame(columns=header)

os.chdir(sourceFolder)
files = os.listdir()


for file in files:
    dfTemp = pd.DataFrame()
    if 'pdf' in file:
        pdf = extract_text(file).lower().split()
        print("\nStarted parsing file")
        
        if checkDocument(pdf):
            pdfType = determineDocument(pdf)

        if pdfType == 'certificate':
            certificate = Certificate(pdf)

            print(pdfType.capitalize())
            print(file)
            print(certificate.file)
            print(certificate.date + ' ' + certificate.time)
            print(certificate.orderType.upper())
            print(certificate.productType + ' ' + certificate.underlying.upper())
            print('ISIN: ' + certificate.isin.upper())
            print('Asset: '+ certificate.securityName.capitalize())    
            print('Shares: ' + str(certificate.shares))
            print('Market Price: ' + str(certificate.marketPrice))
            print('Gross total: ' + str(certificate.grossTotal))
            print(' - Brokerage Fee: ' + str(certificate.brokerageFee))
            print(' - Taxes: ' + str(certificate.taxes))
            print('Total: ' + str(certificate.total))

            dfTemp = pd.DataFrame({'date': [certificate.date], 'type': [certificate.orderType], 'shares': [certificate.shares], 'price': [certificate.marketPrice], 'fees': [certificate.brokerageFee], 'taxes': [certificate.taxes], 'value': [certificate.total], 'ISIN': [certificate.isin], 'security name': [certificate.securityName.capitalize()]})
            df = pd.concat([df, dfTemp])

            print('File parsed')

            shutil.copy(sourceFolder + file, destinationFolder + certificate.file)
            shutil.move(sourceFolder + file, destinationFolder + "originals/" + file)
            print('File moved')

        if pdfType == 'warrant':
            warrant = Warrant(pdf)
            print('\n' + pdfType.capitalize())
            print(file)
            print(warrant.file)
            print(warrant.orderType.upper())
            print(warrant.date + ' ' + warrant.time)
            print(warrant.option.upper() + ' ' + warrant.underlying.upper() + ' @' + str(warrant.strikePrice) + ' ' + warrant.expiry)
            print('ISIN: ' + warrant.isin.upper())
            print('Asset: '+ warrant.securityName.capitalize())
            print('Shares: ' + str(warrant.shares))
            print('Market Price: ' + str(warrant.marketPrice))
            print('Gross total: ' + str(warrant.grossTotal))
            print(' - Brokerage Fee: ' + str(warrant.brokerageFee))
            print(' - Taxes: ' + str(warrant.taxes))
            print('Total: ' + str(warrant.total))

            dfTemp = pd.DataFrame({'date': [warrant.date], 'type': [warrant.orderType], 'shares': [warrant.shares], 'price': [warrant.marketPrice], 'fees': [warrant.brokerageFee], 'taxes': [warrant.taxes], 'value': [warrant.total], 'ISIN': [warrant.isin], 'security name': [warrant.securityName.capitalize()]})
            df = pd.concat([df, dfTemp])

            print('File parsed')

            shutil.copy(sourceFolder + file, destinationFolder + warrant.file)
            shutil.move(sourceFolder + file, destinationFolder + "originals/" + file)
            print('File moved')

        if pdfType == 'stock':
            stock = Stock(pdf)

            print('\n' + pdfType.capitalize())
            print(file)
            print(stock.file)
            print(stock.date + ' ' + stock.time)
            print(stock.orderType.upper())
            print('ISIN: ' + stock.isin.upper())
            print('Asset: '+ stock.securityName.capitalize())
            print('Shares: ' + str(stock.shares))
            print('Market Price: ' + str(stock.marketPrice))
            print('Gross total: ' + str(stock.grossTotal))
            print(' - Brokerage Fee: ' + str(stock.brokerageFee))
            print(' - Taxes: ' + str(stock.taxes))
            print('Total: ' + str(stock.total))

            dfTemp = pd.DataFrame({'date': [stock.date], 'type': [stock.orderType], 'shares': [stock.shares], 'price': [stock.marketPrice], 'fees': [stock.brokerageFee], 'taxes': [stock.taxes], 'value': [stock.total], 'ISIN': [stock.isin], 'security name': [stock.securityName.capitalize()]})
            df = pd.concat([df, dfTemp])

            print('File parsed')

            shutil.copy(sourceFolder + file, destinationFolder + stock.file)
            shutil.move(sourceFolder + file, destinationFolder + "originals/" + file)
            print('File moved')

        if pdfType == 'dividend':
            dividend = Dividend(pdf)

            print('\n' + pdfType.capitalize())
            print(file)
            print(dividend.file)
            print(dividend.date)
            print(dividend.orderType.upper())
            print('ISIN: ' + dividend.isin.upper())
            print('Asset: '+ dividend.securityName.capitalize())
            print('Shares: ' + str(dividend.shares))
            print('Gross total: ' + str(dividend.grossTotal))
            print(' - Brokerage Fee: ' + str(dividend.brokerageFee))
            print(' - Taxes: ' + str(dividend.taxes))
            print('Total: ' + str(dividend.total))

            dfTemp = pd.DataFrame({'date': [dividend.date], 'type': [dividend.orderType], 'shares': [dividend.shares], 'fees': [dividend.brokerageFee], 'taxes': [dividend.taxes], 'value': [dividend.total], 'ISIN': [dividend.isin], 'security name': [dividend.securityName.capitalize()]})
            df = pd.concat([df, dfTemp])

            print('File parsed')

            shutil.copy(sourceFolder + file, destinationFolder + dividend.file)
            shutil.move(sourceFolder + file, destinationFolder + "originals/" + file)
            print('File moved')

df.set_index('date')
df.to_csv(sourceFolder + 'parsedTrades.csv', ',')
print('\nProcessing completed\n')