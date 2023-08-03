# CSS Selectors
USERNAME_INPUT_SELECTOR = 'input[name="username"]'
PASSWORD_INPUT_SELECTOR = 'input[name="password"]'
LOGIN_BUTTON_SELECTOR = 'button[type="submit"]'
NOT_NOW_SELECTOR_1 = '//div[contains(text(), "Not now")]'
NOT_NOW_SELECTOR_2 = '//button[contains(text(), "Not Now")]'
USERNAME_LINK_SELECTOR = (
    'div._aasi > div > header > div._aaqy._aaqz > div._aar0._ad95._aar1 > '
    'div.x78zum5 > div > div > span > div > div > a'
)
NEXT_BUTTON_SELECTOR1 = '[aria-label="Next"]'
NEXT_BUTTON_SELECTOR2 = 'button[class="_abl-"]'
DATE_OF_PUB_SELECTOR = 'div._ae5u._ae5v._ae5w > div > div > a > span > time'

# change from 'button[class="_a9-- _a9_1"]'
# to 'button[class="_a9-- _a9_0"]' to accept cookies. Default - decline
COOKIE_DECLINE_BUTTON = 'button[class="_a9-- _a9_1"]' # <-- here

# XPaths
POST_LINK_XPATH = "//a[contains(@href, '/p/')]"
USERNAME_XPATH = ".*?/api/v1/users/.*?/info"
MEDIA_XPATH = ".*?/api/v1/media/.*?/info"

# Base URL
BASE_URL = "https://www.instagram.com"