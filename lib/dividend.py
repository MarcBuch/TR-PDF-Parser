from typing import Type
from numpy import empty
from lib.transaction import Transaction
import re

class Dividend(Transaction):
    def __init__(self, pdf):
        super().__init__(pdf)

        if 'fremdkostenzuschlag' in pdf:
            self.brokerageFee = 1
        else:
            self.brokerageFee = 0

        # Parse totals (they are in a different order for Dividents)
        res = []
        for pos in range(len(pdf)):
            hit = re.findall(r'betrag', pdf[pos])
            if hit != []:
                res.append(pos)
        self.grossTotal = float(pdf[res[0]+1].replace('.', '').replace(',', '.')) # Aus "Gesamt Übersicht" (ggf. in Fremdwährung)
        if len(res) > 2:
            self.total = float(pdf[res[2]+1].replace('.', '').replace(',', '.')) # Aus "Abrechnung" (in EUR)
        else:
            self.total = float(pdf[res[1]+1].replace('.', '').replace(',', '.')) # Aus "Abrechnung" (in EUR)

        # Determine conversion rate
        try:
            self.convPairs = re.findall(r'\beur/[a-z]{3}\b', " ".join(pdf)) [0]
        except:
            self.convPairs = ""
        
        try:
            self.convRate = float(pdf[pdf.index(self.convPairs)-1].replace(',','.'))
        except:
            self.convRate = []

        # Calculate taxes
        if self.convRate != []:
            self.grossTotal = self.grossTotal / self.convRate
            self.taxes = self.grossTotal - self.total
            # Limit the float to only 2 decimals
            self.taxes = float("{:.2f}".format(self.taxes))
        else:
            self.taxes = float("{:.2f}".format(self.grossTotal - self.total))

        self.file = self.type.capitalize() + '_' + self.date.replace('.', '') + '.pdf'