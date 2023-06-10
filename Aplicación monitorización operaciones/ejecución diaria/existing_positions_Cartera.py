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
from keys import user_investing, password_investing
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