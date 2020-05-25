import requests
from bs4 import BeautifulSoup
import time
import datetime
import smtplib

cookies = dict(__stripe_mid='222cf6f7-9584-402e-af65-88bbe6d4dec1', _ga='GA1.2.537459983.1580398833', cookiescriptaccept='visit', language='en_us', __cfduid= 'd7ea705476f69b0de872c3e2c086454d51589670962', fluxSessionData='oil8qoars6inhqnbfl43a9omto', _gid='GA1.2.1139478948.1589829817', __stripe_sid='4fe28e41-b4b9-4235-b628-24ba0d2e2606', _gat_gtag_UA_68821166_1='1')

item_list = []

def enviaEmail(itens, nome_do_item):
    if len(item_list) == 0:
        pass
    else:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('pedrao5723@gmail.com', 'ogqlwutgvblwbnvr')

        mensagem = 'Subject: Achei {nome_do_item}\n\n{itens}'.format(nome_do_item=nome_do_item, itens=itens)
            
        server.sendmail(
            'pedrao5723@gmail.com',
            'pedrogmfeitosa@gmail.com',
            mensagem
        )

        server.quit()

def faz_int_tira_texto(texto):
    semTexto = texto.replace('z', '')
    finalTexto = semTexto.replace(',', '')
    return int(finalTexto)

def getItem(item_id):        
    url = 'https://www.novaragnarok.com/?module=vending&action=item&id={id}'.format(id=item_id)
    data = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(data.text, 'html.parser')
    '''item_name_span = item_name.find('span')
    item_name_text = item_name_span.find('a').text'''
    nome = soup.find('span', { 'class': 'tooltip'}).text
    item_table = soup.find('table', { 'id': 'itemtable' })
    tbody = item_table.find('tbody')

    for tr in tbody.find_all('tr'):
        #nome = item_name.text
        preco = tr.find_all('td')[0].text.strip()
        preco_int = faz_int_tira_texto(preco)
        preco2 = tr.find_all('td')[1].text.strip()
        preco3 = tr.find_all('td')[2].text.strip()
        preco4 = tr.find_all('td')[3].text.strip()
    

        if preco_int < 50000000 and 'Dragon Enemy Resistance +7%' in preco3:        
            msg = '{preco} {preco2} {preco3} {preco4}, {url}'.format(preco=preco, preco2=preco2, preco3=preco3, preco4=preco4, url=url)
            item_list.append(msg)
            
    enviaEmail(item_list, nome)
            

getItem(22208)