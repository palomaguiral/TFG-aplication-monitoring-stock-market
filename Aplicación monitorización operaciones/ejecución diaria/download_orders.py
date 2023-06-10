from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer
from ibapi.execution import ExecutionFilter
from datetime import datetime, timedelta
import time

from my_trades import MyTrades_BuySell_App
from getISIN import ISINApp

######################################  To get the operations - MyTrades_BuySell_App #########################################
app = MyTrades_BuySell_App()
app.connect("127.0.0.1", 7497, 0)

Timer(5, app.stop).start()
app.run()


print('----Operations----')
print(app.conID)
print(app.symbol)
print(app.action)
print(app.quantity)
print(app.executionPrice)
print(app.executionTime)



######################################  To get ISIN  - ISINapp ######################################
isins = []
names = []

contracts_IDs = app.conID
#print('numero de operaciones')
#print(len(app_sell.conID))
for i in range(len(app.conID)): #recorrer cada operación
    appISIN = ISINApp()

    appISIN.connect("127.0.0.1", 7497, 1000)

    mycontract = Contract()
    mycontract.conId = contracts_IDs[i]   # Use just the Contract ID

    time.sleep(1)

    appISIN.reqContractDetails(1, mycontract)

    appISIN.run()

    isins.append(appISIN.isin)
    names.append(appISIN.longname)

print(isins)
print(names)


######################################### SAVE in csv ###############################################
import pandas as pd
data = {'action':app.action, 'name':names, 'ISIN': isins, 'symbol' : app.symbol, 'quantity':app.quantity, 'execPrice':app.executionPrice,
        'execTime':app.executionTime}
df = pd.DataFrame(data)

df.to_csv('operationsHistory_IBKR.csv', index=False)