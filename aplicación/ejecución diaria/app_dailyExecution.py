###################################################################################################################################
###################################################################################################################################
##                                      PASO 1 - Descargar histórico de operaciones (diarias) de IBKR                            ##
###################################################################################################################################
###################################################################################################################################
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

#df.to_csv('operationsHistory_IBKR.csv', index=False) #Guardar el historial en un csv  #LO HE QUITADO PARA LAS PRUEBAS









###################################################################################################################################
###################################################################################################################################
##                                      PASO 2.a - Cargar las operaciones de IBKR a la Cartera 1                                 ##
###################################################################################################################################
###################################################################################################################################
print('--------------------------------CARTERA 1-------------------------------------')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from datetime import datetime
import pdfkit
import os
import pandas as pd

from get_Portfolio_Names import portfolios_Names_and_ID

from pruebas_AddPosition_ConDetail import add_position
from pruebas_ClosePosition_ConDetails import close_position

from existing_positions_Cartera import get_existing_positions

from details_positions import detail_rows

from dotenv import load_dotenv
import os


#Cargar las credenciales de investing.com, que están como variables de entorno
load_dotenv()
user_investing = os.getenv('USER_INVESTING')
print(user_investing)
password_investing =  os.getenv('PASSWORD_INVESTING')



#https://stackoverflow.com/questions/72773206/selenium-python-attributeerror-webdriver-object-has-no-attribute-find-el


# Configuración del controlador de Chrome. # Start a web driver to automate the browser actions
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service("selenium/chromedriver/win32/111.0.5563.64/chromedriver.exe"), options=options)


                            ################### Inicia sesión ###################
driver.get("https://www.investing.com/portfolio") #"https://www.investing.com/portfolio/?portfolioID=ZWQzYDRnMmtiNz02ZTc4Mg%3D%3D"
driver.delete_all_cookies()# Elimina todas las cookies
email_input = driver.find_element("name", "loginFormUser_email")
email_input.send_keys(user_investing)
email_input.send_keys(Keys.RETURN)
password_input = driver.find_element("id", "loginForm_password")
password_input.send_keys(password_investing)
password_input.send_keys(Keys.RETURN)

                                ###########################'My watchlist'###############################
driver.get("https://www.investing.com/portfolio") #Go to 'import watchlist' page. STEP 1

wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk")))

# The cookie company, OneTrust, puts an overlay that protects the button and I can't click it. 
# To fix the error I have to delete from the html of the page the code: '<div id="onetrust-consent-sdk"></div>. 
element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script


                                            ##########Go to 'CARTERA 1 - ACTUAL'##########

#Primero hay que sacar el ID de la Cartera1 para poder acceder
existing_portfolios = portfolios_Names_and_ID(driver=driver) #nombre y ID de los portfolios de tu cuenta de investing.com
                                                             # ejemplo: [('Cartera 1 - ACTUAL', 'tab_41609486'), ('Cartera 2 - VENDIDAS', 'tab_41639367')]
for tuple in existing_portfolios:
    name = tuple[0]
    id = tuple[1]
    if name == 'Cartera 1':
        id_cartera1 = id #example: tab_41609486
#print(id_cartera1)

# Quitar cookies
wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk"))) 
element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script


#Acceder al portfolio de la Cartera1 --> CLICAR
cartera_btn = driver.find_element(By.XPATH, f"//ul[@class='ui-sortable portfolioTabs shortList']/li[@id='{id_cartera1}']") #example: id="tab_41609486"
cartera_btn.click()


time.sleep(5)
                    ###############################################Add operations #######################################################                                     

            ######### Leer el csv de las operaciones realizadas en IBKR en los últimos 7 días #########
df_operations= pd.read_csv('operationsHistory_IBKR.csv')


