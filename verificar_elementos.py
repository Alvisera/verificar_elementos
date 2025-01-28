# verificarElementos(): Pega elementos em uma página e me retorna
# conferirElementosExcel(): Pega os elementos de cada site e compara as informações que faltam

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import pandas as pd

def iniciar_navegador(com_debugging_remoto=True):
    #chrome_driver_path = ChromeDriverManager().install()
    chrome_driver_path = r'C:\Users\gabriel.alvise\.wdm\drivers\chromedriver\win64\130.0.6723.91\chromedriver-win32/chromedriver.exe'
    chrome_driver_executable = os.path.join(os.path.dirname(chrome_driver_path), 'chromedriver.exe')
    #print(chrome_driver_path)
    
    if not os.path.isfile(chrome_driver_executable):
        raise FileNotFoundError(f"O ChromeDriver não foi encontrado em {chrome_driver_executable}")

    service = Service(executable_path=chrome_driver_executable)
    
    chrome_options = Options()
    if com_debugging_remoto:
        remote_debugging_port = 9222
        chrome_options.add_experimental_option("debuggerAddress", f"localhost:{remote_debugging_port}")
    
    navegador = webdriver.Chrome(service=service, options=chrome_options)
    return navegador

navegador = iniciar_navegador()

def verificarElementos():
    soup = BeautifulSoup(navegador.page_source, "html.parser")
    spans = soup.find_all('span')  
    informacoes = [span.text.strip() for span in spans]

    for info in informacoes:
        print(info)

def conferirElementosExcel():
    arquivo_excel = "elementos.xlsx"
    nome_planilha = "Planilha1"

    df = pd.read_excel(arquivo_excel, sheet_name=nome_planilha)

    print("Nomes das colunas no arquivo:", df.columns)

    coluna_a = df['A'].dropna().astype(str) if 'A' in df.columns else df[df.columns[0]].dropna().astype(str)
    coluna_b = df['B'].dropna().astype(str) if 'B' in df.columns else df[df.columns[1]].dropna().astype(str)

    faltantes_em_a = coluna_b[~coluna_b.isin(coluna_a)]

    faltantes_em_b = coluna_a[~coluna_a.isin(coluna_b)]

    print("Valores que estão na coluna B, mas não na coluna A:")
    print(faltantes_em_a)

    print("\nValores que estão na coluna A, mas não na coluna B:")
    print(faltantes_em_b)

    resultado_excel = "resultados_comparacao.xlsx"
    with pd.ExcelWriter(resultado_excel) as writer:
        faltantes_em_a.to_frame(name='Faltantes em A').to_excel(writer, index=False, sheet_name="Faltantes em A")
        faltantes_em_b.to_frame(name='Faltantes em B').to_excel(writer, index=False, sheet_name="Faltantes em B")

    print(f"Resultados salvos em: {resultado_excel}")

verificarElementos()
