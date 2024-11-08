from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import csv


def extract_data():
    """
        It is function that extract all the required data from the specified link
    """
    try:
        # Product name
        names_ = [name.text for name in driver.find_elements(By.CSS_SELECTOR, "div h2 a span")]
        # Product price
        prices_ = [price.text for price in driver.find_elements(By.CSS_SELECTOR, "span .a-price-whole")]
        # Product ratings
        ratings_ = [rates.text for rates in driver.find_elements(By.XPATH, "//span[@class='a-size-base s-underline-text']")]
        # Product link
        links_ = [link.get_attribute("href") for link in driver.find_elements(By.XPATH, '//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')]
    except:
        """
            when above data is not available then N/A value will assign for the particular data
        """
        names_ = "N/A"
        prices_ = "N/A"
        ratings_ = "N/A"
        links_ = "N/A"

    return names_, prices_, ratings_, links_


driver = webdriver.Edge()
for page in range(107):
    driver.get("https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar&page={}".format(page))
    try:
        names, prices, ratings, links = extract_data()  # Calling function to get data
        with open("Details.csv", mode="w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Product name", "Price", "No of ratings", "Links"])    # Column heading
            for i in range(len(names)):
                writer.writerow([names[i], prices[i], ratings[i], links[i]])    # writing data in csv

        sleep(5)
    except:
        print("OutOfStock")