for index, operation in df_operations.iterrows(): #Recorrer cada operación 

    #Cada vez que vamos a procesar una operación de IBKR, tenemos que actualizar la lista de las posiciones que tenemos en
    #nuestra cartera de investing.com
    # Sacar las posiciones que hay en este momento en la cartera:
    time.sleep(5)
    actual_positions_list = get_existing_positions(driver=driver, id_cartera=id_cartera1) #ejemplo: [{'longName': 'Apple Inc', 'row_id': 'row_symbol_41609486_6408_39154437'}]
    #n=operation['name']                                                                                    # Al hacer esto se genera el anuncio de las cookies
    #print(f'###############Operation {index}, {n}################')
    #print('->actual_positions_list :')
    #print(actual_positions_list)

    # Quitar cookies
    wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk"))) 
    element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
    driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script


        #Buscamos si existe el activo ya en nuestras posiciones actuales de la cartera (actual_positions_list)

            ###############################################Add SELL operations #######################################################
                                                                        #Filtramos solo las VENTAS hechas
    if operation['action'] == 'SLD': #SELL operation
        #print('es tipo SELL')

        #1º Mirarmos si ya teníamos el activo en nuestra cartera o no. Si ya lo teníamos recuperamos el id de su fila
        #Además de comprar si está en nuestro portfolio, tenemos que mirar que la posición sea de tipo BUY. Ya que 
        #para hacer el close_position tener que cerrar una posición de una cantidad que tengamos comprada.
        #print('------mirar si ya estaba o no en la cartera:-------')
        print('OPERACIÓN DE IBKR:')
        print(operation['name'])
        diccionario_position_existente = None
        for dict_position in actual_positions_list: #Recorrer cada posición actual de nuestro portfolio
            print('·Nombre de la cartera de investing:')
            print(dict_position['longName'].upper())
            if (operation['name'] == (dict_position['longName']).upper()) and (dict_position['type']=='BUY'): 
                diccionario_position_existente = dict_position
                break
                
        print('-->Resultado de diccionario_position_existente:')
        print(diccionario_position_existente)
        #Ahora ya sabemos si el activo que vamos a procesar de IBKR está o no en nuestra cartera de investing, por lo que
        #ya podemos tomar dos acciones diferentes dependiente de esto:

        if diccionario_position_existente != None: #El activo ya lo tenemos en nuestro portfolio de investing.com --> CLOSE POSITION
            print('Vamos a hacer el CLOSE POSITION')

            # Acceder a la posición de la cartera
            positon_row_btn = driver.find_element("id", diccionario_position_existente['row_id']) #Accedemos a la posición del portfolio 'Cartera 1 - ACTUAL' mediante su ID
            positon_row_btn.click()

            # Una vez dentro de la posición, se desplegan las detail rows, y podemos sacar info:
            detailed_position_list = detail_rows(driver=driver, id_row_position=diccionario_position_existente['row_id']) #Sacar las detailed rows


                                            ############Condiciones según el amount:##########
            detailed_position_list = detail_rows(driver=driver, id_row_position=diccionario_position_existente['row_id']) #Sacar las detailed rows
            
            cantidad_total_a_vender = operation['quantity']

            while cantidad_total_a_vender > 0 and detailed_position_list: #queda cantidad por vender y detailed rows por iterar
                detailed_row = detailed_position_list.pop(0)  # sacar el primer elemento de la lista
                print(f'iteramos en una detail row: {detailed_row}')
                
                amount_sell = min(int(cantidad_total_a_vender), int(detailed_row['amount_detail_row']))
                print('         ·Hacemos close position')
                close_position(driver=driver, date=operation['execTime'], amount=amount_sell, price=operation['execPrice'], id_row_detailed_position=detailed_row['id_detail_row']) # #ejemplo id_position='row_symbol_41609486_6408_39082580'
                cantidad_total_a_vender -= amount_sell #actualizar según vamos vendiendo
                

            if cantidad_total_a_vender == 0:  #ya hemos hecho toda la cantidad de venta
                print("   ·Venta completada")
            else: #queda cantidad por vender, pero ya hemos iterado todas las filas
                add_position(driver=driver, operation=operation, amount=cantidad_total_a_vender, id_cartera=id_cartera1, type='S')
                print("     ·Venta en corto, hacemos add_position")

            
        else: #(diccionario_position_existente == None) #El activo NO lo tenemos en nuestro portfolio de investing.com --> AÑADIR POSICIÓN, type=SELL
                #En este caso, vendemos algo que no tenemos --> operaciones en corto
                #Clickar en el input para add position
                #En este caso, vendemos algo que no tenemos --> operaciones en corto
                #Clickar en el input para add position
            print('Vamos a hacer el ADD POSITION')
            
            add_position(driver=driver, operation = operation, id_cartera = id_cartera1, type='S') #Ejemplo id_cartera='tab_41609486'
                            ###################################################################################




            ###############################################Add BUY operations #######################################################
                                                           #Filtramos solo las COMPRAS hechas
    if operation['action'] == 'BOT': #BUY operation

        #1º Mirarmos si ya teníamos el activo en nuestra cartera o no. Si ya lo teníamos recuperamos el id de su fila
        #Además de comprar si está en nuestro portfolio, tenemos que mirar que la posición sea de tipo SELL. Ya que 
        #empezaremos por el hacer un close_position con la cantidad comprada ahora. 
        #print('------mirar si ya estaba o no en la cartera:-------')
        print('OPERACIÓN DE IBKR:')
        print(operation['name'])
        diccionario_position_existente = None
        for dict_position in actual_positions_list: #Recorrer cada posición actual de nuestro portfolio
            print('·Nombre de la cartera de investing:')
            print(dict_position['longName'].upper())
            if (operation['name'] == (dict_position['longName']).upper()) and (dict_position['type']=='SELL'): 
                diccionario_position_existente = dict_position
                break
                
        print('-->Resultado de diccionario_position_existente:')
        print(diccionario_position_existente)
        #Ahora ya sabemos si el activo que vamos a procesar de IBKR está o no en nuestra cartera de investing, por lo que
        #ya podemos tomar dos acciones diferentes dependiente de esto:


        if diccionario_position_existente != None: #El activo ya lo tenemos en nuestro portfolio de investing.com con tipo SELL--> CLOSE POSITION
            print('Vamos a hacer el CLOSE POSITION')

            # Acceder a la posición de la cartera
            positon_row_btn = driver.find_element("id", diccionario_position_existente['row_id']) #Accedemos a la posición del portfolio 'Cartera 1 - ACTUAL' mediante su ID
            positon_row_btn.click()

            # Una vez dentro de la posición, se desplegan las detail rows, y podemos sacar info:
            detailed_position_list = detail_rows(driver=driver, id_row_position=diccionario_position_existente['row_id']) #Sacar las detailed rows


                                            ############Condiciones según el amount:##########
            detailed_position_list = detail_rows(driver=driver, id_row_position=diccionario_position_existente['row_id']) #Sacar las detailed rows
            
            cantidad_total_a_comprar = operation['quantity']

            while cantidad_total_a_comprar > 0 and detailed_position_list: #queda cantidad por vender y detailed rows por iterar
                detailed_row = detailed_position_list.pop(0)  # sacar el primer elemento de la lista
                print(f'iteramos en una detail row: {detailed_row}')
                
                amount_buy = min(int(cantidad_total_a_comprar), int(detailed_row['amount_detail_row']))
                print('         ·Hacemos close position')
                close_position(driver=driver, date=operation['execTime'], amount=amount_buy, price=operation['execPrice'], id_row_detailed_position=detailed_row['id_detail_row']) # #ejemplo id_position='row_symbol_41609486_6408_39082580'
                cantidad_total_a_comprar -= amount_buy #actualizar según vamos vendiendo
                

            if cantidad_total_a_comprar == 0:  #ya hemos hecho toda la cantidad de compra
                print("     ·Compra completada")
            else: #queda cantidad por compra, pero ya hemos iterado todas las filas. Hacemos compra normal, con add_position
                add_position(driver=driver, operation=operation, amount=cantidad_total_a_comprar, id_cartera=id_cartera1, type='B')
                print("     ·Compra normal, hacemos add_position")



        else: #(diccionario_position_existente == None) #El activo NO lo tenemos en nuestro portfolio de investing.com --> AÑADIR POSICIÓN, type=BUY
                #En este caso, vendemos algo que no tenemos --> operaciones en corto
                #Clickar en el input para add position
                #En este caso, vendemos algo que no tenemos --> operaciones en corto
                #Clickar en el input para add position
            print('Vamos a hacer el ADD POSITION')
            
            add_position(driver=driver, operation = operation, id_cartera = id_cartera1, type='B') #Ejemplo id_cartera='tab_41609486'
                            ###################################################################################






