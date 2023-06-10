"""
To update the Investing's watchlist we need to use the ISIN, in order to not to have any confussion with the symbols
"""
from ibapi.client import *
from ibapi.wrapper import *
import time

class ISINApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.isin = ""
        self.longname = ""

    def contractDetails(self, reqId, contractDetails):
        #print(f"contract details: {contractDetails}")
        #print(contractDetails.secIdList)
        for identifier in contractDetails.secIdList:
            if identifier.tag == 'ISIN':
                isin = identifier.value
                break
        #print(f"ISIN for {contractDetails.contract.symbol}: {isin}")
        self.isin = isin

        self.longname = contractDetails.longName

    def contractDetailsEnd(self, reqId):
        #print("End of contractDetails")
        self.disconnect()
"""
def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 1000)

    mycontract = Contract()
    mycontract.symbol = "AI1"
    mycontract.secType = "STK"
    mycontract.exchange = "SMART"
    mycontract.currency = "EUR"


    # Or you can use just the Contract ID
    # mycontract.conId = 552142063


    time.sleep(3)

    app.reqContractDetails(1, mycontract)

    app.run()

if __name__ == "__main__":
    main()
"""

"""
symbols = ['AAPL', 'AI1', 'NFLX']
secs = ['STK', 'STK', 'STK']
exs = ["SMART", "SMART", "SMART"]
currencies = ['USD', 'EUR', 'USD']
for i in range(3):
    app = ISINApp()

    app.connect("127.0.0.1", 7497, 1000)

    mycontract = Contract()

    mycontract.symbol = symbols[i]
    mycontract.secType = secs[i]
    mycontract.exchange = exs[i]
    mycontract.currency = currencies[i]

        # Or you can use just the Contract ID
        # mycontract.conId = 552142063


    time.sleep(3)

    app.reqContractDetails(1, mycontract)

    app.run()
"""