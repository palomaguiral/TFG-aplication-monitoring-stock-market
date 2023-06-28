###################################################################################################################################
###################################################################################################################################
##                                      PASO 1 - Descarga del portfolio de IBKR                                                  ##
###################################################################################################################################
###################################################################################################################################

print('-----------------------PASO 1-----------------------')
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer
import time


from dependencies import PortfolioApp, ISINApp


# ·PortfolioApp
appPortfolio = PortfolioApp()
appPortfolio.connect("127.0.0.1", 7497, 0)
Timer(5, appPortfolio.stop).start()
appPortfolio.run()


# returned values:
print(appPortfolio.symbol)
print(appPortfolio.sectype)
print(appPortfolio.exchange)
print(appPortfolio.currency)
print(appPortfolio.positionn)
print(appPortfolio.marketPrice)
print(appPortfolio.marketValue)
print(appPortfolio.averageCost)
print(appPortfolio.unrealizedPNL)
print(appPortfolio.realizedPNL)
print(appPortfolio.accountName)

# ·ISINapp
isins = []
names = []

symbols = appPortfolio.symbol
secs = appPortfolio.sectype
exs = appPortfolio.exchange
currencies = appPortfolio.currency
print('numero de operaciones')
print(len(appPortfolio.symbol))
for i in range(len(appPortfolio.symbol)):
    appISIN = ISINApp()

    appISIN.connect("127.0.0.1", 7497, 1000)

    mycontract = Contract()

    mycontract.symbol = symbols[i]
    mycontract.secType = secs[i]
    mycontract.exchange = exs[i]
    mycontract.currency = currencies[i]

        # Or you can use just the Contract ID
        # mycontract.conId = 552142063


    time.sleep(1)

    appISIN.reqContractDetails(1, mycontract)

    appISIN.run()

    isins.append(appISIN.isin)
    names.append(appISIN.longname)

print(isins)
print(names)

# SAVE
import pandas as pd
data = {'name':names, 'ISIN': isins, 'sectype': appPortfolio.sectype, 'exchange': appPortfolio.exchange,
        'position': appPortfolio.positionn, 'marketPrice':appPortfolio.marketPrice, 'marketValue': appPortfolio.marketValue,
        'averageCost':appPortfolio.averageCost, 'unrealizedPNL': appPortfolio.unrealizedPNL, 
        'realizedPNL':appPortfolio.realizedPNL, 'accountName': appPortfolio.accountName }
df = pd.DataFrame(data)

print(df)

df.to_csv('./initial_IBKR_portfolio.csv', index=False)



###################################################################################################################################
###################################################################################################################################
##                                       PASO 2 - Crear portfolios vacíos en IBKR                                                ##
###################################################################################################################################
###################################################################################################################################
print('-----------------------PASO 2-----------------------')
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

    driver.quit()



crear_cartera_holdings(nombre_cartera='Cartera 1')
crear_cartera_holdings(nombre_cartera='Cartera 2')
crear_cartera_holdings(nombre_cartera='Cartera 3')



###################################################################################################################################
###################################################################################################################################
##                                      PASO 3 - Importar portfolio a la Cartera 1                                               ##
###################################################################################################################################
###################################################################################################################################

print('-----------------------PASO 3-----------------------')
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

####################################Inside 'Import Watchlist'#####################################################

# ·Needed variables:
#-csv file:
current_directory = os.getcwd() # Get the current working directory
#csv_name = "positions_example.csv"             #Needed variables: ISIN/Ticker, Open Price, Amount
#csv_path = os.path.join(current_directory, "positions_example.csv")
csv_name = "initial_IBKR_portfolio.csv"             #Needed variables: ISIN/Ticker, Open Price, Amount
csv_path = os.path.join(current_directory, csv_name)

#-portfolio name:
portfolio_name =  "Cartera 1" #"Cartera 1 - ACTUAL"



# ·STEP 1
driver.get("https://www.investing.com/portfolio/importcsvstep1") #Go to 'import watchlist' page. STEP 1

wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk")))

# The cookie company, OneTrust, puts an overlay that protects the button and I can't click it. 
# To fix the error I have to delete from the html of the page the code: '<div id="onetrust-consent-sdk"></div>. 
element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script


#Upload your existing portfolio file. (Browse file):
fileInput = driver.find_element("name", "uploadFile")
fileInput.send_keys(csv_path)  #CSV path #"C:/Users/usuario/_ TFG GitHub _/TFG-repository/csv_prueba_subir.csv"

#Portfolio type (watchlist or positions):
portfolio_type_btn = driver.find_element("id", "importToPositions") #·Positions
portfolio_type_btn.click()


#Import to: 
portfolioInput = driver.find_element("name", "importTarget")
portfolioInput.send_keys(portfolio_name)            #PORTFOLIO NAME!!!!


#Portfolio currency (It is in USD by default)


#Next:
btn = driver.find_element("id", "importNextBtn")
btn.click()# Click the button 'next'


# ·STEP 2
#First wait until the element we want appears
wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk")))

#Delete cookies
element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script

#Select all the stocks (all the rows) in the csv:
checkbox = driver.find_element("id", "deleteAllRows")
checkbox.click()

#Next:
btn2 = driver.find_element("id", "step2NextBtn")
btn2.click()

# ·STEP 3
#First wait until the element we want appears
wait_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-consent-sdk")))

#Delete cookies
element = driver.find_element("id", "onetrust-consent-sdk")# Find the OneTrust consent SDK element
driver.execute_script("arguments[0].remove();", element)# Delete the element from the DOM using execute_script

#Select all the rows:
checkbox = driver.find_element("id", "deleteAllRows")
checkbox.click()

#Import button:
import_watchlist_button = driver.find_element(By.LINK_TEXT, 'Import Watchlist') # find the 'Import Watchlist' button by its link text
import_watchlist_button.click() # click the button

#Confirmation box
yes_button = driver.find_element("id", "yesBtn")
yes_button.click()

##############################################################################################################################


#######################################################Close##################################################################
# wait for the footer element to appear on the page
#wait = WebDriverWait(driver, 10)
#footer_element = wait.until(EC.presence_of_element_located((By.ID, "footer")))
#input("Press Enter to close the browser...")# keep the browser open until you manually close it

driver.quit()# Cierra el controlador de Chrome
