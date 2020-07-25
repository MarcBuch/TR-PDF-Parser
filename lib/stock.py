from lib.transaction import Transaction

class Stock(Transaction):
    def __init__(self, pdf):
        super().__init__(pdf)

        if 'fremdkostenzuschlag' in pdf:
            self.brokerageFee = 1
        else:
            self.brokerageFee = 0

        if 'kapitalertragssteuer' in pdf:
            taxes = 0
            if 'optimierung' in pdf:
                taxes = self.total - (self.netTotal - self.brokerageFee)
            else:
                taxes = self.total - (self.netTotal - self.brokerageFee)
                # Limit the float to only 2 decimals
            self.taxes = float("{:.2f}".format(taxes))
        else:
            self.taxes = 0

        self.underlying = ''
        temp = ' '.join(pdf[pdf.index('position') + 1 : pdf.index('isin:')]).upper()
        if 'KURS' in temp:
            self.underlying = ' '.join(pdf[pdf.index('kurs') + 1 : pdf.index('isin:')]).upper()

        if 'WISDOMTREE' in temp:
            if 'OIL' in temp:
                if 'SHT' in temp:
                    self.underlying = 'SHORT_WTI_CRUDE_OIL'
                else:
                    self.underlying = 'WTI_CRUDE_OIL'
            if 'NATURAL GAS' in temp:
                if 'SHT' in temp:
                    self.underlying = 'SHORT_WTI_NATURAL_GAS'
                else:
                    self.underlying = 'WTI_NATURAL_GAS'
        else:
            self.underlying = ' '.join(pdf[pdf.index('position') + 1 : pdf.index('isin:')]).upper()


        self.file = self.orderType.upper() + '_' + self.type.capitalize() + '_' + self.underlying.upper() + '_' + self.date.replace('.', '') + '.pdf'