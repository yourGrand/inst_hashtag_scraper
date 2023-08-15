import time
import json
from getpass import getpass
from tqdm import tqdm
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from parser import response_parser, convert_to_csv, convert_to_json
from constants import *

def handle_cookie_options(driver):
    '''
    Handle cookies pop-ups if they appear.
    Args:
        driver (WebDriver): The WebDriver object for interacting with the browser.
    '''
    try:
        cookie = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, COOKIE_DECLINE_BUTTON))
        )
        cookie.click()
    except Exception as e:
        pass

def login_to_instagram(driver):
    '''
    Handle cookies if needed. Log in to Instagram using the provided WebDriver.
    Args:
        driver (WebDriver): The WebDriver object for interacting with the browser.
    '''
    # Validate user's cookies choice
    cookies_option = get_validated_input(
        "\nHandle cookies? (y/n): ", validate_yes_or_no
    )

    if cookies_option == "y":
        handle_cookie_options

    # Login
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, USERNAME_INPUT_SELECTOR))
    )
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, PASSWORD_INPUT_SELECTOR))
    )

    username.clear()
    username.send_keys(getpass("Enter you username: "))
    password.clear()
    password.send_keys(getpass("Enter you password: "))

    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR))
    )
    button.click()

# UNUSED
def handle_not_now_options(driver):
    '''
    Handle 'Not Now' pop-ups if they appear.
    Args:
        driver (WebDriver): The WebDriver object for interacting with the browser.
    '''
    try:
        not_now1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, NOT_NOW_SELECTOR_1))
        )
        not_now1.click()
    except Exception as e:
        pass

    try:
        not_now2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, NOT_NOW_SELECTOR_2))
        )
        not_now2.click()
    except Exception as e:
        pass

def get_response_dict(driver, url):
    '''
    Get the JSON response from a specific URL.
    Args:
        driver (WebDriver): The WebDriver object for interacting with the browser.
        url (str): The URL to get the response from.
    Returns:
        dict: The JSON response as a Python dictionary.
    '''
    request = driver.wait_for_request(url, 10)
    time.sleep(2)
    response = request.response
    response_decoded = json.loads(
        decode(
            response.body, response.headers.get('Content-Encoding', 'identity')
        )
    )

    return response_decoded

def independent_print(string):
    '''
    Print independent messeges in terminal
    Args:
        string: String to print
    '''
    print()
    print(string)
    print()


def scrape_instagram_posts(driver, num_accounts = 10, hashtag = "", main_category = "", backup_category = ""):
    '''
    Scrape Instagram posts under a specific hashtag from business accounts.
    Args:
        driver (WebDriver): The WebDriver object for interacting with the browser.
        num_accounts (int): The number of business accounts to scrape. 
                            Default is 10.
        hashtag (str): Secondary hashtag to filter users' accounts
        main_category (str): Main category of business accounts to filter
        backup_category (str): Secondary category of business accounts to filter
    Returns:
        tuple: A tuple containing the scraped data dictionary, 
               duration of the scrape, and the number of scrolls.
    '''
    accounts = {}
    action = ActionChains(driver)
    start_time = time.time()
    scrolls = 0

    # Progress bar with the total number of accounts as the maximum value
    progress_bar = tqdm(total = num_accounts, desc = "Scraping Instagram Posts")

    while len(accounts) != num_accounts:
        if scrolls == 0:
            try:
                first_post = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, POST_LINK_XPATH))
                )
                first_post.click()
                scrolls += 1
            except Exception as e:
                raise ValueError("The hashtag has no posts!")
        else:
            try:
                next_post1 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR, NEXT_BUTTON_SELECTOR1
                    ))
                )
                next_post1.click()
                scrolls += 1
            except Exception as e:
                independent_print(
                    "The very last post with entered hashtag was reached!"
                )
                break

        # if publication is collaborative, skip it.
        try:
            username_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, USERNAME_LINK_SELECTOR
                ))
            )
        except Exception as e:
            continue
        
        # post data
        media_dict = get_response_dict(driver, MEDIA_XPATH)
        date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, DATE_OF_PUB_SELECTOR
            ))
        )

        # user data
        action.move_to_element(username_link).perform()
        user_dict = get_response_dict(driver, USERNAME_XPATH)

        # record the account and/or post if the account is buisness
        # and has catergory "Restaurant"
        response_parser(
            user_dict,
            media_dict,
            hashtag,
            main_category,
            backup_category,
            date,
            username_link,
            accounts,
            progress_bar,
            driver
        )
                
        del driver.requests

    end_time = time.time()
    duration = end_time - start_time
    progress_bar.close()

    return accounts, duration, scrolls

