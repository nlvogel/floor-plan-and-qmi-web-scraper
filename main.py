from bs4 import BeautifulSoup
import requests

url = "https://hhhunthomes.com/regions/richmond/move-in-ready-homes"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())

qmi_list = []
for qmi_card in soup.select('.qmi-card'):
    # data = {
    #     'Listing Name': qmi_card.p.text.split('Community:\n')[1].strip('\n'),
    # }
    # qmi_list.append(data)
    print(qmi_card.p.text.split('Community:\n')[1].strip('\n'))
