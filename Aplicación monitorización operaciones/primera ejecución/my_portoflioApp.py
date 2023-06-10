from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer
"""
We are going to download the necessary variables to import posititions to investing.com, which are:
    ·ISIN/Ticker
    ·Open Price
    ·Amount
"""

class PortfolioApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

        # You can access the variables by calling the instance variables of the PortfolioApp object. 
        # For example, app.symbol will give you the symbol of the contract
        self.symbol = []
        self.sectype = []
        self.exchange = []
        self.currency = []
        self.positionn = []
        self.marketPrice = []
        self.marketValue = []
        self.averageCost = []
        self.unrealizedPNL = []
        self.realizedPNL = []
        self.accountName = []

    def error(self, reqId, errorCode, errorString, errorObj):
        print("Error: ", reqId, " ", errorCode, " ", errorString)


    def nextValidId(self, orderId):
        self.start()

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        #print("·UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange,
        #      "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:", averageCost,
        #     "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)

        self.symbol.append(contract.symbol)
        self.sectype.append(contract.secType)
        self.exchange.append(contract.exchange)
        self.currency.append(contract.currency)
        self.positionn.append(position)
        self.marketPrice.append(marketPrice)
        self.marketValue.append(marketValue)
        self.averageCost.append(averageCost)
        self.unrealizedPNL.append(unrealizedPNL)
        self.realizedPNL.append(realizedPNL)
        self.accountName.append(accountName)

    def updateAccountTime(self, timeStamp: str):
        print("UpdateAccountTime. Time:", timeStamp)
        

    def start(self):
        # Account number can be omitted when using reqAccountUpdates with single account structure
        self.reqAccountUpdates(True, "")
        #reqAccountUpdates --> position and account information for a specific account

    def stop(self):
        self.reqAccountUpdates(False, "")
        self.done = True
        self.disconnect()

""" #To run the app
def main():
    app = PortfolioApp()
    app.connect("127.0.0.1", 7497, 0)

    Timer(5, app.stop).start()
    app.run()

if __name__ == "__main__":
    main()
"""
"""
#To run the app
app = PortfolioApp()
app.connect("127.0.0.1", 7497, 0)

Timer(5, app.stop).start()
app.run()


#Print the returned variables
print(app.symbol)
print(app.sectype)
print(app.exchange)
print(app.currency)
print(app.positionn)
print(app.marketPrice)
print(app.marketValue)
print(app.averageCost)
print(app.unrealizedPNL)
print(app.realizedPNL)
print(app.accountName)
"""
