#################################################################################################################################
#AddPosition_ConDetail.py
#################################################################################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from keys import user_investing, password_investing
from selenium.webdriver.chrome.service import Service
import pdfkit
import os
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from datetime import datetime



from get_Portfolio_Names import portfolios_Names_and_ID


#df_operations= pd.read_csv('last7days_operations.csv')



#https://stackoverflow.com/questions/72773206/selenium-python-attributeerror-webdriver-object-has-no-attribute-find-el

"""
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
"""

def add_position(driver, operation, id_cartera, type, amount=None):
    #df_operations= pd.read_csv('last7days_operations.csv')


                                    ###########################'My watchlist'###############################
    driver.get("https://www.investing.com/portfolio") #Go to 'import watchlist' page. STEP 1

    time.sleep(1)

    wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk")))

    # The cookie company, OneTrust, puts an overlay that protects the button and I can't click it. 
    # To fix the error I have to delete from the html of the page the code: '<div id="onetrust-consent-sdk"></div>. 
    element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
    driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script

                                            
                                            ##########Go to 'CARTERA 1 - ACTUAL'##########
    #ui-sortable portfolioTabs shortList

    #cartera_btn = driver.find_element(By.XPATH, "//ul[@id='tab_41609486']")
    #id_cartera = 'tab_41609486'
    
    id_number_cartera = id_cartera[4:] #example: '41609486'

    time.sleep(1)
    cartera_btn = driver.find_element(By.XPATH, f"//ul[@class='ui-sortable portfolioTabs shortList']/li[@id='{id_cartera}']")
    cartera_btn.click()

    #Clickar en el input para add position
    time.sleep(1)
    add_position_btn = driver.find_element(By.XPATH, "//div[@class='inlineblock searchBoxContainer topBarSearch ']")
    add_position_btn.click()


    #Escribir el nombre del activo que queremos
    time.sleep(3)
    position_input = add_position_btn.find_element(By.XPATH, "//input[@placeholder='EUR/USD or AAPL']")
    position_input.send_keys(operation['ISIN']) #'AAPL' #'TSLA' #Con el ISIN va mejor que con el symbol, porque no hay confusión

    #Nos quedamos con el primer resultado
    time.sleep(1)
    wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchRowIdtop_0")))
    pick_active_btn = driver.find_element(By.XPATH, "//tr[@id='searchRowIdtop_0']")
    pick_active_btn.click()


    #Rellenar campos:
    time.sleep(1)
    operation_type_id = 'a_operation_' + id_number_cartera
    wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, operation_type_id)))
    #·Type
    select_element = driver.find_element('id', operation_type_id) # Seleccionar el elemento 'select' por su id. Example id='a_operation_41609486'
    select = Select(select_element) # Crear un objeto Select a partir del elemento (from selenium.webdriver.support.ui import Select)
    select.select_by_value(type) # Seleccionar la opción por su valor --> value="S" (sell)

    #·Date
    date = operation['execTime'] #20230420 12:55:55 US/Eastern
    date = str(date)[0:8] #20230420
    date = datetime.strptime(date, '%Y%m%d')
    dia = date.strftime('%d')
    dia = dia.lstrip('0') #Quitar el 0 de delante si lo hay. Los días de un solo dígito están como dia='03', y yo quiero dia='3'
    mes_dot = date.strftime('%b.') #Con el punto al final
    mes = date.strftime('%b') #Sin punto al final  




    #Desplegar el calendario:
    time.sleep(1)
    date_picker = driver.find_element("id", 'datePickerIconWrap') # Clickar en el input de la fecha para desplegar el calendario. Example: id="a_posDate_41609486"
    date_picker.click()
    time.sleep(1)


    #Encontrar mes: 
    month_btn = driver.find_element(By.XPATH, "//span[@class='ui-datepicker-month']")
    month_btn.click()
    try: # El mes de mayo está sin punto al final, xq no es abreviatura --> Ejemplo: 'Apr.' y 'May'
        month_link = month_btn.find_element(By.XPATH, f"//span[contains(text(), '{mes_dot}')]") #mes con punto al final
        month_link.click() # Hacer clic en el mes
    except:
        month_link = month_btn.find_element(By.XPATH, f"//a[@href='#']/span[contains(text(),'{mes}')]") #mes sin punto al final
        month_link.click() # Hacer clic en el mes

    #Encontrar número de día:
    time.sleep(1)
    day_btn = driver.find_element(By.XPATH, f"//td[@data-event='click']/a[contains(text(), '{dia}')]")
    day_btn.click()


    #·Amount
    time.sleep(1)
    amount_id = 'a_amount_' + id_number_cartera #example: id="a_amount_41609486"
    amount_input = driver.find_element('id', amount_id)
    amount_input.clear() #borrar el número que había
    #amount_input.send_keys(int(operation['quantity']))
    if amount is not None: #Le hemos puesto a mano la cantidad a vender en el atributo 'amount' ->Es porque venimos del close position
        amount_input.send_keys(int(amount))
    else: #amount is None
        amount_input.send_keys(int(operation['quantity']))


    #·Price
    time.sleep(1)
    price_id = 'a_price_' + id_number_cartera #example: id="a_price_41609486"
    price_input = driver.find_element('id', price_id)
    price_input.clear() #borrar el número que había
    price_input.send_keys(int(operation['execPrice']))


    # Añadir posición (save)
    time.sleep(1)
    save_id = 'addPositionBtn_' + id_number_cartera #example: id="addPositionBtn_41609486"
    save_btn = driver.find_element(By.ID, save_id)   
    save_btn.click()

    #driver.implicitly_wait(10)

