#!/env/bin python3

# Imports
from playwright.sync_api import sync_playwright
from getpass import getpass
import json
import time

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
def login_to_instagram(username, password):
    page.get_by_label("username").fill(username)
    page.get_by_label("password").fill(password)
    page.get_by_text("Log in", exact = True).click()

# handles not now popups
def handle_not_now_options():
    try:
        page.get_by_text("Not now", exact = True).click()
    except Exception as e:
        pass

    try:
        page.get_by_text("Not Now", exact = True).click()
    except Exception as e:
        pass

'''
Perform an HTTP request to the given URL and extract the JSON response data.

This function sends an HTTP request to the specified URL using the "page.expect_response()" method
and then calls a callable function attribute of the provided "locator" object. The name of the function
attribute is specified by the "locator_func" parameter. The called function can perform any actions
necessary to set up the HTTP request, such as adding headers or cookies.

Parameters:
    url (str): The URL to send the HTTP request to.
    locator (object): An object representing the locator. This object should have a callable function attribute
                  specified by "locator_func".
    locator_func (str): The name of the function attribute to call on the "locator" object. This function
                          will be executed within the context of the HTTP request.

Returns:
    dict: A Python dictionary containing the parsed JSON response data from the HTTP request.

Raises:
    ValueError: If the provided "locator_func" does not correspond to a callable function attribute
                of the "locator" object.
'''
def response_body_dic(url, locator, locator_func):
    action = getattr(locator, locator_func, None)
    if action is not None and callable(action): 
        with page.expect_response(url) as response_info:
            action()
        response = response_info.value
        return response.json()
    else:
        raise ValueError(f"The attribute '{locator_func}' is not a callable function in the locator object.")

# the scrape function that loops over number of posts (specified by max_iterations) and scrapes data of buisness accounts
def scrape_instagram_posts(hashtag, max_iterations = 10):
    accounts = {}
    start_time = time.time()

    # go to the hashtag page
    page.goto(f"https://www.instagram.com/explore/tags/{hashtag}/")

    for i in range(max_iterations):
        # get post data
        if i == 0:
            first_post = page.locator("//a[contains(@href, '/p/')]").first
            post_dic = response_body_dic(".*?/api/v1/media/.*?/info", first_post, "click")
        else:
            next_button = page.get_by_label("Next")
            post_dic = response_body_dic(".*?/api/v1/media/.*?/info", next_button, "click")

        # get account data
        try:
            user = page.locator("div._aasi > div > header > div._aaqy._aaqz > div._aar0._ad95._aar1 > div.x78zum5 > div > div > span > div > div > a")
            acc_dic = response_body_dic(".*?/api/v1/user/.*?/info", user, "hover")
        except Exception as e:
            continue

        # record the account and/or post if the account is buisness
        if acc_dic["user"]["is_business"]:
            # user data
            username = acc_dic["user"]["username"]
            link = user.get_attribute('href')
            followers = acc_dic["user"]["follower_count"]

            # post data
            date_of_pub = page.locator('div._ae5u._ae5v._ae5w > div > div > a > span > time').get_attribute('datetime')
            likes = post_dic["items"][0]["like_count"]
            comments = post_dic["items"][0]["comment_count"]

            if username in accounts:
                accounts[username].append_post(Post(likes, comments, date_of_pub))
            else:
                profile = Account(followers, link, username)
                profile.append_post(Post(likes, comments, date_of_pub))
                accounts[username] = profile

    end_time = time.time()
    duration = end_time - start_time
    return accounts, duration

# Main script
if __name__ == "__main__":

    with sync_playwright() as p:
        # Setting up playwright
        browser = p.chromium.launch(headless = False, channel = "chrome")
        page = browser.new_page()
        page.goto("https://www.instagram.com")

        # Logging in
        #username = input("Username: ")
        #password = getpass("Password: ")
        login_to_instagram("ninamuray3", "wexna4-suxkeb-gyFwov")

        # Handling NOT NOW options
        handle_not_now_options()

        # Get the hashtag
        hashtag = input("Enter the hashtag without '#': ")
        
        #https://www.instagram.com/explore/tags/ramen/?__a=1&__d=dis

        # Start Scraping
        scraped_accounts, total_duration = scrape_instagram_posts(hashtag)

        # Print the results of the run
        # Loop through the values of the dictionary and print each Account object
        for account in scraped_accounts.values():
            print(account)
            print()

        print(f"Total duration of the loop: {total_duration:.2f} seconds")
        print(f"Number of business accounts: {len(scraped_accounts)}")
