import pandas as pd
import numpy as nump
import requests
from time import sleep
from random import randint 
import json
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as bs
import re

def guidestar_ein_search(ein_num_list):
    cookies = {
        'ASP.NET_SessionId': 'mwugwf3lgpwjw3tebbyckzeu',
        '_vwo_uuid_v2': 'DE6A93A3901E730D3B03A7074EDF822CD|6395931c4bdf5ad30a1302a512d69ee9',
        '_gcl_au': '1.1.1224203376.1719248110',
        'ajs_anonymous_id': '14a25e10-005c-4a4b-8227-4f1d5239f70a',
        'ajs_user_id': '2034',
        '_ga': 'GA1.1.817022669.1719248110',
        'cb_user_id': 'null',
        'cb_group_id': 'null',
        'cb_anonymous_id': '%229de663e2-e416-43a6-89c3-1367f8e6efa2%22',
        'visitor_id934453': '361976509',
        'visitor_id934453-hash': '52ccff6edc57f29205274764fe4b36eb06ddb5b17b2c2a7c0a6630644df219e28c6efc7a9ce61c0834771c7f5057f3d852ad639f',
        '_hjSessionUser_2545182': 'eyJpZCI6ImZkNDZlZjQzLTI1ZTYtNTY0YS04Nzg5LWE1NGRlOTUwYjRjMCIsImNyZWF0ZWQiOjE3MTkyNDgxMTAyMzAsImV4aXN0aW5nIjp0cnVlfQ==',
        '_hjSession_2545182': 'eyJpZCI6ImViMDc3OWI5LTRhMjgtNDY2NS1hYWU3LWVlY2YwMDBiZTg3MyIsImMiOjE3MTkyNTE5MjQ0MjMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==',
        '__RequestVerificationToken': 'HsM_tUPCUXBAory3oWpesAXhU7A5UHFFCXYCO3A4nZdW8irrpY7NPiXjGTFQupuHJltuDw2',
        'OptanonConsent': 'isIABGlobal=false&datestamp=Mon+Jun+24+2024+14%3A45%3A17+GMT-0400+(Eastern+Daylight+Time)&version=6.5.0&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C101%3A1%2C102%3A1%2C103%3A1%2C104%3A1%2C105%3A1%2C106%3A1%2C107%3A1%2C108%3A1%2C109%3A1&AwaitingReconsent=false',
        '_ga_5W8PXYYGBX': 'GS1.1.1719251879.2.1.1719254717.16.0.0',
        'AWSALB': 'yVS5jVa2hhb1B9i7laX4ir1N7WL2BgVVdllkc6Q2Ss4m2OH9iRBY/x+uj8PYduXY4VrK9Eqdq2+fnmgb579F8IVVcnRzUtQ3qeZZwWNwf8NU1cRgsC/mVAIaOoC9',
        'AWSALBCORS': 'yVS5jVa2hhb1B9i7laX4ir1N7WL2BgVVdllkc6Q2Ss4m2OH9iRBY/x+uj8PYduXY4VrK9Eqdq2+fnmgb579F8IVVcnRzUtQ3qeZZwWNwf8NU1cRgsC/mVAIaOoC9',
    }
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'ASP.NET_SessionId=mwugwf3lgpwjw3tebbyckzeu; _vwo_uuid_v2=DE6A93A3901E730D3B03A7074EDF822CD|6395931c4bdf5ad30a1302a512d69ee9; _gcl_au=1.1.1224203376.1719248110; ajs_anonymous_id=14a25e10-005c-4a4b-8227-4f1d5239f70a; ajs_user_id=2034; _ga=GA1.1.817022669.1719248110; cb_user_id=null; cb_group_id=null; cb_anonymous_id=%229de663e2-e416-43a6-89c3-1367f8e6efa2%22; visitor_id934453=361976509; visitor_id934453-hash=52ccff6edc57f29205274764fe4b36eb06ddb5b17b2c2a7c0a6630644df219e28c6efc7a9ce61c0834771c7f5057f3d852ad639f; _hjSessionUser_2545182=eyJpZCI6ImZkNDZlZjQzLTI1ZTYtNTY0YS04Nzg5LWE1NGRlOTUwYjRjMCIsImNyZWF0ZWQiOjE3MTkyNDgxMTAyMzAsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_2545182=eyJpZCI6ImViMDc3OWI5LTRhMjgtNDY2NS1hYWU3LWVlY2YwMDBiZTg3MyIsImMiOjE3MTkyNTE5MjQ0MjMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==; __RequestVerificationToken=HsM_tUPCUXBAory3oWpesAXhU7A5UHFFCXYCO3A4nZdW8irrpY7NPiXjGTFQupuHJltuDw2; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jun+24+2024+14%3A45%3A17+GMT-0400+(Eastern+Daylight+Time)&version=6.5.0&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C101%3A1%2C102%3A1%2C103%3A1%2C104%3A1%2C105%3A1%2C106%3A1%2C107%3A1%2C108%3A1%2C109%3A1&AwaitingReconsent=false; _ga_5W8PXYYGBX=GS1.1.1719251879.2.1.1719254717.16.0.0; AWSALB=yVS5jVa2hhb1B9i7laX4ir1N7WL2BgVVdllkc6Q2Ss4m2OH9iRBY/x+uj8PYduXY4VrK9Eqdq2+fnmgb579F8IVVcnRzUtQ3qeZZwWNwf8NU1cRgsC/mVAIaOoC9; AWSALBCORS=yVS5jVa2hhb1B9i7laX4ir1N7WL2BgVVdllkc6Q2Ss4m2OH9iRBY/x+uj8PYduXY4VrK9Eqdq2+fnmgb579F8IVVcnRzUtQ3qeZZwWNwf8NU1cRgsC/mVAIaOoC9',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

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

    social_media_df = pd.DataFrame(social_media_rows, columns=['ein_num', 'mission_statement', 'facebook_link', 'twitter_link', 
                                            'youtube_link', 'instagram_link', 'linkedin_link'])
    
    return social_media_df

if __name__ == "__main__":
    ein_num_list = 'list_of_ein_number'