#################################################################################################################################
#addPositions_toCartera3.py
#################################################################################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from keys import user_investing, password_investing
from selenium.webdriver.chrome.service import Service
import pdfkit
import os
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from datetime import datetime



from get_Portfolio_Names import portfolios_Names_and_ID


#df_operations= pd.read_csv('last7days_operations.csv')



#https://stackoverflow.com/questions/72773206/selenium-python-attributeerror-webdriver-object-has-no-attribute-find-el

"""
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
"""

def add_position_toCartera3(driver, name, amount, price,  id_cartera, date, type='S'):
    #df_operations= pd.read_csv('last7days_operations.csv')


                                    ###########################'My watchlist'###############################
    driver.get("https://www.investing.com/portfolio") #Go to 'import watchlist' page. STEP 1

    wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk")))

    # The cookie company, OneTrust, puts an overlay that protects the button and I can't click it. 
    # To fix the error I have to delete from the html of the page the code: '<div id="onetrust-consent-sdk"></div>. 
    element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
    driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script

                                            
                                            ##########Go to 'CARTERA 1 - ACTUAL'##########
    #ui-sortable portfolioTabs shortList

    #cartera_btn = driver.find_element(By.XPATH, "//ul[@id='tab_41609486']")
    #id_cartera = 'tab_41609486'
    
    id_number_cartera = id_cartera[4:] #example: '41609486'


    cartera_btn = driver.find_element(By.XPATH, f"//ul[@class='ui-sortable portfolioTabs shortList']/li[@id='{id_cartera}']")
    cartera_btn.click()

    #Clickar en el input para add position
    time.sleep(1)
    add_position_btn = driver.find_element(By.XPATH, "//div[@class='inlineblock searchBoxContainer topBarSearch ']")
    add_position_btn.click()


    #Escribir el NOMBRE del activo que queremos
    time.sleep(1)
    position_input = add_position_btn.find_element(By.XPATH, "//input[@placeholder='EUR/USD or AAPL']")
    position_input.send_keys(name) #'AAPL' #'TSLA' #Con el ISIN va mejor que con el symbol, porque no hay confusión

    #Nos quedamos con el primer resultado
    time.sleep(1)
    wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchRowIdtop_0")))
    pick_active_btn = driver.find_element(By.XPATH, "//tr[@id='searchRowIdtop_0']")
    pick_active_btn.click()


    #Rellenar campos:
    operation_type_id = 'a_operation_' + id_number_cartera
    wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, operation_type_id)))
    
    #·TYPE
    select_element = driver.find_element('id', operation_type_id) # Seleccionar el elemento 'select' por su id. Example id='a_operation_41609486'
    select = Select(select_element) # Crear un objeto Select a partir del elemento (from selenium.webdriver.support.ui import Select)
    select.select_by_value(type) # Seleccionar la opción por su valor --> value="S" (sell)

    #·DATE
    date = datetime.strptime(date, '%m/%d/%Y') #'06/14/2023'
    date = date.strftime('%Y%m%d') #--> 20230614        Cambiar formato para procesarlo como antes


    date = datetime.strptime(date, '%Y%m%d') #Separar por partes: Y m d
    dia = date.strftime('%d')
    dia = dia.lstrip('0') #Quitar el 0 de delante si lo hay. Los días de un solo dígito están como dia='03', y yo quiero dia='3'
    mes_dot = date.strftime('%b.') #Con el punto al final
    mes = date.strftime('%b') #Sin punto al final  




    #Desplegar el calendario:
    date_picker = driver.find_element("id", 'datePickerIconWrap') # Clickar en el input de la fecha para desplegar el calendario. Example: id="a_posDate_41609486"
    date_picker.click()
    time.sleep(1)


    #Encontrar mes: 
    month_btn = driver.find_element(By.XPATH, "//span[@class='ui-datepicker-month']")
    month_btn.click()
    try: # El mes de mayo está sin punto al final, xq no es abreviatura --> Ejemplo: 'Apr.' y 'May'
        month_link = month_btn.find_element(By.XPATH, f"//span[contains(text(), '{mes_dot}')]") #mes con punto al final
        month_link.click() # Hacer clic en el mes
    except:
        month_link = month_btn.find_element(By.XPATH, f"//a[@href='#']/span[contains(text(),'{mes}')]") #mes sin punto al final
        month_link.click() # Hacer clic en el mes

    #Encontrar número de día:
    day_btn = driver.find_element(By.XPATH, f"//td[@data-event='click']/a[contains(text(), '{dia}')]")
    day_btn.click()


    #·AMOUNT
    amount_id = 'a_amount_' + id_number_cartera #example: id="a_amount_41609486"
    amount_input = driver.find_element('id', amount_id)
    amount_input.clear() #borrar el número que había
    #amount_input.send_keys(int(operation['quantity']))

    amount_input.send_keys(int(amount))



    #·PRICE
    price_id = 'a_price_' + id_number_cartera #example: id="a_price_41609486"
    price_input = driver.find_element('id', price_id)
    price_input.clear() #borrar el número que había
    
    price_input.send_keys(float(price))


    # Añadir posición (save)
    save_id = 'addPositionBtn_' + id_number_cartera #example: id="addPositionBtn_41609486"
    save_btn = driver.find_element(By.ID, save_id)   
    save_btn.click()

    #driver.implicitly_wait(10)



