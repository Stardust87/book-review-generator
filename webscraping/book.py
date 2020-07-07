import time
from bs4 import BeautifulSoup
from selenium import webdriver
##copy chromedriver into python folder
# driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe')
driver = webdriver.Chrome(r'C:\Users\aniak\chromedriver.exe')
#driver.set_window_position(-2000,0)#this function will minimize the window
first_url = 1
last_url = 3    # Last book is 8,630,000

for book_reference_number in range(first_url, last_url):
    driver.get("https://www.goodreads.com/book/show/"+str(book_reference_number))
    #time.sleep(2)#optional
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        book_title = soup.select('.gr-h1.gr-h1--serif')[0].text.strip()
    except:
        book_title = ''
    try:
        author_name = soup.select('.authorName')[0].text.strip()
    except:
        author_name = ''
    try:
        book_description = soup.select("#description span:nth-child(2)")[0].text.strip()
    except:
        book_description = ''
    try:
        book_format = soup.select("div.row span:nth-child(1)")[0].text.strip()
    except:
        book_format= ''
    try:
        book_language = soup.select("div[itemprop='inLanguage']")[0].text.strip()
    except:
        book_language= ''
    try:
        genre= [value.text.strip() for value in soup.select("div.elementList  div:nth-child(1)")]
        genre_users= [value.text.strip() for value in soup.select("div.elementList  div:nth-child(2)")]
    except:
        genre = []
        genre_users = []


    print('NO.', book_reference_number, ', TITLE: ', book_title, ', AUTHOR: ', author_name,', DESCRIPTION: ',book_description,', FORMAT: ', book_format,', LANGUAGE: ', book_language,', GENRES&USERS: ',genre,genre_users) 
   