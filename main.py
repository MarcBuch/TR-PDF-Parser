import re
import json
import os
import sys
from lib.warrant import Warrant
from lib.certificate import Certificate
from lib.stock import Stock
from pdfminer.high_level import extract_text
import shutil

def determineDocument(pdf):
    """ Scans the pdf document for certain text lines and determines the type of investment vehicle traded"""
    if 'turbop' in pdf or 'turboc' in pdf:
        return 'certificate'
    elif 'minil' in pdf:
        return 'certificate'
    elif 'call' in pdf or 'put' in pdf:
        return 'warrant'
    else:
        return 'stock'

def checkDocument(pdf):
    if 'trade' in pdf and 'republic' in pdf:
        return True
    else:
        return False

sourceFolder = '/downloads'
destinationFolder = '/Wertpapierabrechnungen/'

os.chdir(sourceFolder)
files = os.listdir()

for file in files:
    if 'pdf' in file:
        pdf = extract_text(file).lower().split()
        
        if checkDocument(pdf):
            pdfType = determineDocument(pdf)

        if pdfType is 'certificate':
            certificate = Certificate(pdf)

            print('\nCertificate')
            print(file)
            print(certificate.file)
            print(certificate.date + ' ' + certificate.time)
            print(certificate.orderType.upper())
            print(certificate.productType + ' ' + certificate.underlying.upper())
            print('ISIN: ' + certificate.isin.upper())      
            print('Shares: ' + str(certificate.shares))
            print('Market Price: ' + str(certificate.marketPrice))
            print('Net Total: ' + str(certificate.netTotal))
            print(' - Brokerage Fee: ' + str(certificate.brokerageFee))
            print(' - Taxes: ' + str(certificate.taxes))
            print('Total: ' + str(certificate.total))

            # os.rename() doesn't work with 2 different file systems
            shutil.copy(sourceFolder + file, destinationFolder + certificate.file)
            os.remove(sourceFolder + file)
            print('File moved')

        if pdfType is 'warrant':
            warrant = Warrant(pdf)

            print('\nWarrant')
            print(file)
            print(warrant.file)
            print(warrant.orderType.upper())
            print(warrant.date + ' ' + warrant.time)
            print(warrant.option.upper() + ' ' + warrant.underlying.upper() + ' @' + str(warrant.strikePrice) + ' ' + warrant.expiry)
            print('ISIN: ' + warrant.isin.upper())
            print('Shares: ' + str(warrant.shares))
            print('Market Price: ' + str(warrant.marketPrice))
            print('Net Total: ' + str(warrant.netTotal))
            print(' - Brokerage Fee: ' + str(warrant.brokerageFee))
            print(' - Taxes: ' + str(warrant.taxes))
            print('Total: ' + str(warrant.total))

            shutil.copy(sourceFolder + file, destinationFolder + warrant.file)
            os.remove(sourceFolder + file)
            print('File moved')

        if pdfType is 'stock':
            stock = Stock(pdf)

            print('\nStock')
            print(file)
            print(stock.file)
            print(stock.date + ' ' + stock.time)
            print(stock.orderType.upper())
            print(stock.underlying)
            print('ISIN: ' + stock.isin.upper())
            print('Shares: ' + str(stock.shares))
            print('Market Price: ' + str(stock.marketPrice))
            print('Net Total: ' + str(stock.netTotal))
            print(' - Brokerage Fee: ' + str(stock.brokerageFee))
            print(' - Taxes: ' + str(stock.taxes))
            print('Total: ' + str(stock.total))

            shutil.copy(sourceFolder + file, destinationFolder + stock.file.replace(' ', '_').replace('/', ''))
            os.remove(sourceFolder + file)
            print('File moved')