#################################################################################################################################
#ClosePosition_ConDetails.py
#################################################################################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from keys import user_investing, password_investing
from selenium.webdriver.chrome.service import Service
import pdfkit
import os
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from datetime import datetime

from selenium.webdriver.common.by import By

from AddPosition_ConDetail import add_position


#df_operations= pd.read_csv('last7days_operations.csv')
"""
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
"""

#POSICIÓN DE LA CARTERA --> id_position
#DETALLES DE ESA POSICIÓN --> detailed_position_list = detail_rows(driver=driver, id_row_position=id_row_position)


#Con argumentos
def close_position(driver, date, amount, price, id_row_detailed_position):
    from selenium.webdriver.common.by import By

                                    ###########################'My watchlist'###############################

    # Click Close position
    #edit_position_button = driver.find_element(By.XPATH, "//div[@class='js-close-position']") #js-edit-position
    time.sleep(1)
    edit_position_button = driver.find_element(By.XPATH, f"//div[@class='js-close-position' and @data-row='{id_row_detailed_position}']")
    edit_position_button.click()


    # ·Date
    #df_buy_operations= pd.read_csv('last7days_operations.csv')
    #date = operation['execTime'] #20230420 12:55:55 US/Eastern
    date = str(date)[0:8] #20230420
    date = datetime.strptime(date, '%Y%m%d')
    dia = date.strftime('%d')
    dia = dia.lstrip('0') #Quitar el 0 de delante si lo hay. Los días de un solo dígito están como dia='03', y yo quiero dia='3'
    mes_dot = date.strftime('%b.') #Con punto al final
    mes = date.strftime('%b') #Sin punto al final  


    # Desplegar el calendario
    time.sleep(1)
    id_calendario = 'widgetFieldDateRange' + id_row_detailed_position
    date_picker = driver.find_element("id", id_calendario) # Clickar en el input de la fecha para desplegar el calendario
    date_picker.click()

    # Hacer clic en el botón del AÑO para cambiarlo --> Siempre va a ser 2023
    #year_btn = driver.find_element(By.XPATH, "//span[@class='ui-datepicker-year']")
    #year_btn.click()


    # Hacer clic en el botón del MES para cambiarlo
    time.sleep(1)
    month_btn = driver.find_element(By.XPATH, "//span[@class='ui-datepicker-month']")
    month_btn.click()
    # Encontrar el MES que quiero
    ###APUNTE!!! Con el 'close position' solo puedo escoger el mes actual --> POR LO TANTO, REALMENTE ESTA PARTE LA PODRÍAMOS QUITAR, PORQUE NO HARÍA FALTA ESCOGER MES
    try:  # El mes de mayo está sin punto al final, xq no es abreviatura --> Ejemplo: 'Apr.' y 'May'
        month_link = month_btn.find_element(By.XPATH, f"//span[contains(text(),'{mes_dot}')]")
        month_link.click() # Hacer clic en el mes
    except: 
        month_link = month_btn.find_element(By.XPATH, f"//a[@href='#']/span[contains(text(),'{mes}')]")
        month_link.click() # Hacer clic en el mes

    # Econtar el NÚMERO DE DÍA que quiero
    ###APUNTE!!! Con el 'close position' solo puedo elegir el día actual o el anterior
    #day_btn = driver.find_element(By.XPATH, "//td/a[contains(text(), bought_dia)]")
    time.sleep(4)
    day_btn = driver.find_element(By.XPATH, f"//td[@data-event='click']/a[contains(text(), '{dia}')]")
    day_btn.click()



    # ·Amount variable
    time.sleep(1)
    id_amount_input = 'amount' + id_row_detailed_position #example: "amountrow_symbol_41609486_6408_39082580"
    amount_input = driver.find_element("id", id_amount_input)
    amount_input.clear() #borrar el número que había
    #amount_input.send_keys(operation['quantity'])
    time.sleep(1)
    amount_input.send_keys(int(amount))


    # .Price
    time.sleep(1)
    id_price_input = 'curPrice' + id_row_detailed_position #example: "curPricerow_symbol_41609486_6408_39082580"
    close_price_input = driver.find_element("id", id_price_input)
    close_price_input.clear() #borrar el número que había
    close_price_input.send_keys(int(price))


    #Close position (save)
    time.sleep(1)
    id_save_position = 'closeBtn' + id_row_detailed_position #example: "closeBtnrow_symbol_41609486_6408_39082580"
    save_btn = driver.find_element(By.ID, id_save_position)   #editBtnrow_symbol_41609486_6408_39027001
    save_btn.click()


    #valor_actual = amount_input.get_attribute("value")
    #print(type(valor_actual))

    #time.sleep(10) # Espera 10 segundos


