from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

import pandas as pd

import time

chrome_driver_path = r".\chromedriver\chromedriver.exe"
service = Service(chrome_driver_path) 

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--window_size=1920,1080')

driver = webdriver.Chrome(service=service, options=options)

url_base = 'https://masander.github.io/AlimenticiaLTDA-financeiro/'
driver.get(url_base)

time.sleep(5)

# armazém ITENS
dic_ = {'column1':[], 'column2':[]}
