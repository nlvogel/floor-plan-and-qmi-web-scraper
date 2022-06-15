from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_mls_id(url):
    '''
    defines a function that gets the MLS number from a deeper page than what the rest of the code handles.\n
    returns mls number as text
    '''
    mls_response = requests.get(url)
    mls_soup = BeautifulSoup(mls_response.text, 'html.parser')
    mls_text = mls_soup.find('span', {'class': 'community__mls-number'}).text.split('MLS#')[1].split('\n')[1].lstrip()
    if ' | ' in mls_text:
        altered = mls_text.split(' | ')[0]
        return altered
    return mls_text

# lower() is used to make sure the community name matches, converted to title case later
community_city = {
    'Central Crossing'.lower(): ('Aylett, VA', 'Single-family Home'),
    'FoxCreek Homestead'.lower(): ('Moseley, VA', 'Single-family Home'),
    'Giles - The Cove'.lower(): ('Mechanicsville, VA', 'Single-family Home'),
    'Giles - Townhomes'.lower(): ('Mechanicsville, VA', 'Townhome'),
    'Governor\'s Retreat'.lower(): ('Richmond, VA', 'Single-family Home'),
    'Magnolia Green Single Family'.lower(): ('Moseley, VA', 'Single-family Home'),
    'Magnolia Green Townhomes'.lower(): ('Moseley, VA', 'Townhome'),
    'Maidstone Village Townhomes'.lower(): ('New Kent, VA', 'Townhome'),
    'Meadowville Landing - Twin Rivers'.lower(): ('Chester, VA', 'Single-family Home'),
    'Mosaic at West Creek'.lower(): ('Richmond, VA', 'Townhome'),
    'The Pointe at Twin Hickory'.lower(): ('Short Pump, VA', 'Condominium'),
    'River Mill Townhomes'.lower(): ('Glen Allen, VA', 'Townhome'),
    'Rutland Grove'.lower(): ('Mechanicsville, VA', 'Single-family Home'),
    'Sandler Station'.lower(): ('North Chesterfield, VA', 'Condominium'),
    'wescott'.lower(): ('Midlothian, VA', 'Townhome'),
    'Wescott Condos'.lower(): ('Midlothian, VA', 'Condominium'),
    'Taylor Farm'.lower(): ('Mechanicsville, VA', 'Single-family Home'),
    'Quarterpath at Williamsburg Condos'.lower(): ('Williamsburg, VA', 'Condominium'),
    'Meadows Landing'.lower(): ('Suffolk, VA', 'Single-family Home'),
    'River Highlands'.lower(): ('Suffolk, VA', 'Single-family Home'),
    'Banks Pointe'.lower(): ('Raleigh, NC', 'Single-family Home'),
    'Dayton Woods'.lower(): ('Raleigh, NC', 'Single-family Home'),
    'Enclave at Leesville'.lower(): ('Durham, NC', 'Single-family Home'),
    'Granite Falls Estates'.lower(): ('Rolesville, NC', 'Single-family Home'),
    'The Reserve at Wackena'.lower(): ('Cary, NC', 'Single-family Home')
}

# includes a list of all the move-in ready home pages for processing
url_list = ['https://hhhunthomes.com/regions/richmond/move-in-ready-homes',
            'https://hhhunthomes.com/regions/williamsburg/move-in-ready-homes',
            'https://hhhunthomes.com/regions/hampton-roads/move-in-ready-homes',
            'https://hhhunthomes.com/regions/Raleigh/move-in-ready-homes']
data_list = []  # empty list for data storage for later processing
for url in url_list:
    qmi_response = requests.get(url)
    qmi_soup = BeautifulSoup(qmi_response.text, 'html.parser')

    all_qmis = qmi_soup.select('div.qmi-card')  # gets all the QMIs on each page
    for qmi in all_qmis:  # a loop through all active QMIs
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
            qmi_price = int(qmi.find('span', {'class': 'qmi-card__price'}).text.split('$')[1].replace(',', ''))
            qmi_listing_type = 'For sale'
            if community_name.lower() in community_city:
                qmi_home_type = community_city[community_name.lower()][1].lower()
            qmi_keywords = f'new home construction; new {qmi_home_type}s; houses for sale; new homes for sale; real estate; {community_name}'
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

# sorts all the data above into different lists based on location, then sends each list to a different CSV
richmond_list = [item for item in data_list if 'richmond' in item['Final URL'] or 'new-kent' in item['Final URL']]
print('Richmond sorted.')
pd.DataFrame(richmond_list).to_csv('qmi/richmond-qmi.csv', index=False)
print('Richmond CSV done.')

hampton_roads_list = [item for item in data_list if 'hampton-roads' in item['Final URL']]
print('Hampton Roads sorted.')
pd.DataFrame(hampton_roads_list).to_csv('qmi/hampton-roads-qmi.csv', index=False)
print('Hampton Roads CSV done.')

williamsburg_list = [item for item in data_list if 'williamsburg' in item['Final URL']]
print('Williamsburg sorted.')
pd.DataFrame(williamsburg_list).to_csv('qmi/williamsburg-qmi.csv', index=False)
print('Williamsburg CSV done.')

raleigh_list = [item for item in data_list if 'raleigh' in item['Final URL']]
print('Raleigh sorted.')
pd.DataFrame(raleigh_list).to_csv('qmi/raleigh-qmi.csv', index=False)
print('Raleigh CSV done.')