#################################################################################################################################
#create_portfolios.py
#################################################################################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pdfkit
import os

from dotenv import load_dotenv
import os


#Cargar las credenciales de investing.com, que están como variables de entorno
load_dotenv()
user_investing = os.getenv('USER_INVESTING')
print(user_investing)
password_investing =  os.getenv('PASSWORD_INVESTING')


def crear_cartera_holdings(nombre_cartera):
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


                    #####################################Create new portfolio ############################################
    # New portfolio button (+)
    new_portfolio_btn = driver.find_element(By.CSS_SELECTOR, 'span[data-tooltip="Create a New Portfolio"]')
    new_portfolio_btn.click()

    #Portfolio type (watchlist or positions):
    holdings_btn = driver.find_element(By.CSS_SELECTOR, 'div[class="portfolioIcon float_lang_base_2"]') #holdings type
    holdings_btn.click()

    #portfolio name
    portfolio_name_field = driver.find_element(By.ID, 'newPortfolioText') #text input
    portfolio_name_field.send_keys(nombre_cartera) # Escribir el nombre de la cartera en el campo de texto


    # Create
    create_btn = driver.find_element(By.ID, 'createPortfolio') # Localizar el botón "Create"
    create_btn.click() # Hacer clic en el botón "Create"



"""#CREAR LAS DOS CARTERAS
crear_cartera_holdings(nombre_cartera='Cartera 1')
crear_cartera_holdings(nombre_cartera='Cartera 2')
crear_cartera_holdings(nombre_cartera='Cartera 3')
"""


