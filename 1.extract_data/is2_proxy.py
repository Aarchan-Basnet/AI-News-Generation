import requests
from selenium import webdriver
from lxml import html
from time import sleep
import concurrent.futures



def get_proxies(proxies_list):
    url = 'https://free-proxy-list.net'
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    sleep(2)
    html_content = driver.page_source
    sleep(2)
    driver.quit()

    tree = html.fromstring(html_content)

    data_rows = tree.xpath("//div[@class='table-responsive']//table//tbody/tr")
    # proxies_list = []
    for row in data_rows:
        try:
            ip = row.xpath("td[1]//text()")[0]
            port = row.xpath("td[2]//text()")[0]
            proxy = f"{ip}:{port}"
            proxies_list.append(proxy)
        except IndexError:
            pass

    return proxies_list

def get_proxies2(proxies_list):
    url = 'https://proxyscrape.com/free-proxy-list'
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    sleep(2)
    html_content = driver.page_source
    sleep(2)
    driver.quit()

    tree = html.fromstring(html_content)

    data_rows = tree.xpath("//div[@class='box']//table//tbody/tr")
    # proxies_list = []
    for row in data_rows:
        try:
            ip = row.xpath("td[2]//text()")[0]
            port = row.xpath("td[3]//text()")[0]
            proxy = f"{ip}:{port}"
            proxies_list.append(proxy)

        except IndexError:
            pass

    return proxies_list

def extract(proxy):
    try:
        url = "https://ekantipur.com"
        r = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=10)  # Increased timeout
        if r.status_code == 200:
            print(f"{proxy} is working")

            with open('proxy_demo.txt', 'a') as f:
                f.write(proxy + '\n')

        else:
            print(f"{proxy} returned status code {r.status_code}")
    except requests.RequestException as e:
        print(f"{proxy} Error: {e}")
    except requests.exceptions.ReadTimeout as e:
        print(f"{proxy} Read Timeout Error: {e}")

def main():
    print("Extracting proxies...")
    proxies_list = []
    proxylist1 = get_proxies(proxies_list)
    print(len(proxylist1))
    proxylist = get_proxies2(proxylist1)
    print(len(proxylist))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(extract, proxylist[:40])

if __name__ == "__main__":
    main()