# Establecer un tiempo de espera implícito de 10 segundos
driver.implicitly_wait(10)

    







###################################################################################################################################
###################################################################################################################################
##                                      PASO 2.b - Cargar las operaciones de IBKR a la Cartera 2                                 ##
###################################################################################################################################
###################################################################################################################################
print('--------------------------------CARTERA 2-------------------------------------')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from datetime import datetime
import pdfkit
import os
import pandas as pd


from get_Portfolio_Names import portfolios_Names_and_ID

from pruebas_AddPosition_ConDetail import add_position
from pruebas_ClosePosition_ConDetails import close_position

from existing_positions_Cartera import get_existing_positions

from details_positions import detail_rows


from dotenv import load_dotenv
import os


#Cargar las credenciales de investing.com, que están como variables de entorno
load_dotenv()
user_investing = os.getenv('USER_INVESTING')
print(user_investing)
password_investing =  os.getenv('PASSWORD_INVESTING')

#https://stackoverflow.com/questions/72773206/selenium-python-attributeerror-webdriver-object-has-no-attribute-find-el


# Configuración del controlador de Chrome. # Start a web driver to automate the browser actions
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service("selenium/chromedriver/win32/111.0.5563.64/chromedriver.exe"), options=options)


                            ################### Inicia sesión ###################
