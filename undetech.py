import undetected_chromedriver as uc

def scrape_website(url):
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html
print(scrape_website("https://www.amazon.in/s?k=vivo+mobile+5g+phone"))