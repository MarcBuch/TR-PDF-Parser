from ast import Try
from dataclasses import replace
import re

validMarketOrderTypes = ['market-order', 'limit-order']
validOrderTypes = ['kauf', 'verkauf', 'sparplanausführung', 'dividende', 'ausschüttung']

class Transaction:
    def __init__(self, pdf):

        if 'turbop' in pdf or 'turboc' in pdf:
            self.type = 'certificate'
        elif 'minil' in pdf:
            self.type = 'certificate'
        elif 'call' in pdf or 'put' in pdf:
            self.type = 'warrant'
        elif 'ausschüttung' in pdf or 'dividende' in pdf:
            self.type = 'dividend'
        else:
            self.type = 'stock'

        # Check for marketOrderType
        for typ in validMarketOrderTypes:
            if typ in pdf:
                self.marketOrderType = pdf[pdf.index(typ)]

        # Check for date and time
        try:
            self.date = re.findall(r"\d\d.\d\d.\d\d\d\d", pdf[pdf.index('am') + 1])[0]
            self.time = re.findall(r"\d\d:\d\d", pdf[pdf.index('um') + 1])[0]
        except ValueError:
            self.date = re.findall(r"\d\d.\d\d.\d\d\d\d", pdf[pdf.index('ex-tag') + 1])[0]
        except IndexError:
            self.time = ""


        # Check for orderType
        for typ in validOrderTypes:
            if typ in pdf:  
                if typ == 'verkauf':
                    self.orderType = 'sell'
                elif typ == 'kauf' or typ == 'sparplanausführung':
                    self.orderType = 'buy' 
                else:
                    self.orderType = 'dividend'

        # ISIN
        self.isin = pdf[pdf.index('isin:') + 1]

        # Shares
        if ',' in pdf[pdf.index('stk.') - 1]:
            self.shares = float((pdf[pdf.index('stk.') - 1]).replace(',','.'))
        else:
            self.shares = int(pdf[pdf.index('stk.') - 1])

        # Market Price
        if pdf[pdf.index('stk.') + 1] != 'kurs':
            try:            
                self.marketPrice = float(pdf[pdf.index('stk.') + 1].replace('.', '').replace(',', '.'))
            except ValueError:
                self.marketPrice = ""
        else:
            try:
                self.marketPrice = float(pdf[pdf.index('kurs') + 1].replace('.', '').replace(',', '.'))
            except ValueError: # sometimes order in array is different
                self.marketPrice = float(pdf[pdf.index('kurs') + 2].replace('.', '').replace(',', '.'))
                    

        # Find totals for tax calculation
        res = []
        for pos in range(len(pdf)):
            hit = re.findall(r'gesamt', pdf[pos])
            if hit != []:
                res.append(pos)
        self.grossTotal = float(pdf[res[0]+1].replace('.', '').replace(',', '.')) # Aus "Gesamt Übersicht" (ggf. in Fremdwährung)
        try:
            self.total = abs(float(pdf[pdf.index('valuta')+3].replace('.', '').replace(',', '.'))) # Aus "Abrechnung" (in EUR)
        except ValueError:
            self.total = abs(float(pdf[pdf.index('wertstellung')+3].replace('.', '').replace(',', '.'))) # Aus "Abrechnung" (in EUR)

        

        # Currency
        self.currency = pdf[pdf.index('betrag')+2] # Währung Übersicht

        # Asset name
        self.securityName = " ".join(pdf[pdf.index('position')+1:pdf.index('isin:')]).replace('anzahl','').replace('durchschnittskurs','').replace('kurs','').replace('betrag','').replace('erträgnis','').replace('preis','').strip()