driver.get("https://www.investing.com/portfolio") #"https://www.investing.com/portfolio/?portfolioID=ZWQzYDRnMmtiNz02ZTc4Mg%3D%3D"
driver.delete_all_cookies()# Elimina todas las cookies
email_input = driver.find_element("name", "loginFormUser_email")
email_input.send_keys(user_investing)
email_input.send_keys(Keys.RETURN)
password_input = driver.find_element("id", "loginForm_password")
password_input.send_keys(password_investing)
password_input.send_keys(Keys.RETURN)

                                ###########################'My watchlist'###############################
driver.get("https://www.investing.com/portfolio") #Go to 'import watchlist' page. STEP 1

wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk")))

# The cookie company, OneTrust, puts an overlay that protects the button and I can't click it. 
# To fix the error I have to delete from the html of the page the code: '<div id="onetrust-consent-sdk"></div>. 
element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script


                                            ##########Go to 'CARTERA 2'##########

#Primero hay que sacar el ID de la Cartera1 para poder acceder
existing_portfolios = portfolios_Names_and_ID(driver=driver) #nombre y ID de los portfolios de tu cuenta de investing.com
                                                             # ejemplo: [('Cartera 1 - ACTUAL', 'tab_41609486'), ('Cartera 2 - VENDIDAS', 'tab_41639367')]
print(existing_portfolios)

for tuple in existing_portfolios:
    name = tuple[0]
    id = tuple[1]
    if name == 'Cartera 2':
        id_cartera2 = id #example: tab_41609486
#print(id_cartera2)

# Quitar cookies
wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk"))) 
element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script


#Acceder al portfolio de la Cartera2 --> CLICAR
cartera_btn = driver.find_element(By.XPATH, f"//ul[@class='ui-sortable portfolioTabs shortList']/li[@id='{id_cartera2}']") #example: id="tab_41609486"
cartera_btn.click()


driver.implicitly_wait(5)

            ###############################################Add operations #######################################################                                     

            ######### Leer el csv de las operaciones realizadas en IBKR en los últimos 7 días #########
df_operations= pd.read_csv('operationsHistory_IBKR.csv')