def get_validated_input(prompt, validator_func):
    '''
    Prompt the user for input, validate it using the provided validator function,
    and keep prompting until valid input is received.
    Args:
        prompt (str): The message to display to the user as a prompt for input.
        validator_func (function): A function that takes a user input as a string
                                   and returns True if the input is valid, False otherwise.
    Returns:
        str: The user's valid input that passed the validation.
    '''
    while True:
        user_input = input(prompt)
        if validator_func(user_input):
            return user_input
        independent_print("Invalid input. Please try again.")

def validate_yes_or_no(input_str):
    '''
    Validate a user's input to check if it is either 'y' or 'n' (case-insensitive).
    Args:
        input_str (str): The user's input as a string.
    Returns:
        bool: True if the input is either 'y' or 'n', False otherwise.
    '''
    return input_str.lower() in ["y", "n"]


def validate_hashtag(input_str):
    '''
    Validate a user's input to check if it contains a '#' symbol.
    Args:
        input_str (str): The user's input as a string.
    Returns:
        bool: True if the input does not contain a '#', False otherwise.
    '''
    return "#" not in input_str


def validate_integer(input_str):
    '''
    Validate a user's input to check if it can be converted to an integer.
    Args:
        input_str (str): The user's input as a string.
    Returns:
        bool: True if the input can be converted to an integer, False otherwise.
    '''
    try:
        int(input_str)
        return True
    except ValueError:
        return False

def scrape(driver):
    '''
    Perform the scraping process for the user-specified hashtag.
    Main user's inputs.
    Args:
        driver (WebDriver): The WebDriver object for interacting with the browser.
    '''
    while True:
        # Warn user to remove previously scraped data files from the directory
        print()
        data_files_removed = get_validated_input(
            "Before scraping again, please ensure you have removed any\n"
            "previously scraped data files from the directory.\n"
            "Have you removed the data files? (y/n): ",
            validate_yes_or_no,
        )

        if data_files_removed == "n":
            independent_print(
                "Please remove the data files first before continuing."
            )
            continue

        # Validate user's hashtag inputs
        print()
        hashtag = get_validated_input(
            "Enter the main hashtag without '#': ", validate_hashtag
        )
        hashtag_2 = get_validated_input(
            "Enter the secondary hashtag without '#': ", validate_hashtag
        )

        # Handle user's category input
        print()
        print(
            "Warning: Providing a non-existent category could result\n in "
            "0 scraped accounts and may take a long time.\n"
            "Please ensure you enter a valid business category"
            " to get meaningful results.\n"
        )
        main_category = input(
            "Enter main category of business accounts"
            " to scrape (or leave blank): "
        )
        if main_category:
            backup_category = input(
                "Enter backup category of business accounts"
                " to scrape (or leave blank): "
            )
        else:
            backup_category = ""

        main_category = main_category.capitalize()
        backup_category = backup_category.capitalize()
        

        driver.get(f"{BASE_URL}/explore/tags/{hashtag}/")

        # Validate user's integer input
        print()
        num_accounts = int(
            get_validated_input(
                "Number of business accounts to scrape: ", validate_integer
            )
        )

        accounts, total_duration, num_of_scrolls = scrape_instagram_posts(
            driver, 
            num_accounts, 
            hashtag_2, 
            main_category, 
            backup_category
        )

        convert_to_csv(accounts, hashtag)
        convert_to_json(accounts, hashtag)

        independent_print(
            f"Total duration of the loop: {total_duration:.2f} seconds\n"
            f"Number of business accounts: {len(accounts)}\n"
            f"Number of posts scrolled: {num_of_scrolls}"
        )

        choice = input("Do you wish to scrape another hashtag? (y/n): ")
        if choice.lower() != "y":
            break