#################################################################################################################################
#details_positions_information.py
#################################################################################################################################
"""
Al pinchar en una posición (en una fila de la tabla de la cartera) para cerrar posición, queremos saber si hay más de una fila,
es decir si hay varias posiciones para iterar por ellas si hiciera falta y cerrarlas.
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pdfkit
import os
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time
import requests


from selenium.webdriver.common.by import By

"""
#df_operations= pd.read_csv('last7days_operations.csv')

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
element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script


#Pinchar en la posición:
# Acceder a la posición de la cartera (tesla por ejemplo)
id_row_position =  "row_symbol_43097234_252_39914387" #"row_symbol_41609486_6408_39082580"
position_row_btn = driver.find_element("id", id_row_position) #Accedemos a la posición del portfolio 'Cartera 1 - ACTUAL' mediante su ID
position_row_btn.click()
"""



def detail_rows(driver, name, id_row_position):
                                                ###################BS###################
    # Obtener el código HTML de la página actual
    time.sleep(5)
    page_html = driver.page_source

    # Parsear el código HTML con BeautifulSoup
    time.sleep(5)
    soup = BeautifulSoup(page_html, 'html.parser')#Para hacer el web scraping
    print()

    time.sleep(5)
    id_detials_rows = 'details_' + id_row_position #ejemplo: "details_row_symbol_41609486_13994_39136031"
    print(id_detials_rows)
    
    time.sleep(5)
    tr_details_tag = soup.find('tr', {'id': id_detials_rows }) #the table
    
    
    time.sleep(5)
    div_tag_list = tr_details_tag.find_all('div')

    detailed_position_list = [] # Sacamos el id de las subfilas de la posición
    for div in div_tag_list: #for each row, i.e, for each portfolio position

        #·DETAIL ROW ID
        id = div.get('data-id') #ejemplo: data-id="row_symbol_41609486_13994_39136031"
        if id is not None:
            d_row = {}
            
            #·AMOUNT
            amount_id = "amount" + id #amountrow_symbol_41609486_13994_39136031
            input_amount_tag = div.find('input', {'id': amount_id})
            amount = input_amount_tag.get('value')

            #·OPEN PRICE
            price_id = "curPrice" + id #id="curPricerow_symbol_43097234_252_39914387"
            input_price_tag = div.find('input', {'id': price_id})
            price = input_price_tag.get('value')

            #·DATE
            date_id = "widgetFieldDateRange" + id  #id="widgetFieldDateRangerow_symbol_43097234_252_39914387"
            input_date_tag = div.find('div', {'id': date_id})
            date = input_date_tag.text.strip()




            #añadir al diccionario
            d_row['id_detail_row'] = id
            d_row['amount_detail_row'] = amount
            d_row['price_detail_row'] = price
            d_row['date_detail_row'] = date
            d_row['active_name'] = name

            detailed_position_list.append(d_row)

    return detailed_position_list



"""
#EJECUTAR LA FUNCIÓN
detailed_position_list = detail_rows(driver=driver, name='gffj', id_row_position=id_row_position)
print(detailed_position_list)
#output --> [{'id_detail_row': 'row_symbol_41609486_13994_39136031', 'amount_detail_row': '4'}, {'id_detail_row': 'row_symbol_41609486_13994_39135309', 'amount_detail_row': '2'}]
"""


#################################################################################################################################
#details_positions.py
#################################################################################################################################
"""
Al pinchar en una posición (en una fila de la tabla de la cartera) para cerrar posición, queremos saber si hay más de una fila,
es decir si hay varias posiciones para iterar por ellas si hiciera falta y cerrarlas.
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from keys import user_investing, password_investing
from selenium.webdriver.chrome.service import Service
import pdfkit
import os
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time
import requests


