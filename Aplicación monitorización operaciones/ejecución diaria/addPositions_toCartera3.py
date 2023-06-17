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


