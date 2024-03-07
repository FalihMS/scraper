import nest_asyncio
import time
import asyncio
from playwright.async_api import async_playwright
import random
from bs4 import BeautifulSoup 
import csv 
import pandas as pd
from datetime import datetime

async def scrape_mutual_fund():
    async with async_playwright() as p:
        html_pages = []
        
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto('https://www.pasardana.id/fund/search')
        time.sleep(random.randint(2, 5))
        
        list = page.locator("xpath=//ul[contains(@class,'pagination')]/li")
        print(await list.count())
        html_pages.append(await page.content())
        
        for x in range(await list.count()):
            await list.nth(x).locator("xpath=//a").click()
            time.sleep(random.randint(3, 7))
            html_pages.append(await page.content())
            
        await browser.close()

        return html_pages

def convert_bs4(page, html_item):
    return BeautifulSoup(html_item[page], "html.parser")

def get_data(soup):
    return soup.find_all("tr", {"class": "ng-scope"})

def get_df(list):
    df = []
    quote = {}
    
    for row in list:
        data = row.find_all("td")
        
        # Data Perusahaan
        quote['NAME'] = data[2].text.strip()
        quote['IM'] = data[4].text.strip() 
        quote['CB'] = data[5].text.strip()  
        quote['TYPE'] = data[6].text.strip()   
        quote['CAT'] = data[7].text.strip()
        quote['CURR'] = data[8].text.strip()
        quote['NAV/UNIT'] = data[10].text.strip()
        quote['AUM'] = data[64].text.strip()
        quote['LAST_UPDATE'] = data[72].text.strip()
    
        df.append(quote)
        quote = {}

    return df



def main():
    html = asyncio.run(scrape_mutual_fund())
    for x in range(len(html)):
        if x > 0:
            print("processing page", x)
            page = convert_bs4(x, html)
            df = get_df(get_data(page))
            pd.DataFrame.from_dict(df).to_csv("result/mutual-funds-{date}-{page}.csv".format(date=datetime.today().strftime('%Y-%m-%d'), page=x))

if __name__ == "__main__":
    main()