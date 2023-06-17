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