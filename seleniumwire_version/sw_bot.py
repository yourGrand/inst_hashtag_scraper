# imports
# Selenium Wire
from seleniumwire import webdriver
from seleniumwire.utils import decode

# Selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

# Else
import time
import json

# Classes
class Post:
    def __init__(self, link, likes, comments, date_of_pub):
        self.link = link
        self.likes = likes
        self.comments = comments
        self.date_of_pub = date_of_pub

    def __str__(self):
        return f"\tpost_link = {self.link},\n\tlikes = {self.likes},\n\tcomments = {self.comments},\n\tdate of publication: {self.date_of_pub}"

class Account:
    def __init__(self, followers, link, username):
        self.posts = []
        self.followers = followers
        self.link = link
        self.username = username

    def append_post(self, post):
        if isinstance(post, Post):
            self.posts.append(post)
        else:
            raise ValueError("Only Post objects can be added to 'posts' attribute.")

    def __str__(self):
        posts_str = "\n".join([str(post) for post in self.posts])
        return f"username = {self.link.split('/')[-1]},\nfollowers = {self.followers},\nlink = {self.link},\nposts =\n{posts_str}"

# Functions
def login_to_instagram():
    # target username and password
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    # enter username and password
    username.clear()
    username.send_keys(input("Enter you username: "))
    password.clear()
    password.send_keys(input("Enter your password: "))

    # target the login button and click it
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

# handles not now popups
def handle_not_now_options():
    try:
        not_now1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Not now")]'))).click()
    except Exception as e:
        pass

    try:
        not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Not Now")]'))).click()
    except Exception as e:
        pass

# searches for hashtag
def search_hashtag():
    keyword = input("Enter the hashtag without '#': ")
    driver.get("https://www.instagram.com/explore/tags/" + keyword + "/")

# catch response from url and return dict of it
def get_response_dict(url):
    request = driver.wait_for_request(url, 10)
    time.sleep(2)
    response = request.response
    response_decoded = json.loads(decode(response.body, response.headers.get('Content-Encoding', 'identity')))

    return response_decoded

# the scrape function that loops over number of posts (specified by max_iterations) and scrapes data of buisness accounts
def scrape_instagram_posts(max_iterations = 10):
    accounts = {}
    action = ActionChains(driver)
    start_time = time.time()

    for i in range(70):
        if i == 0:
            # first post
            post = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/p/')]"))).click()
        else:
            # next post
            post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()
        
        # if publication is collaborative, skip it.
        try:
            username_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div._aasi > div > header > div._aaqy._aaqz > div._aar0._ad95._aar1 > div.x78zum5 > div > div > span > div > div > a')))
        except Exception as e:
            next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()
            continue
        
        # post data
        media_dict = get_response_dict(".*?/api/v1/media/.*?/info")

        # user data
        action.move_to_element(username_link).perform()
        user_dict = get_response_dict('.*?/api/v1/users/.*?/info')

        # record the account and/or post if the account is buisness
        if user_dict["user"]["is_business"]:
            username = user_dict["user"]["username"]
            user_link = username_link.get_attribute('href')
            followers = user_dict["user"]["follower_count"]
            date_of_pub = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._ae5u._ae5v._ae5w > div > div > a > span > time'))).get_attribute('datetime')
            likes = media_dict["items"][0]["like_count"]
            comments = media_dict["items"][0]["comment_count"]
            post_link = post.get_attribute('href')

            if username in accounts:
                accounts[username].append_post(Post(post_link, likes, comments, date_of_pub))
            else:
                profile = Account(followers, user_link)
                profile.append_post(Post(post_link, likes, comments, date_of_pub))
                accounts[username] = profile
                
        # clear previously captured requests
        del driver.requests

    end_time = time.time()
    duration = end_time - start_time

    return accounts, duration

# Main script
if __name__ == "__main__":
    # setting up
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com")

    login_to_instagram()
    handle_not_now_options()
    search_hashtag()

    # Start Scraping
    #max_iterations = input("Number of posts to scroll: ")
    scraped_accounts, total_duration = scrape_instagram_posts()

    # Print the results of the run
    # Loop through the values of the dictionary and print each Account object
    for account in scraped_accounts.values():
        print(account)
        print()

    print(f"Total duration of the loop: {total_duration:.2f} seconds")
    print(f"Number of business accounts: {len(scraped_accounts)}")

