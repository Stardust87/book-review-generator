import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

def scroll(driver, timeout):
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(timeout)

    while True:
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height != last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time_start = time.time()

        if time.time()-time_start > timeout:
            break

        last_height = new_height


driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe') 
actions = ActionChains(driver)
#driver.set_window_position(-2000,0)#this function will minimize the window

first_user = 1
last_user = 2

for user_id in range(first_user, last_user):
    driver.get(f'https://www.goodreads.com/user/show/{user_id}')
    
    reviews_url = driver.find_element_by_css_selector('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.leftContainer > div.leftAlignedProfilePicture > div > a:nth-child(5)').get_attribute('href')+'&shelf=read'
    driver.get(reviews_url)

    scroll(driver, 5)
    rows = driver.find_element_by_id('booksBody').find_elements_by_tag_name('tr')

    user_reviews_data = []
    for row in rows:
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

        book_id = row.find_element_by_css_selector('.field.cover > div.value div[data-resource-id]').get_attribute('data-resource-id')
        print(book_id)
        user_reviews_data.append(cols[:5])
        print(cols[:5])
        



# driver.quit()