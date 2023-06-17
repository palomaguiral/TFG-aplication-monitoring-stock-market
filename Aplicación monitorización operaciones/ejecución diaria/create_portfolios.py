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

