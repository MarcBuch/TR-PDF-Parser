from lib.transaction import Transaction

validOptions = ['call', 'put']

class Warrant(Transaction):
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

        # Check for valid option
        for typ in validOptions:
            if typ in pdf:
                self.option = pdf[pdf.index(typ)]
        # Option Expiry Date
        self.expiry = pdf[pdf.index(self.option) + 1]

        # Option Underlying Security
        self.underlying = pdf[pdf.index(self.expiry) + 1]

        # Option Strike Price
        self.strikePrice = int(pdf[pdf.index(self.underlying) + 1])

        self.file = self.orderType.upper() + '_' + self.type.capitalize() + '_' + self.option.capitalize() + '_' + self.underlying.upper() + '_' + self.expiry.replace('.', '') + '_@' + str(self.strikePrice) + '_' + self.date.replace('.', '') + '.pdf'