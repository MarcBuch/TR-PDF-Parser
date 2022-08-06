from lib.transaction import Transaction

class Certificate(Transaction):
    def __init__(self, pdf):
        super().__init__(pdf)

        if 'fremdkostenzuschlag' in pdf:
            self.brokerageFee = 1
        else:
            self.brokerageFee = 0

        if 'kapitalertragssteuer' in pdf:
            taxes = 0
            if 'optimierung' in pdf:
                taxes = self.total - (self.grossTotal - self.brokerageFee)
            else:
                taxes = self.total - (self.grossTotal - self.brokerageFee)
                # Limit the float to only 2 decimals
            self.taxes = float("{:.2f}".format(taxes))
        else:
            self.taxes = 0

        self.underlying = ''

        if 'turbop' in pdf:
            self.underlying = pdf[pdf.index('turbop') + 2]
            self.productType = 'OpenEndTurbo'

        elif 'turboc' in pdf:
            self.underlying = pdf[pdf.index('turboc') + 2]
            self.productType = 'OpenEndTurbo'
        elif 'minil' in pdf:
            self.underlying = pdf[pdf.index('minil') + 2]
            self.productType = 'MiniFuture'

        self.file = self.orderType.upper() + '_' + self.type.capitalize() + '_' + self.productType + '_' + self.underlying.upper() + '_' + self.date.replace('.', '') + '.pdf'