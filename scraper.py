from bs4 import BeautifulSoup
import os
import re
import undetected_chromedriver as uc
"""from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from sentence_transformers import SentenceTransformer, util"""
import torch
torch.classes.__path__ = []
AUTH = ''
SBR_WEBDRIVER = f''

"""def scrape_website(website):
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)

    return html"""
import undetected_chromedriver as uc
def scrape_website_undetect(url):
    print("----------------scrapet_web start")
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)
    driver = uc.Chrome(options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    print("-------------------scrapet_web end")
    return html


def extract_body_content(html_content):
    print("---------------------extract content started")
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        print("---------------------extract content started")
        return str(body_content)
    return ""


def clean_body_content(body_content):
    print("-----------------------cleaning started")
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    print("-----------------------cleaning ended")
    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    print("----------------spliting started")
    chunks = [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
    print(f"Split into {len(chunks)} chunks")
    print("----------------spliting ended")
    return chunks
