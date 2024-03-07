import nest_asyncio
import time
import asyncio
from playwright.async_api import async_playwright
import random
from bs4 import BeautifulSoup 
import csv 
import pandas as pd

nest_asyncio.apply()


async def scrape_ip():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
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
    ip_list = []
    for row in ip_address:
        if(len(row.find_all("td")) > 0):
            ip = {}
            ip["address"] = row.find_all("td")[0].text + ":" + row.find_all("td")[1].text
            ip["code"] = row.find_all("td")[2].text
            if(ip["code"] == "ID"):
                # print(ip)
                ip_list.append(ip)

    return ip_list
            
async def check_ip(filtered_ip_list):
    async with async_playwright() as p:
        html_pages = []
        for ip in filtered_ip_list:
            try:
                browser = await p.chromium.launch(
                    proxy={
                       'server': ip["address"],
                    },
                )
                page = await browser.new_page()
                
                await page.goto("https://httpbin.org/ip")
                html_content = await page.content()
                
                print(ip["address"], "Connection Success")
                return ip

            except:
              print(ip["address"], "Connection Error")
    
            await browser.close()

def get_proxy():
    html_proxies = asyncio.run(scrape_ip())
    ip_address = get_list(html_proxies)
    return iterate_list(ip_address)

    # return asyncio.run(check_ip(filtered_ip_list))
