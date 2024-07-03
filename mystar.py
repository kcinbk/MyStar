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

browser_cookies = "# insert cookies "
request_headers = "# insert browser request headers"

# Return a list of nonprofit organizations, along with their EINs (employer identification numbers) and relevant information based on the search_query
def orgs_search(search_query, page_num, browser_cookies, request_headers):
    cookies = browser_cookies
    headers = request_headers
    
    result_list = []

    for current_page in tqdm(range(1, page_num), desc="Fetching pages"):
        sleep(randint(1,3))
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
            result_list.extend(data)
    print(f"Found {len(result_list)} organizations!")

    rows = []
    ein_num_list= []
    for org in result_list:
        org_name = org.get('OrgName', None)
        org_alt_name = org.get('AkaOrgName', None)
        ein_num =  org.get('Ein', None)
        org_highlight = org.get('HitHighlighting', None)
        city = org.get('City', None)
        state = org.get('State', None)
        assets = org.get('Assets', None)
        income = org.get('Income', None)
        ein_num_list.append(ein_num)
        rows.append((org_name, org_alt_name, ein_num, org_highlight, city, state, assets, income))
    
    df = pd.DataFrame(rows, columns =['org_name', 'org_alt_name', 'ein_num', 'org_highlight', 'city', 'state', 'assets', 'income'] )
    df = df.drop_duplicates(subset='ein_num')
    return  ein_num_list, df



def orgs_supplemental_info(ein_num_list, browser_cookies, request_headers):
    cookies = browser_cookies
    headers = request_headers

    social_media_rows = []

    for i, ein_num in enumerate(tqdm(ein_num_list, desc="Fetching mission statement, social media accounts")):
        sleep(randint(1, 3))
        response = requests.get(f'https://www.guidestar.org/profile/{ein_num}', cookies=cookies, headers=headers)
        if response.status_code != 200:
            continue
        else:
            data = bs(response.text, 'html.parser')
            mission_statement = data.select_one('p#mission-statement').get_text(strip=True)
            social_media_links = data.select('a.media-link')
            link_list = [link.get('href') for link in social_media_links]
        
            # Regex patterns for social media platforms
            twitter_pattern = r"^https?://(?:www\.)?twitter\.com/"
            facebook_pattern = r"^https?://(?:www\.)?facebook\.com/"
            instagram_pattern = r"^https?://(?:www\.)?instagram\.com/"
            youtube_pattern = r"^https?://(?:www\.)?youtube\.com/"
            linkedin_pattern = r"^https?://(?:www\.)?linkedin\.com/"
    
            facebook_link = None
            twitter_link = None
            instagram_link = None
            youtube_link = None
            linkedin_link = None
    
            for platform_url in link_list:
                if re.match(facebook_pattern, platform_url):
                    facebook_link = platform_url
                elif re.match(twitter_pattern, platform_url):
                    twitter_link = platform_url
                elif re.match(linkedin_pattern, platform_url):
                    linkedin_link = platform_url
                elif re.match(youtube_pattern, platform_url):
                    youtube_link = platform_url
                elif re.match(instagram_pattern, platform_url):
                    instagram_link = platform_url
            
            social_media_rows.append((ein_num, mission_statement, facebook_link, twitter_link, youtube_link, instagram_link, linkedin_link))

    df = pd.DataFrame(social_media_rows, columns=['ein_num', 'mission_statement', 'facebook_link', 'twitter_link', 
                                            'youtube_link', 'instagram_link', 'linkedin_link'])
    return df

def find_mystar(search_query, page_num, browser_cookies, request_headers):
    ein_num_list, main_df = orgs_search(search_query, page_num, browser_cookies, request_headers)
    supplement_df = orgs_supplemental_info(ein_num_list, browser_cookies, request_headers)
    df = pd.merge(main_df, supplement_df, left_on='ein_num', right_on='ein_num')
    return df

    if __name__ == "__main__":
        df = find_mystar(search_query, page_num, browser_cookies, request_headers)

    