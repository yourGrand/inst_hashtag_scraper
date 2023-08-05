import time
import json
import csv
from tqdm import tqdm
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from constants import *

class Post:
    '''
    Initialize a Post object.
    Args:
        post_text (str): The post's description
        post_link (str): The link to the post.
        likes (int): Number of likes on the post.
        comments (int): Number of comments on the post.
        date_of_pub (str): Date of publication in ISO format.
    '''
    def __init__(self, post_text, post_link, likes, comments, date_of_pub):
        self.post_text = post_text
        self.post_link = post_link
        self.likes = likes
        self.comments = comments
        self.date_of_pub = date_of_pub

    def __str__(self):
        return (
            f"\tpost text = {self.post_text},\n"
            f"\tpost link = {self.post_link},\n"
            f"\tlikes = {self.likes},\n"
            f"\tcomments = {self.comments},\n"
            f"\tdate of publication: {self.date_of_pub}"
        )

    def to_dict(self):
        '''
        Convert Post object to a dictionary.
        Returns:
            dict: Dictionary representation of the Post object.
        '''
        return {
            "post_text": self.post_text,
            "post_link": self.post_link,
            "likes": self.likes,
            "comments": self.comments,
            "date_of_pub": self.date_of_pub
        }

class Account:
    '''
    Initialize an Account object.
    Args:
        followers (int): Number of followers for the account.
        user_link (str): The link to the account.
        username (str): The username of the account.
    '''
    def __init__(self, followers, user_link, username):
        self.posts = []
        self.followers = followers
        self.user_link = user_link
        self.username = username

    def __str__(self):
        posts_str = "\n".join([str(post) for post in self.posts])
        return (
            f"username = {self.username},\n"
            f"followers = {self.followers},\n"
            f"user link = {self.user_link},\n"
            f"posts =\n{posts_str}"
        )

    def append_post(self, post):
        '''
        Append a Post object to the Account's list of posts.
        Args:
            post (Post): The Post object to be added.
        Raises:
            ValueError: If the input is not a Post object.
        '''
        if isinstance(post, Post):
            self.posts.append(post)
        else:
            raise ValueError(
                "Only Post objects can be added to 'posts' attribute."
            )

    def to_dict(self):
        '''
        Convert Account object to a dictionary.
        Returns:
            dict: Dictionary representation of the Account object.
        '''
        return {
            "followers": self.followers,
            "user_link": self.user_link,
            "username": self.username,
            "posts": [post.to_dict() for post in self.posts]
        }

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
        "Handle cookies? (y/n): ", validate_yes_or_no
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
    username.send_keys(input("Enter you username: "))
    password.clear()
    password.send_keys(input("Enter you password: "))

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

def convert_to_csv(data_dict, hashtag):
    '''
    Convert scraped data to CSV format and save it to a file.
    Args:
        data_dict (dict): A dictionary containing scraped data.
        hashtag (str): The hashtag used for the filename.
    '''
    csv_file = f"{hashtag}.csv"

    with open(csv_file, mode = "w", newline = "", encoding = "utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "username",
            "followers",
            "user link",
            "post link",
            "likes",
            "comments",
            "post text",
            "date of pub"
        ])

        for account in data_dict.values():
            for post in account.posts:
                writer.writerow([
                    account.username, 
                    account.followers, 
                    account.user_link, 
                    post.post_link, 
                    post.likes, 
                    post.comments,
                    post.post_text, 
                    post.date_of_pub
                ])

def convert_to_json(data_dict, hashtag):
    '''
    Convert scraped data to JSON format and save it to a file.
    Args:
        data_dict (dict): A dictionary containing scraped data.
        hashtag (str): The hashtag used for the filename.
    '''
    json_file = f"{hashtag}.json"

    with open(json_file, mode = "w", encoding = "utf-8") as file:
        json.dump(data_dict, file, indent=4, default=lambda x: x.to_dict())

def independent_print(string):
    '''
    Print independent messeges in terminal
    Args:
        string: String to print
    '''
    print()
    print(string)
    print()


def scrape_instagram_posts(driver, num_accounts = 10, hashtag_2 = ""):
    '''
    Scrape Instagram posts under a specific hashtag from business accounts.
    Args:
        driver (WebDriver): The WebDriver object for interacting with the browser.
        num_accounts (int): The number of business accounts to scrape. 
                            Default is 10.
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

        # user data
        action.move_to_element(username_link).perform()
        user_dict = get_response_dict(driver, USERNAME_XPATH)

        # record the account and/or post if the account is buisness
        # and has catergory "Restaurant"
        if user_dict["user"]["is_business"] and \
                user_dict["user"]["category"] == "Restaurant" and \
                f"#{hashtag_2}" in media_dict["items"][0]["caption"]["text"]:

            username = user_dict["user"]["username"]
            user_link = username_link.get_attribute('href')
            followers = user_dict["user"]["follower_count"]
            date = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, DATE_OF_PUB_SELECTOR
                ))
            )
            date_of_pub = date.get_attribute('datetime')
            likes = media_dict["items"][0]["like_count"]
            comments = media_dict["items"][0]["comment_count"]
            text = media_dict["items"][0]["caption"]["text"]
            post_link = driver.current_url

            if username in accounts:
                accounts[username].append_post(
                    Post(text, post_link, likes, comments, date_of_pub)
                )
            else:
                profile = Account(followers, user_link, username)
                profile.append_post(
                    Post(text, post_link, likes, comments, date_of_pub)
                )
                accounts[username] = profile
                progress_bar.update(1)
                
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
    Args:
        driver (WebDriver): The WebDriver object for interacting with the browser.
    '''
    while True:
        # Warn user to remove previously scraped data files from the directory
        data_files_removed = get_validated_input(
            "Before scraping again, please ensure you have removed any\n"
            "previously scraped data files from the directory.\n"
            "Have you removed the data files? (y/n): ",
            validate_yes_or_no,
        )

        if data_files_removed.lower() == "n":
            independent_print(
                "Please remove the data files first before continuing."
            )
            continue

        # Validate user's hashtag inputs
        hashtag = get_validated_input(
            "Enter the main hashtag without '#': ", validate_hashtag
        )
        hashtag_2 = get_validated_input(
            "Enter the secondary hashtag without '#': ", validate_hashtag
        )

        driver.get(f"{BASE_URL}/explore/tags/{hashtag}/")

        # Validate user's integer input
        num_accounts = int(
            get_validated_input(
                "Number of business accounts to scrape: ", validate_integer
            )
        )

        accounts, total_duration, num_of_scrolls = scrape_instagram_posts(
            driver, num_accounts, hashtag_2
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
    # chrome_options.headless = True    # <-- this one

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(BASE_URL)

    login_to_instagram(driver)

    scrape(driver)

    driver.quit()

# Main script
if __name__ == "__main__":
    main()
