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
                taxes = self.total - (self.grossTotal - self.brokerageFee)
            else:
                taxes = self.total - (self.grossTotal - self.brokerageFee)
                # Limit the float to only 2 decimals
            self.taxes = float("{:.2f}".format(taxes))
        else:
            self.taxes = 0

        self.file = self.orderType.upper() + '_' + self.type.capitalize() + '_' + self.date.replace('.', '') + '.pdf'