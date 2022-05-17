from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_mls_id(url):
    mls_response = requests.get(url)
    mls_soup = BeautifulSoup(mls_response.text, 'html.parser')
    mls_text = mls_soup.find('span', {'class': 'community__mls-number'}).text.split('MLS#')[1].split('\n')[1].lstrip()
    if ' | ' in mls_text:
        altered = mls_text.split(' | ')[0]
        return altered
    return mls_text

community_city = {
    'Central Crossing': ('Aylett, VA', 'Single-family Home'),
    'FoxCreek Homestead': ('Moseley, VA', 'Single-family Home'),
    'Giles - The Cove': ('Mechanicsville, VA', 'Single-family Home'),
    'Giles - Townhomes': ('Mechanicsville, VA', 'Townhome'),
    'Governor\'s Retreat': ('Richmond, VA', 'Single-family Home'),
    'Magnolia Green Single Family': ('Moseley, VA', 'Single-family Home'),
    'Magnolia Green Townhomes': ('Moseley, VA', 'Townhome'),
    'Maidstone Village Townhomes': ('New Kent, VA', 'Townhome'),
    'Meadowville Landing - Twin Rivers': ('Chester, VA', 'Single-family Home'),
    'Mosaic at West Creek': ('Richmond, VA', 'Townhome'),
    'The Pointe at Twin Hickory': ('Short Pump, VA', 'Condominium'),
    'River Mill Townhomes': ('Glen Allen, VA', 'Townhome'),
    'Rutland Grove': ('Mechanicsville, VA', 'Single-family Home'),
    'Sandler Station': ('North Chesterfield, VA', 'Condominium'),
    'Wescott': ('Midlothian, VA', 'Townhome'),
    'Wescott Condos': ('Midlothian, VA', 'Condominium'),
    'Taylor Farm': ('Mechanicsville, VA', 'Single-family Home'),
    'Quarterpath at Williamsburg Condos': ('Williamsburg, VA', 'Condominium'),
    'Meadows Landing': ('Suffolk, VA', 'Single-family Home'),
    'River Highlands': ('Suffolk, VA', 'Single-family Home'),
    'Banks Pointe': ('Raleigh, NC', 'Single-family Home'),
    'Dayton Woods': ('Raleigh, NC', 'Single-family Home'),
    'Enclave at Leesville': ('Durham, NC', 'Single-family Home'),
    'Granite Falls Estates': ('Rolesville, NC', 'Single-family Home'),
    'The Reserve at Wackena': ('Cary, NC', 'Single-family Home')
}

url_list = ['https://hhhunthomes.com/regions/richmond/move-in-ready-homes',
            'https://hhhunthomes.com/regions/williamsburg/move-in-ready-homes',
            'https://hhhunthomes.com/regions/hampton-roads/move-in-ready-homes',
            'https://hhhunthomes.com/regions/Raleigh/move-in-ready-homes']
data_list = []
for url in url_list:
    qmi_response = requests.get(url)
    qmi_soup = BeautifulSoup(qmi_response.text, 'html.parser')

    all_qmis = qmi_soup.select('div.qmi-card')
    for qmi in all_qmis:
        try:
            qmi_link = qmi.find('a')['href']
            qmi_mls_id = get_mls_id(f'https://hhhunthomes.com{qmi_link}')
            community_name = qmi.find('p', {'class': 'qmi-card__community'}).find('span').text
            qmi_img = qmi.find('div', {'class': 'framed-image-content'}).find('img')['src']
            qmi_address = qmi.find_all('address', {'class': 'qmi-card__address'})[0].text.rstrip()
            qmi_state = qmi.find_all('address', {'class': 'qmi-card__address'})[1].text.lstrip()
            all_features = qmi.find('div', {'class': 'qmi-card__features'}).find_all('span')
            qmi_beds = all_features[0].text.lstrip()
            qmi_baths = all_features[1].text.lstrip()
            qmi_sqft = int(all_features[2].text.replace(',', ''))
            qmi_car_garage = all_features[3].text
            qmi_price = int(qmi.find('span', {'class': 'qmi-card__price'}).text.split('$')[1].replace(',', ''))
            qmi_listing_type = 'For sale'
            if community_name in community_city:
                qmi_home_type = community_city[community_name][1]
            qmi_keywords = f'new home construction; new {qmi_home_type}s; houses for sale; new homes for sale; real estate'
            data = {
                'Listing ID': qmi_mls_id,
                'Listing Name': community_name,
                'Final URL': f'https://hhhunthomes.com{qmi_link}',
                'Image URL': qmi_img,
                'City name': qmi_state,
                'Description': f'{qmi_beds} beds, {qmi_baths} bath, {qmi_sqft}sqft',
                'Price': f'{qmi_price} USD',
                'Property type': qmi_home_type,
                'Listing type': qmi_listing_type,
                'Contextual keywords': qmi_keywords,
                'Address': f'{qmi_address}, {qmi_state}'
            }
            data_list.append(data)
        except TypeError as err:
            continue

pd.DataFrame(data_list).to_csv('qmis.csv', index=False)

