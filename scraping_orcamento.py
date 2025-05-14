# ATENÇÃO >>> TROCAR A 'ABA' DA PÁGINA WEBSITE

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

dic_orcamentos = {'setor': [], 'valor_previsto': [], 'valor_realizado': [], 'mes': [], 'ano': []}

try:
    WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.ID, 'Table'))
    )
except TimeoutException:
    print('>>> TEMPO EXCEDIDO! <<<')

lista_orcamentos = driver.find_elements(By.TAG_NAME, 'tr')

for i in lista_orcamentos:
    try:
        setor = i.find_element(By.CLASS_NAME, 'td_setor').text.strip()
        valor_previsto = i.find_element(By.CLASS_NAME, 'td_valor_previsto').text.strip()
        valor_realizado = i.find_element(By.CLASS_NAME, 'td_valor_realizado').text.strip()
        mes = i.find_element(By.CLASS_NAME, 'td_mes').text.strip()
        ano = i.find_element(By.CLASS_NAME, 'td_ano').text.strip()

        dic_orcamentos['setor'].append(setor)
        dic_orcamentos['valor_previsto'].append(valor_previsto)
        dic_orcamentos['valor_realizado'].append(valor_realizado)
        dic_orcamentos['mes'].append(mes)
        dic_orcamentos['ano'].append(ano)

        print(f'{setor} - {valor_realizado}')

    except Exception as e:
        print('Não foi possível coletar dados: ', e)

driver.quit()

df = pd.DataFrame(dic_orcamentos)
df.to_excel('webscraping_orcamentos.xlsx', index=False)
print(f"Arquivo foi salvo com sucesso {len(df)}")