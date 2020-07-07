import time
from bs4 import BeautifulSoup
from selenium import webdriver
import random
import threading
import numpy as np

def scroll(driver, timeout):
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time_start = time.time()
    
    while time.time()-time_start <= timeout:
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height != last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time_start = time.time()

        last_height = new_height

def parse_review(driver, row):
    review_id = row.get_attribute('id')
    review_more_id = ''.join(review_id.split('_'))
    
    try: 
        review_content_id = f'freeText{review_more_id}'
        review_short_id = f'freeTextContainer{review_more_id}'

        driver.execute_script(f'document.getElementById("{review_content_id}").style.display = "block";')
        driver.execute_script(f'document.getElementById("{review_short_id}").style.display = "none";')
    except:
        pass

    cols = row.find_elements_by_tag_name('td')
    cols = [el.text.strip() for el in cols if len(el.text.strip()) > 0]

    if len(cols) == 8: # if there was no rating given, add NULL
        cols.insert(3, 'NULL')
    cols.pop(4) # drop "my rating"

    try:
        book_id = row.find_element_by_css_selector('.field.cover > div.value div[data-resource-id]').get_attribute('data-resource-id')
    except:
        book_url = row.find_element_by_css_selector('.field.cover > div.value a').get_attribute('href')
        book_id = book_url.split('/')[-1].split('-')[0].split('.')[0]

    return [book_id, *cols[:5]]

def download_user_data(driver, user_id):
    driver.get(f'https://www.goodreads.com/user/show/{user_id}')

    reviews_url = driver.find_element_by_css_selector('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.leftContainer > div.leftAlignedProfilePicture > div > a:nth-child(5)').get_attribute('href')+'&shelf=read'
    driver.get(reviews_url)

    scroll(driver, 5)
    rows = driver.find_element_by_id('booksBody').find_elements_by_tag_name('tr')

    user_reviews_data = []
    for row in rows:
        review_data = parse_review(driver, row)
        cleaned_data = clean_data(review_data)
        user_reviews_data.append(cleaned_data)
        print(cleaned_data)

    return user_reviews_data

def clean_data(cleaned_data):
    cleaned_data[0],cleaned_data[3] = int(cleaned_data[0]), float(cleaned_data[3])

    try:
        cleaned_data[5] = cleaned_data[5].replace('\n...more','')
    except:
        pass

    rating_map = { 'NULL': -1, 'did not like it': 1, 'it was ok': 2, 'liked it': 3, 'really liked it': 4, 'it was amazing': 5 }
    cleaned_data[4] = rating_map[cleaned_data[4]]

    cleaned_data[5] = cleaned_data[5].replace("\n","")

    return cleaned_data

def download_users(driver, users):
    for user_id in users:
        try:
            user_data = download_user_data(driver, user_id)
            print(f'Downloaded user: {user_id}')
        except:
            # TODO: Log unsuccsessful downloads
            print(f'Could not download user: {user_id}')
        

def main():
    num_of_users_per_driver = 25
    num_of_drivers = 3

    sample = random.sample(range(1, 110000000), num_of_users_per_driver*num_of_drivers)
    users_batch = np.split(np.array(sample), num_of_drivers)

    # drivers = [ webdriver.Chrome('C:\ChromeDriver\chromedriver.exe') for _ in range(num_of_drivers) ]
    drivers = [ webdriver.Chrome(r'C:\Users\aniak\chromedriver.exe') for _ in range(num_of_drivers) ]
    #driver.set_window_position(-2000,0)#this function will minimize the window
    threads = []
    for k in range(num_of_drivers):
        t = threading.Thread(target=download_users, args=[drivers[k], users_batch[k]])
        t.start()

    for t in threads:
        t.join()            
        
if __name__ == '__main__':
    main()


# driver.quit()