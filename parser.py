import csv
import json

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

def response_parser(user, media, hashtag, date, link, accounts, pb, driver):
    '''
    Parse the JSON response to record business accounts' posts 
    under a specific hashtag.

    Args:
        user (dict): The JSON response containing user data.
        media (dict): The JSON response containing media data.
        hashtag (str): The secondary hashtag to search for in the post caption.
        date (WebElement): The date of publication WebElement object.
        link (WebElement): The username link WebElement object.
        accounts (dict): A dictionary to store Account objects.
        pb (tqdm.tqdm): The tqdm progress bar for tracking
                        the number of accounts scraped.
        driver (WebDriver): The WebDriver object for 
                            interacting with the browser.
    '''
    # Record the account and/or post if the account is buisness
    # and has catergory "Restaurant"
    if user["user"]["is_business"] and \
            user["user"]["category"] == "Restaurant" and \
            f"#{hashtag}" in media["items"][0]["caption"]["text"]:

        username = user["user"]["username"]
        user_link = link.get_attribute('href')
        followers = user["user"]["follower_count"]

        date_of_pub = date.get_attribute('datetime')
        likes = media["items"][0]["like_count"]
        comments = media["items"][0]["comment_count"]
        text = media["items"][0]["caption"]["text"]
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
            pb.update(1)
