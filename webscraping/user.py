import time
from bs4 import BeautifulSoup
from selenium import webdriver

def scroll(driver, timeout):
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(timeout)
    time_start = time.time()
    
    while True:
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height != last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time_start = time.time()

        if time.time()-time_start > timeout:
            break

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

    # not all IDs can be found this way, FIX it
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
        clean_data(review_data)
        user_reviews_data.append(review_data)
        print(review_data)

def clean_data(cleaned_data):
    cleaned_data[0],cleaned_data[3] = int(cleaned_data[0]), float(cleaned_data[3])
    try:
        cleaned_data[5] = cleaned_data[5].replace('\n...more','')
    except:
        pass
    if cleaned_data[4] == 'did not like it':
        cleaned_data[4] = 1
    elif cleaned_data[4] == 'it was ok':
        cleaned_data[4] = 2
    elif cleaned_data[4] == 'liked it':
        cleaned_data[4] = 3
    elif cleaned_data[4] == 'really liked it':
        cleaned_data[4] = 4
    elif cleaned_data[4] == 'it was amazing':
        cleaned_data[4] = 5
    cleaned_data[5] = cleaned_data[5].replace("\n","")
    return cleaned_data


def main():
    driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe')
    # driver = webdriver.Chrome(r'C:\Users\aniak\chromedriver.exe') 
    #driver.set_window_position(-2000,0)#this function will minimize the window

    first_user = 1
    last_user = 110000000

    for user_id in range(first_user, last_user):
        download_user_data(driver, user_id)
        
main()


# driver.quit()