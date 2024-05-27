import requests
from lxml import html
import json
import concurrent.futures
from itertools import cycle
from time import sleep
import os

current_dir = os.getcwd()
new_dir = os.path.join(current_dir, 'images_demo')
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

# Load proxies from proxy.txt file
with open("proxy_demo.txt", "r") as proxy_file:
    proxy_list = [line.strip() for line in proxy_file]

# Combine HTTP and HTTPS proxies
proxies = cycle(['http://' + proxy for proxy in proxy_list] + ['https://' + proxy for proxy in proxy_list])

data_list = []

# Function to download image
def download_image(url, name):
    save_as = f"images_demo/{name}.jpg"
    response = requests.get(url)
    sleep(2)
    with open(save_as, 'wb') as file:
        file.write(response.content)

def extract_data(url):
    # Select proxy from the cyclic generator
    proxy = next(proxies)
    retries = len(proxy_list)  # Number of retries equals the number of proxies

    for _ in range(retries):
        try:
            r = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=10)
            r.raise_for_status()
            html_content = r.content

            content = html.fromstring(html_content)

            title_element = content.xpath("//main//div[@class='container']//div[@class='row']//h1//text()")
            title = title_element[0] if title_element else None

            article_element = content.xpath("//main//div[@class='page-detail--content clearfix']//section//p//text()")
            article = ' '.join(article_element) if article_element else None

            image_url_element = content.xpath("//main//div[@class='container']//div[@class='col-sm-8']/img")
            try:
                image_url = image_url_element[0].attrib.get('data-src')
            except:
                image_url = None

            print("Image URL:", image_url)  # Add this line for debugging

            data_dict = {
                'title': title,
                'article': article,
                'image_url': image_url
            }

            return data_dict


        except (requests.exceptions.ProxyError, requests.exceptions.RequestException) as e:
            print(f"Error occurred while extracting data from {url} using proxy {proxy}: {e}")
            if proxy == proxy_list[-1]:  # If this is the last proxy in the list
                print("Error occurred for all proxies. Stopping retries.")
                break
            else:
                proxy = next(proxies)  # Move to the next proxy and retry

    print(f"All retries failed for URL: {url}")
    return None


def process_link(category, link):
    print(f"Extracting {category}: {link}")
    data_dict = extract_data(link)
    if data_dict:
        data_dict['category'] = category
        data_dict['link'] = link

        # Generate 'name' key
        data_dict['name'] = f"{category}_{len(data_list)}"

        data_list.append(data_dict)

        # Save image
        if data_dict['image_url']:
            download_image(data_dict['image_url'], data_dict['name'])

        # Introduce a wait time using sleep
        sleep(5)  # Sleep for 5 seconds between requests

def main():
    # Load URLs from JSON file
    with open("href_list_demo.json", "r") as file:
        extracted = json.load(file)

    # Process links using multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for category, links in extracted.items():
            for link in links:
                futures.append(executor.submit(process_link, category, link))
                break
        concurrent.futures.wait(futures)

    # Save data to JSON file
    with open("data_demo.json", 'w') as file:
        json.dump(data_list, file)


if __name__ == "__main__":
    main()