from selenium.webdriver.common.by import By

"""
#df_operations= pd.read_csv('last7days_operations.csv')

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
element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script


#Pinchar en la posición:
# Acceder a la posición de la cartera (tesla por ejemplo)
id_row_position =  "row_symbol_41609486_13994_39136031" #"row_symbol_41609486_6408_39082580"
position_row_btn = driver.find_element("id", id_row_position) #Accedemos a la posición del portfolio 'Cartera 1 - ACTUAL' mediante su ID
position_row_btn.click()
"""



def detail_rows(driver, id_row_position):
                                                ###################BS###################
    # Obtener el código HTML de la página actual
    page_html = driver.page_source

    # Parsear el código HTML con BeautifulSoup
    soup = BeautifulSoup(page_html, 'html.parser')#Para hacer el web scraping

    id_detials_rows = 'details_' + id_row_position #ejemplo: "details_row_symbol_41609486_13994_39136031"
    tr_details_tag = soup.find('tr', {'id': id_detials_rows }) #the table
    div_tag_list = tr_details_tag.find_all('div')

    detailed_position_list = [] # Sacamos el id de las subfilas de la posición
    for div in div_tag_list: #for each row, i.e, for each portfolio position
        id = div.get('data-id') #ejemplo: data-id="row_symbol_41609486_13994_39136031"
        if id is not None:
            d_row = {}
            
            price_id = "amount" + id #amountrow_symbol_41609486_13994_39136031
            input_price_tag = div.find('input', {'id': price_id})
            amount = input_price_tag.get('value')

            d_row['id_detail_row'] = id
            d_row['amount_detail_row'] = amount

            detailed_position_list.append(d_row)

    return detailed_position_list



"""
#EJECUTAR LA FUNCIÓN
detailed_position_list = detail_rows(driver=driver, id_row_position=id_row_position)
print(detailed_position_list)
#output --> [{'id_detail_row': 'row_symbol_41609486_13994_39136031', 'amount_detail_row': '4'}, {'id_detail_row': 'row_symbol_41609486_13994_39135309', 'amount_detail_row': '2'}]
"""

#################################################################################################################################
#download_orders.py
#################################################################################################################################
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




