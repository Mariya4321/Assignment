from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv
import os
from dotenv import load_dotenv

load_dotenv()


def extract_data():
    """
    Extracts bio, following, followers, location, and website from a Twitter profile using the provided link.

    Returns:
        tuple: A tuple containing the extracted data (bio, following, followers, location, website).
            If elements are not found, returns an empty string for that field.
    """
    bio_ = ""
    website_ = ""
    try:    # Handle login gracefully
        email = driver.find_element(By.NAME, 'text')
        email.send_keys(os.environ['EMAIL_X'], Keys.ENTER)
        sleep(2)
        try:     # Enter username and password both
            username = driver.find_element(By.NAME, "text")
            username.send_keys(os.environ['USERNAME_X'], Keys.ENTER)
            sleep(2)
            password = driver.find_element(By.NAME, "password")
            password.send_keys(os.environ['PASSWORD_X'], Keys.ENTER)
        except NoSuchElementException:  # Enter only password
            password = driver.find_element(By.NAME, "password")
            password.send_keys(os.environ['PASSWORD_X'], Keys.ENTER)
    except NoSuchElementException:
        pass    # No login required
    finally:
        try:
            sleep(10)
            bio_ = driver.find_element(By.CSS_SELECTOR, 'div.css-175oi2r.r-1adg3ll.r-6gpygo div div span').text
            website_ = driver.find_element(By.XPATH, '//a[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-4qtqp9 r-1a11zyx r-1loqt21"]').get_attribute("href")
        except NoSuchElementException:  # If there are no Boi or website
            if bio_ == "":
                website_ = driver.find_element(By.XPATH, '//a[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-4qtqp9 r-1a11zyx r-1loqt21"]').get_attribute("href")
        follow_elements = driver.find_elements(By.CSS_SELECTOR, 'a span span')
        following_ = follow_elements[0].text if len(follow_elements) >= 1 else ""
        followers_ = follow_elements[2].text if len(follow_elements) >= 3 else ""
        location_ = driver.find_element(By.CSS_SELECTOR, 'div.css-175oi2r.r-1adg3ll.r-6gpygo div span span span').text

    return bio_, following_, followers_, location_, website_    # returning the data


driver = webdriver.Edge()   # Or other browser driver

with open('twitter_links.csv', 'r') as file:
    links = csv.reader(file)    # read data from file

    for link in links:  # iterate through data
        if link[0] == 'http://www.twitter.com/' or link[0] == 'http://www.twitter.com':
            continue  # Skip invalid links
        print(link[0])
        driver.get(link[0])
        sleep(10)

        bio, following, followers, location, website = extract_data()  # Calling function to get data
        with open("Details.csv", mode="a", newline='') as csvfile:      # open csv file
            writer = csv.writer(csvfile)
            writer.writerow([bio, following, followers, location, website])     # writing data

        sleep(5)    # Adjust wait time between profiles

