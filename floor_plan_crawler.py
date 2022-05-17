from bs4 import BeautifulSoup
import requests
import pandas as pd

sitemaps = "https://hhhunthomes.com/sitemap.xml"
response = requests.get(sitemaps)
contents = response.text
# initialize soup using an xml interpreter, doesn't work with html.parser
soup = BeautifulSoup(contents, features="xml")
url_list = []
# get all urls
for url in soup.find_all(name="loc"):
    if "floorplan" in url.text or "floorplans" in url.text:
        url_list.append(url.text)
print('Received URLs')
# filters out all response == 404 and blog posts
not_404 = []
for url in url_list:
    try:
        if requests.get(url).status_code != 404 or 'blog' not in url:
            not_404.append(url)
    except requests.exceptions.TooManyRedirects:
        continue
print('URLs filtered')
# dictionary describing the city and home type because this isn't included anywhere
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
print('Location dictionary read.')
data_list = []
# loop to check each page and get information from them
for link in not_404:
    try:
        floor_plan_url = link
        floor_plan_response = requests.get(floor_plan_url)
        # initialize soup now using html.parser because we're investigating an html page
        floor_plan_soup = BeautifulSoup(floor_plan_response.text, "html.parser")
        description = floor_plan_soup.select('ul.qmi-detail__features-list li')
        beds = description[0].text
        baths = description[1].text
        try:
            # had to separate out communities with 'at' in the name
            if 'mosaic' in link:
                data = {
                    'Listing Name': 'The ' + floor_plan_soup.h1.text.split("\n")[1],
                    'Final URL': floor_plan_url,
                    'Image URL': floor_plan_soup.find('div', {'class': 'framed-image-content'}).find('img')['src'],
                    'City name': community_city['Mosaic at West Creek'][0],
                    'Property type': community_city['Mosaic at West Creek'][1],
                    'Listing type': 'For sale',
                    'Price': floor_plan_soup.find('div', {'class': 'qmi-detail__price-list'}).find('p').text.split('\n')[1].split(' ')[-1].split('$')[1] + ' USD',
                    'Description': f'{beds} beds,{baths} baths',
                    'Contextual keywords': f'new home construction; new {community_city["Mosaic at West Creek"][1]}s; '
                                           f'houses for sale; new homes for sale; real estate; Mosaic; '
                                           f'Mosaic at West Creek; hhhunt homes'
                }
                data_list.append(data)
            elif 'twin-hickory' in link:
                data = {
                    'Listing Name': 'The ' + floor_plan_soup.h1.text.split("\n")[1],
                    'Final URL': floor_plan_url,
                    'Image URL': floor_plan_soup.find('div', {'class': 'framed-image-content'}).find('img')['src'],
                    'City name': community_city['The Pointe at Twin Hickory'][0],
                    'Property type': community_city['The Pointe at Twin Hickory'][1],
                    'Listing type': 'For sale',
                    'Price':
                        floor_plan_soup.find('div', {'class': 'qmi-detail__price-list'}).find('p').text.split('\n')[1].split(' ')[
                            -1].split('$')[1] + ' USD',
                    'Description': f'{beds} beds,{baths} baths',
                    'Contextual keywords': f'new home construction; '
                                           f'new {community_city["The Pointe at Twin Hickory"][1]}s; houses for sale; '
                                           f'new homes for sale; real estate; Twin Hickory; '
                                           f'The Pointe at Twin Hickory; hhhunt homes'
                }
                data_list.append(data)
            elif 'quarterpath' in link:
                data = {
                    'Listing Name': 'The ' + floor_plan_soup.h1.text.split("\n")[1],
                    'Final URL': floor_plan_url,
                    'Image URL': floor_plan_soup.find('div', {'class': 'framed-image-content'}).find('img')['src'],
                    'City name': community_city['Quarterpath at Williamsburg Condos'][0],
                    'Property type': community_city['Quarterpath at Williamsburg Condos'][1],
                    'Listing type': 'For sale',
                    'Price':
                        floor_plan_soup.find('div', {'class': 'qmi-detail__price-list'}).find('p').text.split('\n')[1].split(' ')[
                            -1].split('$')[1] + ' USD',
                    'Description': f'{beds} beds,{baths} baths',
                    'Contextual keywords': f'new home construction; new '
                                           f'{community_city["Quarterpath at Williamsburg Condos"][1]}s; '
                                           f'houses for sale; new homes for sale; real estate; Quarterpath;'
                                           f'Quarterpath at Williamsburg; hhhunt homes'
                }
                data_list.append(data)
            elif 'enclave' in link:
                data = {
                    'Listing Name': 'The ' + floor_plan_soup.h1.text.split("\n")[1],
                    'Final URL': floor_plan_url,
                    'Image URL': floor_plan_soup.find('div', {'class': 'framed-image-content'}).find('img')['src'],
                    'City name': community_city['Enclave at Leesville'][0],
                    'Property type': community_city['Enclave at Leesville'][1],
                    'Listing type': 'For sale',
                    'Price':
                        floor_plan_soup.find('div', {'class': 'qmi-detail__price-list'}).find('p').text.split('\n')[1].split(' ')[
                            -1].split('$')[1] + ' USD',
                    'Description': f'{beds} beds,{baths} baths',
                    'Contextual keywords': f'new home construction; new '
                                           f'{community_city["Enclave at Leesville"][1]}s; '
                                           f'houses for sale; new homes for sale; real estate; enclave; '
                                           f'enclave at leesville; hhhunt homes'

                }
                data_list.append(data)
            elif 'wackena' in link:
                data = {
                    'Listing Name': 'The ' + floor_plan_soup.h1.text.split("\n")[1],
                    'Final URL': floor_plan_url,
                    'Image URL': floor_plan_soup.find('div', {'class': 'framed-image-content'}).find('img')['src'],
                    'City name': community_city['The Reserve at Wackena'][0],
                    'Property type': community_city['The Reserve at Wackena'][1],
                    'Listing type': 'For sale',
                    'Price':
                        floor_plan_soup.find('div', {'class': 'qmi-detail__price-list'}).find('p').text.split('\n')[1].split(' ')[
                            -1].split('$')[1] + ' USD',
                    'Description': f'{beds} beds,{baths} baths',
                    'Contextual keywords': f'new home construction; new '
                                           f'{community_city["The Reserve at Wackena"][1]}s; '
                                           f'houses for sale; new homes for sale; real estate; hhhunt homes'
                }
                data_list.append(data)
            else:
                data = {
                    'Listing Name': 'The ' + floor_plan_soup.h1.text.split("\n")[1],
                    'Final URL': floor_plan_url,
                    'Image URL': floor_plan_soup.find('div', {'class': 'framed-image-content'}).find('img')['src'],
                    'City name': community_city[floor_plan_soup.h1.text.split("\n")[2].split('at ')[1]][0],
                    'Property type': community_city.get(floor_plan_soup.h1.text.split("\n")[2].split('at ')[1])[1],
                    'Listing type': 'For sale',
                    'Price':
                        floor_plan_soup.find('div', {'class': 'qmi-detail__price-list'}).find('p').text.split('\n')[1].split(
                            ' ')[-1].split('$')[1] + ' USD',
                    'Description': f'{beds} beds,{baths} baths',
                    'Contextual keywords': 'new home construction; new ' +
                                           community_city.get(floor_plan_soup.h1.text.split("\n")[2].split('at ')[1])[1]
                                           + 's; houses for sale; new homes for sale; real estate; hhhunt homes;' +
                                           floor_plan_soup.h1.text.split("\n")[2].replace('at ', '')
                }
                data_list.append(data)
        except KeyError as key_err:
            print(link, key_err)
            continue
        except IndexError as in_err:
            print(link, in_err)
            continue
        except AttributeError as attr_err:
            print(link, attr_err)
            continue
    except IndexError as err:
        print(link, err)
        continue
print('URLs processed.')

richmond_list = [item for item in data_list if 'richmond' in item['Final URL']]
print('Richmond sorted.')
pd.DataFrame(richmond_list).to_csv('richmond-floor-plans.csv', index=False)
print('Richmond CSV done.')

hampton_roads_list = [item for item in data_list if 'hampton-roads' in item['Final URL']]
print('Hampton Roads sorted.')
pd.DataFrame(hampton_roads_list).to_csv('hampton-roads-floor-plans.csv', index=False)
print('Hampton Roads CSV done.')

williamsburg_list = [item for item in data_list if 'williamsburg' in item['Final URL']]
print('Williamsburg sorted.')
pd.DataFrame(williamsburg_list).to_csv('williamsburg-floor-plans.csv', index=False)
print('Williamsburg CSV done.')

raleigh_list = [item for item in data_list if 'raleigh' in item['Final URL']]
print('Raleigh sorted.')
pd.DataFrame(raleigh_list).to_csv('raleigh-floor-plans.csv', index=False)
print('Raleigh CSV done.')

print('Script done.')