#################################################################################################################################
#existing_positions_Cartera.py
#################################################################################################################################
"""
Función para sacar una lista con las posiciones que tenemos en nuestra cartera de investing.com en el momento actual.
Esto nos servirá para, a la hora de añadir compras y ventas de IBKR, poder comprobar primero si el activo está presente 
ya en nuestra cartera o no.


Output --> lista de diccionarios: [{'longName': 'Apple Inc', 'row_id': 'row_symbol_41609486_6408_39154437'}, {'longName': 'Apple Inc', 
                                    'row_id': 'row_symbol_41609486_6408_39082580'}, {'longName': 'Tesla Inc', 'row_id': 'row_symbol_41609486_13994_39136031'}, 
                                    {'longName': 'Meta Platforms Inc', 'row_id': 'row_symbol_41609486_26490_39079129'}, 
                                    {'longName': 'Netflix Inc', 'row_id': 'row_symbol_41609486_13063_39027003'}, 
                                    {'longName': 'Airtificial Intelligence Structures SA', 'row_id': 'row_symbol_41609486_32184_39027002'}]
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from keys import user_investing, password_investing
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from datetime import datetime
import pdfkit
import os

#venimos de pinchar en 'CARTERA 1 - ACTUAL'
def get_existing_positions(driver, id_cartera):
    url_cartera1 = driver.current_url
    #print(f'- URL: {url_cartera1}')
    driver.get(url_cartera1)
    soup = BeautifulSoup(driver.page_source, "html.parser") #Para hacer el web scraping y sacar los nombres de los activos que tenemos
    #print(soup)
    id_number_cartera1 = 'positionstable_' + id_cartera[4:] #quitar el principio de 'tab_' para quedarnos solo con los números
    #print(f'-id number: {id_number_cartera1}') 
    table_tag = soup.find('table', {'id': id_number_cartera1}) #the table
    #print(table_tag)
    

    table_body_tag = table_tag.find('tbody')
    tr_tag_list = table_body_tag .find_all('tr') #each row of the table
    
    actual_actives_list = [] # Sacamos los nombres de los activos que están en nuestra Cartera1 en este momento
    for tr in tr_tag_list: #for each row, i.e, for each portfolio position
        d={} #long name: xxx, id: xxx .   Nos guardamos tanto el nombre del activo como el id de la fila, por si necesitamos recuperarlo luegos
        d['longName'] = tr.get('data-fullname') #example: data-fullname="Apple Inc"
        d['row_id'] = tr.get('id') #example: id="row_symbol_41609486_6408_39154437"
        d['type'] =tr.get('data-operation') #example: data_operation="SELL"
        actual_actives_list.append(d)

    return actual_actives_list


#################################################################################################################################
#get_Portfolio_Names.py
#################################################################################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from keys import user_investing, password_investing
from selenium.webdriver.chrome.service import Service
import pdfkit
import os


def portfolios_Names_and_ID(driver): #Poner el driver, así no hará falta volver a logearse

    #####################   GET THE NAMES OF THE EXISTING PORTFOLIOS    ######################
    #Two types: ·Watchlis, ·Positions
    existing_portfolios_watchlist = [] #portfolio name
    existing_portfolios_positions = [] #portfolio name

    driver.get("https://www.investing.com/portfolio") #'My watchlist page'
    url_portfolios = driver.current_url #Cuando entras al link de /portfolios, automáticamente se cambia señalando al id del primer portfolio, 
                                        #por ejemplo, cambia a: https://www.investing.com/portfolio/?portfolioID=YmM3ZG88NWw%2Bazw3NWc1Pw%3D%3D
    driver.get(url_portfolios)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    watchlist_tag = soup.find('div', {'class': 'js-scrollability-wrapper slideWrapper float_lang_base_1 noSlide'}) #barra donde están los nombres de los portfolios que tengo
    li_list_tag = watchlist_tag.find_all('li') #each portfolio info
    for li in li_list_tag:
        #Portfolio name:
        title = li.get('title') 
        id = li.get('id')

        #Check the portfolio type:
        portfolio_type_tag_list = li.find_all('span')
        portfolio_type_tag = portfolio_type_tag_list[1] #The second 'span' contains the portfolio type
        type = portfolio_type_tag.get('class')
        if type == ['watchlistIcon', 'middle', 'portfolioImg']: 
            existing_portfolios_watchlist.append((title, id))
        if type == ['positionIcon', 'middle', 'portfolioImg']:
            existing_portfolios_positions.append((title, id))

    #print(f'·WATCHLIST names: {existing_portfolios_watchlist}')
    #print(f'·POSITIONS names: {existing_portfolios_positions}')
    return existing_portfolios_positions


#################################################################################################################################
#getISIN.py
#################################################################################################################################
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



#################################################################################################################################
#my_trades.py
#################################################################################################################################
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
