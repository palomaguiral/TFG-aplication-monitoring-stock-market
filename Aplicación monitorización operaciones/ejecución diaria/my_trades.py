"""
Queremos descargar las operaciones de COMPRA y las operaciones de VENTA que se han 
hecho desde nuestra cuenta de IBKR.
Se descargaran las operaciones hechas en los últimos 7 días (o los elegidos). Esto se puede cambiar en los ajustes de TWS, pudiendo elegir
entre recuperar las operaciones desde hoy hasta los últimos 7 días, no más.
"""
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer
from ibapi.execution import ExecutionFilter
from datetime import datetime, timedelta

########################################################BUY and SELL operations#############################################################

class MyTrades_BuySell_App(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.conID = []
        self.symbol = []
        self.sectype = []
        self.exchange = []
        self.currency =[]
        self.action = []
        self.quantity = []
        self.executionPrice = []
        self.executionTime = []

    def error(self, reqId, errorCode, errorString, errorObj):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.start()

    def execDetails(self, reqId, contract, execution):
        if execution.side == 'BOT' or execution.side == 'SLD': #BOT: símbolo de compra //// SLD: símbolo de venta
            self.conID.append(contract.conId)
            self.symbol.append(contract.symbol)
            self.sectype.append(contract.secType)
            self.exchange.append(contract.exchange)
            self.currency.append(contract.currency)
            self.action.append(execution.side)
            self.quantity.append(execution.shares)
            self.executionPrice.append(execution.price)
            self.executionTime.append(execution.time)
            

    def start(self):
        self.reqExecutions(1, ExecutionFilter())

    def stop(self):
        self.done = True
        self.disconnect()


######################################To run the app#########################################
app = MyTrades_BuySell_App()
app.connect("127.0.0.1", 7497, 0)

Timer(5, app.stop).start()
app.run()


print('----BUY and SELL operations----')
print(app.symbol)
print(app.action)
print(app.quantity)
print(app.executionPrice)
print(app.executionTime)
