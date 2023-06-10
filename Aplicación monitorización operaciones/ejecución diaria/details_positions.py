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
from keys import user_investing, password_investing
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