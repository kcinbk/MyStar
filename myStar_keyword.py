import numpy as nump
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
from time import sleep
from random import randint
import json
from tqdm import tqdm
import re

def guidestar_keyword_search(search_query, initialPage, lastPage, folder_path):
    cookies = {
        'ASP.NET_SessionId': 'mwugwf3lgpwjw3tebbyckzeu',
        '_vwo_uuid_v2': 'DE6A93A3901E730D3B03A7074EDF822CD|6395931c4bdf5ad30a1302a512d69ee9',
        '_gcl_au': '1.1.1224203376.1719248110',
        'ajs_anonymous_id': '14a25e10-005c-4a4b-8227-4f1d5239f70a',
        'ajs_user_id': '2034',
        '_ga': 'GA1.1.817022669.1719248110',
        '_hjSession_2545182': 'eyJpZCI6ImIxNzdmMTEyLTY0OGQtNDBmNC1iOWUzLTg1NWQxMzViN2NhNyIsImMiOjE3MTkyNDgxMTAyMzAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxfQ==',
        'cb_user_id': 'null',
        'cb_group_id': 'null',
        'cb_anonymous_id': '%229de663e2-e416-43a6-89c3-1367f8e6efa2%22',
        'visitor_id934453': '361976509',
        'visitor_id934453-hash': '52ccff6edc57f29205274764fe4b36eb06ddb5b17b2c2a7c0a6630644df219e28c6efc7a9ce61c0834771c7f5057f3d852ad639f',
        'OptanonConsent': 'isIABGlobal=false&datestamp=Mon+Jun+24+2024+13%3A00%3A02+GMT-0400+(Eastern+Daylight+Time)&version=6.5.0&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C101%3A1%2C102%3A1%2C103%3A1%2C104%3A1%2C105%3A1%2C106%3A1%2C107%3A1%2C108%3A1%2C109%3A1&AwaitingReconsent=false',
        '_hjSessionUser_2545182': 'eyJpZCI6ImZkNDZlZjQzLTI1ZTYtNTY0YS04Nzg5LWE1NGRlOTUwYjRjMCIsImNyZWF0ZWQiOjE3MTkyNDgxMTAyMzAsImV4aXN0aW5nIjp0cnVlfQ==',
        'AWSALB': 'lw2+lZt8X1HtdMn7v8Zqy1oay/K+fg5lL2fs6Pg4SocCRiPi9pOBgHvCODWBm1FwHSa4+sklhniIJ9kfYjSB7uHY0zXuku/l621AF/v4BjuDoW88Rhzi5gnl2ejO',
        'AWSALBCORS': 'lw2+lZt8X1HtdMn7v8Zqy1oay/K+fg5lL2fs6Pg4SocCRiPi9pOBgHvCODWBm1FwHSa4+sklhniIJ9kfYjSB7uHY0zXuku/l621AF/v4BjuDoW88Rhzi5gnl2ejO',
        '_ga_5W8PXYYGBX': 'GS1.1.1719248110.1.1.1719248403.58.0.0',
    }
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'ASP.NET_SessionId=mwugwf3lgpwjw3tebbyckzeu; _vwo_uuid_v2=DE6A93A3901E730D3B03A7074EDF822CD|6395931c4bdf5ad30a1302a512d69ee9; _gcl_au=1.1.1224203376.1719248110; ajs_anonymous_id=14a25e10-005c-4a4b-8227-4f1d5239f70a; ajs_user_id=2034; _ga=GA1.1.817022669.1719248110; _hjSession_2545182=eyJpZCI6ImIxNzdmMTEyLTY0OGQtNDBmNC1iOWUzLTg1NWQxMzViN2NhNyIsImMiOjE3MTkyNDgxMTAyMzAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxfQ==; cb_user_id=null; cb_group_id=null; cb_anonymous_id=%229de663e2-e416-43a6-89c3-1367f8e6efa2%22; visitor_id934453=361976509; visitor_id934453-hash=52ccff6edc57f29205274764fe4b36eb06ddb5b17b2c2a7c0a6630644df219e28c6efc7a9ce61c0834771c7f5057f3d852ad639f; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jun+24+2024+13%3A00%3A02+GMT-0400+(Eastern+Daylight+Time)&version=6.5.0&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C101%3A1%2C102%3A1%2C103%3A1%2C104%3A1%2C105%3A1%2C106%3A1%2C107%3A1%2C108%3A1%2C109%3A1&AwaitingReconsent=false; _hjSessionUser_2545182=eyJpZCI6ImZkNDZlZjQzLTI1ZTYtNTY0YS04Nzg5LWE1NGRlOTUwYjRjMCIsImNyZWF0ZWQiOjE3MTkyNDgxMTAyMzAsImV4aXN0aW5nIjp0cnVlfQ==; AWSALB=lw2+lZt8X1HtdMn7v8Zqy1oay/K+fg5lL2fs6Pg4SocCRiPi9pOBgHvCODWBm1FwHSa4+sklhniIJ9kfYjSB7uHY0zXuku/l621AF/v4BjuDoW88Rhzi5gnl2ejO; AWSALBCORS=lw2+lZt8X1HtdMn7v8Zqy1oay/K+fg5lL2fs6Pg4SocCRiPi9pOBgHvCODWBm1FwHSa4+sklhniIJ9kfYjSB7uHY0zXuku/l621AF/v4BjuDoW88Rhzi5gnl2ejO; _ga_5W8PXYYGBX=GS1.1.1719248110.1.1.1719248403.58.0.0',
        'dnt': '1',
        'origin': 'https://www.guidestar.org',
        'priority': 'u=1, i',
        'referer': 'https://www.guidestar.org/search',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    result_list = []

    for current_page in tqdm(range(initialPage, lastPage), desc="Fetching pages"):
        sleep(randint(1, 3))
        data = {
            'CurrentPage': f"{current_page}",
            'SearchType': 'org',
            'GroupExemption': '',
            'AffiliateOrgName': '',
            'RelatedOrgName': '',
            'RelatedOrgEin': '',
            'RelationType': '',
            'RelatedOrgs': '',
            'SelectedCityNav[]': '',
            'SelectedCountyNav[]': '',
            'Eins': '',
            'ul': '',
            'PCSSubjectCodes[]': '',
            'PeoplePCSSubjectCodes[]': '',
            'PCSPopulationCodes[]': '',
            'AutoSelectTaxonomyFacet': '',
            'AutoSelectTaxonomyText': '',
            'Keywords': f'{search_query}',
            'City': '',
            'PeopleZip': '',
            'PeopleZipRadius': 'Zip Only',
            'PeopleCity': '',
            'PeopleRevenueRangeLow': '$0',
            'PeopleRevenueRangeHigh': 'max',
            'PeopleAssetsRangeLow': '$0',
            'PeopleAssetsRangeHigh': 'max',
            'Sort': '',
        }
        
        response = requests.post('https://www.guidestar.org/search/SubmitSearch', 
                                 cookies=cookies, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code != 200:
            print(f'An error has occured on page {current_page}')
            continue
        else:
            data = response.json()['Hits']
            # file_path = f"{folder_path} {search_query}_{current_page}.json"
            # with open(file_path, 'w') as file:
                # json.dump(data, file, indent = 4)
            result_list.extend(data)
            
        
    print(f"All {lastPage+1-initialPage} pages have been completed!")

    rows = []

    for org in result_list:
        org_name = org.get('OrgName', None)
        org_alt_name = org.get('AkaOrgName', None)
        ein_num =  org.get('Ein', None)
        bio = org.get('HitHighlighting', None)
        city = org.get('City', None)
        state = org.get('State', None)
        assets = org.get('Assets', None)
        income = org.get('Income', None)
    
        rows.append((org_name, org_alt_name, ein_num, bio, city, state, assets, income))
    
    df = pd.DataFrame(rows, columns =['org_name', 'org_alt_name', 'ein_num', 'bio', 'city', 'state', 'assets', 'income'] )
    df = df.drop_duplicates(subset='ein_num')
    
    return df
    # return result_list

if __name__ == "__main__":
    search_query = "your_query_here"
    initialPage = 'starting_page'
    lastPage = 'endin_page'
    folder_path = "/path/to/your/folder/"
