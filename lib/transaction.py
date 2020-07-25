import re

validMarketOrderTypes = ['market-order', 'limit-order']
validOrderTypes = ['kauf', 'verkauf']

class Transaction:
    def __init__(self, pdf):

        if 'turbop' in pdf or 'turboc' in pdf:
            self.type = 'certificate'
        elif 'minil' in pdf:
            self.type = 'certificate'
        elif 'call' in pdf or 'put' in pdf:
            self.type = 'warrant'
        else:
            self.type = 'stock'

        # Check for marketOrderType
        for typ in validMarketOrderTypes:
            if typ in pdf:
                self.marketOrderType = pdf[pdf.index(typ)]

        # Check for date and time
        self.date = re.findall(r"\d\d.\d\d.\d\d\d\d", pdf[pdf.index('am') + 1])[0]
        self.time = re.findall(r"\d\d:\d\d", pdf[pdf.index('um') + 1])[0]

        # Check for orderType
        for typ in validOrderTypes:
            if typ in pdf:
                if typ is 'kauf':
                    self.orderType = 'buy'
                else:
                    self.orderType = 'sell'

        # ISIN
        self.isin = pdf[pdf.index('isin:') + 1]

        # Shares
        if '.' in pdf[pdf.index('stk.') - 1]:
            self.shares = int(float(pdf[pdf.index('stk.') - 1]))
        else:
            self.shares = int(pdf[pdf.index('stk.') - 1])

        # Market Price
        if pdf[pdf.index('stk.') + 1] != 'kurs':
            self.marketPrice = float(pdf[pdf.index('stk.') + 1].replace(',', '.'))
        else:
            self.marketPrice = float(pdf[pdf.index('kurs') + 1].replace(',', '.'))

        numbers = []
        for item in pdf:
            if re.match(r'\d*,', item):
                numbers.append(float(item.replace(',', '.')))
            if re.match(r'-\d*', item):
                numbers.append(float(item.replace(',', '.').replace('-', '')))

        numbers = list(dict.fromkeys(numbers))
        numbers = sorted(numbers)

        if 'optimierung' in pdf:
            self.netTotal = numbers[-2]
            self.total = numbers[-1]
        else:    
            self.netTotal = numbers[-1]
            self.total = numbers[-2]

        # Currency
        self.currency = pdf[pdf.index('eur')]