from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from scraper import login_to_instagram, scrape
from constants import *

def main():
    '''
    Main function to set up WebDriver, log in to Instagram, 
    and start the scraping process.
    '''

    chrome_options = Options()
    chrome_options.add_experimental_option(
        'excludeSwitches', 
        ['enable-logging']
    )

    # Uncomment the following line,  
    # to run this bot in headless mode.
    chrome_options.headless = True    # <-- this one

    driver = webdriver.Chrome(options = chrome_options)
    driver.get(BASE_URL)

    login_to_instagram(driver)
    scrape(driver)

    driver.quit()

# Main script
if __name__ == "__main__":
    main()
