from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

custom_dict = dict()
def get_href_list(category):
    url = f"https://kathmandupost.com/{category}"
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)
    time.sleep(5)


    button = driver.find_element(By.XPATH, "//span[@class='btn btn-default load-more-btn']")

    for i in range(3):
        try:
            time.sleep(2)
            driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
            button.click()
            time.sleep(5)
            break
        except:
            pass

    #find all article elements
    article_elements = driver.find_elements(
        By.XPATH,
        "//div[@class='block--morenews']//article/a")

    # Extract href attributes from article links
    href_list = [link.get_attribute("href") for link in article_elements if link.get_attribute("href") is not None]
    # print(href_list)
    custom_dict[category] = href_list

    driver.quit()

    return custom_dict

def main():
    # categories = ['sports', 'money', 'world', 'science-technology', 'climate-environment', 'art-culture', 'health']
    categories = ['sports']
    categories = sorted(categories)
    for category in categories:
        print(f"Extracting links from {category} category...")
        get_href_list(category)

    print(custom_dict)

    with open("href_list_demo.json", 'w') as f:
        json.dump(custom_dict, f)

    print("Saved to href_list.json successfully. ")

if __name__ == "__main__":
    main()