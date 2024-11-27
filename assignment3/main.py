from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep
import mysql.connector
import csv


def extract_data():
    """
    Extracts bio, following, followers, location, and website from a Twitter profile using the provided link.

    Returns:
        tuple: A tuple containing the extracted data (bio, following, followers, location, website).
            If elements are not found, returns an empty string for that field.
    """
    bio_ = ""
    website_ = ""
    try:  # Handle login gracefully
        email = driver.find_element(By.NAME, 'text')
        email.send_keys("youremail@xyz.com", Keys.ENTER)
        sleep(2)
        try:  # Enter username and password both
            username = driver.find_element(By.NAME, "text")
            username.send_keys("your username", Keys.ENTER)
            sleep(2)
            password = driver.find_element(By.NAME, "password")
            password.send_keys("your password", Keys.ENTER)
        except NoSuchElementException:  # Enter only password
            password = driver.find_element(By.NAME, "password")
            password.send_keys("your password", Keys.ENTER)
    except NoSuchElementException:
        pass  # No login required
    finally:
        try:
            sleep(10)
            bio_ = driver.find_element(By.CSS_SELECTOR, 'div.css-175oi2r.r-1adg3ll.r-6gpygo div div span').text
            website_ = driver.find_element(By.XPATH, '//a[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0'
                                                     ' r-poiln3 r-4qtqp9 r-1a11zyx r-1loqt21"]').get_attribute("href")
        except NoSuchElementException:  # If there are no Boi or website
            if bio_ == "":
                website_ = driver.find_element(By.XPATH, '//a[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 '
                                                         'r-poiln3 r-4qtqp9 r-1a11zyx r-1loqt21"]').get_attribute("href")
        follow_elements = driver.find_elements(By.CSS_SELECTOR, 'a span span')
        following_ = follow_elements[0].text if len(follow_elements) >= 1 else ""
        followers_ = follow_elements[2].text if len(follow_elements) >= 3 else ""
        location_ = driver.find_element(By.CSS_SELECTOR, 'div.css-175oi2r.r-1adg3ll.r-6gpygo div span span span').text

    return bio_, following_, followers_, location_, website_  # returning the data


def add_in_mysql():
    """
        adding data in database using mysql-connector
    """
    db = mysql.connector.connect(
        host="localhost",
        user="user",
        passwd="password",
        database="testdatabase"
    )

    my_cursor = db.cursor()

    """
        Firstly if we doesn't create database then create a database in mysql using mysql-connector:
            "my_cursor.execute("CREATE DATABASE testdatabase")"
            OR
            In database 'create database testdatabase;'
        and add in mysql.connector like 'database="testdatabase"'
        
        Then create table by giving query:
            "CREATE TABLE profile(id int primary key,bio varchar(225),following varchar(10),followers varchar(10),
             location varchar(225),website varchar(225));"
        where id is the line number the link is. By which we can easily excess the data using 'WHERE' clos
    """

    sql = "INSERT INTO profile (id, bio, following, followers, location, website) VALUES (%s, %s, %s, %s, %s, %s)"
    my_cursor.executemany(sql, val)
    db.commit()
    print(my_cursor.rowcount, "was inserted.")  # no. of rows added


options = Options()
driver = webdriver.Chrome(options=options)  # Or other browser driver
val = []    # empty list for information
count = 0
with open('twitter_links.csv', 'r') as file:
    links = csv.reader(file)  # read data from file

    for link in links:  # iterate through data
        count += 1  # id in table
        if link[0] == 'http://www.twitter.com/' or link[0] == 'http://www.twitter.com':
            continue  # Skip invalid links
        print(link[0])
        driver.get(link[0])     # open browser
        sleep(10)

        bio, following, followers, location, website = extract_data()  # Calling function to get data
        val.append((count, bio, following, followers, location, website))   # create tuple and append in list

add_in_mysql()  # for adding all data in database