for index, operation in df_operations.iterrows(): #Recorrer cada operación hecha en IBKR

    print('--------------------------------------')
    print(f' Operación de IBKR {operation}')

    #Cada vez que vamos a procesar una operación de IBKR, tenemos que actualizar la lista de las posiciones que tenemos en
    #nuestra cartera de investing.com
    # Sacar las posiciones que hay en este momento en la cartera:
    try:
        actual_positions_list = get_existing_positions(driver=driver, id_cartera=id_cartera2) #ejemplo: [{'longName': 'Apple Inc', 'row_id': 'row_symbol_41609486_6408_39154437'}]
        

        #Cuando la cartera2 se vuelve a quedar vacía, hay un problema y en vez de no devolver nada, devuelve los valores None en el diccionario.
        #En ese caso, cambiamos los valores 'None' por 'empty table', para que se pueda seguir ejecutando el resto del código
        for dictionary in actual_positions_list:
            if all(value is None for value in dictionary.values()):
                dictionary.update((key, 'empty table') for key in dictionary.keys())

    except:
        #Al incio la cartera2 estaba vacía, así que la función get_existing_positions devuelve error, porque no hay ninguna tabla
        #Entonces, en este caso nos 'inventamos' un diccionario, para que se pueda seguir ejecutando el resto del código
        actual_positions_list = [{'longName': 'empty table', 'row_id': 'empty table', 'type': 'empty table'}] #Vacío

    print(f'Posiciones que hay ahora en la Cartera2: {actual_positions_list}')

    #n=operation['name']                                                                                    # Al hacer esto se genera el anuncio de las cookies
    #print(f'###############Operation {index}, {n}################')
    #print('->actual_positions_list :')
    #print(actual_positions_list)

    # Quitar cookies
    wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk"))) 
    element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
    driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script


        #Buscamos si existe el activo ya en nuestras posiciones actuales de la cartera (actual_positions_list)

            ###############################################Add SELL operations from IBKR #####################################################
                                                            #Filtramos solo las VENTAS hechas
    if operation['action'] == 'SLD': #SELL operation en IBKR
        ####Una operación de venta (-) de IBKR en la cartera2 se refleja como una operación de compra (+)
        ####Estas operaciones siempre se van a añadir a la cartera2

        print('Vamos a hacer el ADD POSITION')
        add_position(driver=driver, operation = operation, id_cartera = id_cartera2, type='B') #Ejemplo id_cartera='tab_41609486'
                            
                            ###################################################################################




            ###############################################Add BUY operations from IBKR ####################################################
                                                           #Filtramos solo las COMPRAS hechas
    if operation['action'] == 'BOT': #BUY operation en IBKR
        ####Una operación de compra (+) de IBKR en la cartera2 se refleja como una operación de venta (-)

        #### Solo añadimos esa cantidad (en forma de venta->closePosition) en el caso de que el activo ya esté en la cartera2
        #### Si el activo no está en la cartera2, no hacemos nada
        
        
        #1º Mirarmos si ya teníamos el activo en nuestra cartera o no. Si ya lo teníamos recuperamos el id de su fila
        #print('------mirar si ya estaba o no en la cartera:-------')
        #print('OPERACIÓN DE IBKR:')
        #print(operation['name'])
        diccionario_position_existente = None
        for dict_position in actual_positions_list: #Recorrer cada posición actual de nuestro portfolio
            #print('·Nombre de la cartera de investing:')
            print(  '·Mirar si ya existía el activo en la cartera:')
            print(      '-activo a comparar de la cartera2:')
            print(dict_position['longName'])
            print(dict_position['longName'].upper())
            if (operation['name'] == (dict_position['longName']).upper()): 
                diccionario_position_existente = dict_position
                break
                
        print('-->Resultado de diccionario_position_existente:')
        print(diccionario_position_existente)
        #Ahora ya sabemos si el activo que vamos a procesar de IBKR está o no en nuestra cartera de investing, por lo que
        #ya podemos tomar dos acciones diferentes dependiente de esto:


        if diccionario_position_existente != None: #El activo ya lo tenemos en nuestro portfolio de investing.com --> CLOSE POSITION´
            print('Vamos a hacer el CLOSE POSITION')

            # Acceder a la posición de la cartera
            positon_row_btn = driver.find_element("id", diccionario_position_existente['row_id']) #Accedemos a la posición del portfolio 'Cartera 1 - ACTUAL' mediante su ID
            positon_row_btn.click()

            # Una vez dentro de la posición, se desplegan las detail rows, y podemos sacar info:
            detailed_position_list = detail_rows(driver=driver, id_row_position=diccionario_position_existente['row_id']) #Sacar las detailed rows


                                            ############Condiciones según el amount:##########
            detailed_position_list = detail_rows(driver=driver, id_row_position=diccionario_position_existente['row_id']) #Sacar las detailed rows
            
            cantidad_total_a_vender = operation['quantity']

            while cantidad_total_a_vender > 0 and detailed_position_list: #queda cantidad por vender y detailed rows por iterar
                detailed_row = detailed_position_list.pop(0)  # sacar el primer elemento de la lista
                print(f'iteramos en una detail row: {detailed_row}')
                
                amount_sell = min(int(cantidad_total_a_vender), int(detailed_row['amount_detail_row']))
                print('         ·Hacemos close position')
                close_position(driver=driver, date=operation['execTime'], amount=amount_sell, price=operation['execPrice'], id_row_detailed_position=detailed_row['id_detail_row']) # #ejemplo id_position='row_symbol_41609486_6408_39082580'
                cantidad_total_a_vender -= amount_sell #actualizar según vamos vendiendo
                

            if cantidad_total_a_vender == 0:  #ya hemos hecho toda la cantidad de venta
                print("   ·Venta completada")


                            ###################################################################################


# Establecer un tiempo de espera implícito de 10 segundos
driver.implicitly_wait(10)

    



###################################################################################################################################
###################################################################################################################################
##                                      PASO 2.c - Cargar las operaciones de IBKR a la Cartera 3                                 ##
###################################################################################################################################
###################################################################################################################################