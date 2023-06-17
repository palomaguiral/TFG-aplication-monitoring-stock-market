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
