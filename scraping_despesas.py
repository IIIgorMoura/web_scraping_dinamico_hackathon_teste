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
dic_despesas = {'id_despesa': [], 'setor': [], 'tipo': [], 'valor': [], 'data':[], 'tipo':[], }
# dic_orcamentos = {'setor': [], 'valor_previsto': [], 'valor_realizado': [], 'mes': [], 'ano': []}

while True:
    try:
        WebDriverWait(driver,10).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
        )
        print('Elementos encontrados com sucesso!')

    except TimeoutException:
        print('Tempo de espera excedido!')

    # tabela = driver.find_elements(By.ID, 'Table')
    lista_despesas = driver.find_elements(By.TAG_NAME, 'td')

    for i in lista_despesas:
        try:
            id_despesa = i.find_element(By.CLASS_NAME, 'td_id_despesa').text.strip()
            data = i.find_element(By.CLASS_NAME, 'td_data').text.strip()
            tipo = i.find_element(By.CLASS_NAME, 'td_tipo').text.strip()
            setor = i.find_element(By.CLASS_NAME, 'td_setor').text.strip()
            valor = i.find_element(By.CLASS_NAME, 'td_valor').text.strip()
            fornecedor = i.find_element(By.CLASS_NAME, 'td_fornecedor').text.strip()

            dic_despesas['id_despesa'].append(id_despesa)
            dic_despesas['tipo'].append(tipo)
            dic_despesas['data'].append(data)
            dic_despesas['setor'].append(setor)
            dic_despesas['valor'].append(valor)
            dic_despesas['fornecedor'].append(fornecedor)

        except Exception:
            print('Erro ao coletar dados: ', Exception)
    break
        

df = pd.DataFrame(dic_despesas)
df.to_excel('webscraping_despesas.xlsx',index=False)
print(f"Arquivo foi salvo com sucesso {len(df)}")