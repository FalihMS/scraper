import nest_asyncio
import time
import asyncio
from playwright.async_api import async_playwright
import random
from bs4 import BeautifulSoup 
import csv 
import pandas as pd

nest_asyncio.apply()


async def main():
    async with async_playwright() as p:
        async def print_response(response):
            if("userApi/v4/tags/list" in response.url): 
                print(await response.json()) 

        html_pages = []
        
        browser = await p.chromium.launch(
            headless=False
        )
        page = await browser.new_page()
        
        page.on("response", lambda response: print_response(response))
        await page.goto("https://free-proxy-list.net")

        time.sleep(random.randint(2, 5))
        html_content = await page.content()
        
        await browser.close()

        return html_content

def get_list(html_proxies):
    soup = BeautifulSoup(html_proxies, "html.parser")
    table = soup.find("table", {"class": "table table-striped table-bordered"})
    return table.find_all("tr")

def iterate_list(ip_address):
    # ip_list = []
    for row in ip_address:
        ip_list = []
        if(len(row.find_all("td")) > 0):
            ip = {}
            ip["address"] = row.find_all("td")[0].text + ":" + row.find_all("td")[1].text
            ip["code"] = row.find_all("td")[2].text
            print(ip)
            ip_list.append(ip)

if __name__ == "__main__":
    html_proxies = asyncio.run(main())
    ip_address = get_list(html_proxies)
    iterate_list(ip_address)