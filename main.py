from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

# Set up Selenium with Chrome WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
service = Service('chromedriver-mac-arm64/chromedriver')  # Update with your chromedriver path
driver = webdriver.Chrome(service=service, options=chrome_options)

def sign_in():
    url = "https://taco.ith.sinica.edu.tw/tdk/index.php?title=特殊:用戶登錄"
    driver.get(url)

    profile = {
        'username': 'NM6121030',
        'password': 'ncku2024'
    }

    # Wait for the dynamic content to load
    time.sleep(2)  # Adjust the sleep time as needed

    # Find the username and password fields and enter the credentials
    username = driver.find_element(By.ID, "wpName1")
    username.send_keys(f"{profile['username']}")
    password = driver.find_element(By.ID, "wpPassword1")
    password.send_keys(f"{profile['password']}")

    # Find the login button and click it
    login_button = driver.find_element(By.ID, "wpLoginAttempt")
    login_button.click()

    # Wait for the dynamic content to load
    time.sleep(2)  # Adjust the sleep time as needed

def make_dir(ouput_dir):
    if not os.path.exists(f"{ouput_dir}"):
        os.makedirs(f"{ouput_dir}")

def crawl_by_year(url: str):
    driver.get(url)

    # Wait for the dynamic content to load
    time.sleep(2)  # Adjust the sleep time as needed

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # print(soup.prettify())

    month_container = soup.find('div', id='mw-content-text')

    month_links = []
    month_links = month_container.find_all('li')
    month_links = [link.find('a')['href'] for link in month_links]

    for link in month_links:
        base_url = "https://taco.ith.sinica.edu.tw"
        crawl_by_month(base_url + link)
        time.sleep(2)  # Adjust the sleep time as needed

def crawl_by_month(url: str):
    driver.get(url)

    # Wait for the dynamic content to load
    time.sleep(2)  # Adjust the sleep time as needed

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    day_container = soup.find('div', id="mw-content-text")

    day_links = []
    day_links = day_container.find_all('li')
    day_links = [link.find('a')['href'] for link in day_links]

    for link in day_links:
        base_url = "https://taco.ith.sinica.edu.tw"
        crawl_by_entry(base_url + link)
        time.sleep(2)

def crawl_by_entry(url: str):
    print(f"Crawling {url}")
    driver.get(url)

    # Wait for the dynamic content to load
    time.sleep(2)  # Adjust the sleep time as needed

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    date = soup.find('h1', id='firstHeading').text.split('/')[1]  # 吳新榮日記/1933-09-04
    date_month_day_notes = soup.find_all('span', class_='mw-headline')  # [癸酉年（昭和八年，一九三三年）, 九月四日, 註解]
    chinese_date, chinese_month_day, notes = date_month_day_notes[0].text, date_month_day_notes[1].text, date_month_day_notes[2].text
    content_body = soup.find('td', class_='itharticle')
    contents = content_body.find_all('p')
    cites = soup.find_all('span', class_='reference-text')
    has_img = True if content_body.find_all('img') else False

    generate_file(url, f"{date}.md", date, chinese_date, chinese_month_day, contents, has_img, cites)

def generate_file(source_url: str, file_name: str, date: str, chinese_date: str, chinese_month_day: str, contents: str, has_img: bool, cites: list):
    attributes = {
        "作者": "\"[[吳新榮]]\"",
        "日記出處": source_url,
        "發生日期": date,
        "天氣": "",
        "建檔人": "",
    }
    year = date.split('-')[0]
    file_name = f"{year}/{file_name}"
    make_dir(year)
    print(f"generate file: {file_name}")
    
    with open(file_name, 'w') as f:
        f.write(f"---\n")
        for key, value in attributes.items():
            f.write(f"{key}: {value}\n")
        f.write(f"---\n\n")
        f.write(f"# 日期\n")
        f.write(f"{date.strip()}\n\n")
        f.write(f"# 中文日期\n")
        f.write(f"{chinese_date.strip()}\n")
        f.write(f"{chinese_month_day.strip()}\n\n")
        f.write(f"# 日記內容\n")
        for content in contents:
            f.write(f"{content.text}\n")
        if has_img:
            f.write(f"!!!!!本文出現圖片，請自行到該網站上抓取!!!!!\n\n")
        f.write(f"# 註解\n")
        for i, cite in enumerate(cites):
            f.write(f"{i+1}. {cite.text}\n")

if __name__ == "__main__":
    # url can be found at here: https://taco.ith.sinica.edu.tw/tdk/%E5%90%B3%E6%96%B0%E6%A6%AE%E6%97%A5%E8%A8%98
    url_to_crawl = "https://taco.ith.sinica.edu.tw/tdk/%E5%90%B3%E6%96%B0%E6%A6%AE%E6%97%A5%E8%A8%98/%E4%B9%99%E4%BA%A5%E5%B9%B4%EF%BC%88%E6%98%AD%E5%92%8C%E5%8D%81%E5%B9%B4%EF%BC%8C%E4%B8%80%E4%B9%9D%E4%B8%89%E4%BA%94%E5%B9%B4%EF%BC%89"

    sign_in()
    crawl_by_year(url=url_to_crawl)

    # debug use
    # crawl_by_entry("https://taco.ith.sinica.edu.tw/tdk/%E5%90%B3%E6%96%B0%E6%A6%AE%E6%97%A5%E8%A8%98/1933-09-14")
    # crawl_by_entry("https://taco.ith.sinica.edu.tw/tdk/%E5%90%B3%E6%96%B0%E6%A6%AE%E6%97%A5%E8%A8%98/1933-09-04")
    # crawl_by_entry("https://taco.ith.sinica.edu.tw/tdk/%E5%90%B3%E6%96%B0%E6%A6%AE%E6%97%A5%E8%A8%98/1933-09-10")
