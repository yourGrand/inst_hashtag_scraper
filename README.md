# Instagram Business Post Scraper

## Project Overview

This project involves a Python script designed to scrape Instagram posts. It targets business accounts within a user-defined category by searching for a specific hashtag. To achieve this, the script employs the [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) along with [Selenium Wire](https://github.com/wkeeling/selenium-wire). These tools enable interaction with the Instagram website, facilitating the extraction of various post details. The collected data includes post text, likes, comments, and the publication date.

## Requirements

- Python 3.x
- Google Chrome web browser

### Disclaimer

- This script has been tested and verified to work on macOS Ventura 13.4.1. While it may work on other operating systems, we cannot guarantee full compatibility. Use it on other platforms at your own risk.

- This project is intended for educational and personal use only. Scraping data from websites without permission may violate their terms of service. Use this script responsibly and at your own risk.

## Installation

1. Clone the repository to your local machine:

`git clone https://github.com/yourGrand/instagram-post-scraper.git`

`cd instagram-post-scraper`

2. Install the required Python packages:

`pip install -r requirements.txt`

3. Consider installing Selenium Wire's root certificate or your own root certificate to get rid of the "Not Secure" message and/or unlocked padlock in the address bar. You can read more about certificates and how to install them in the [Selenium Wire documentation](https://github.com/wkeeling/selenium-wire#certificates).

## Usage

1. Run the `main.py` script

2. The script will prompt you to handle cookies and log in to your Instagram account using your username and password.

3. Enter the main and secondary hashtags you'd like to search for. The secondary hashtag will be used to filter posts that also include the main hashtag.

4. Provide the main and backup categories for business accounts. If the main category isn't detected, the script will check for the backup category.

5. Specify the number of business accounts you intend to scrape data from.

6. The script will begin the scraping process, retrieving posts and related data based on the provided hashtags and business account categories. A progress bar will indicate the number of accounts being scraped.

7. Once the scraping is complete, the collected data will be saved in both CSV and JSON formats. The filenames for these files will be generated based on the hashtags you provided.

8. The script will display the total duration of the scraping process and the count of posts that were scrolled through during the scraping.

## Data Output

The scraped data will be saved in CSV and JSON formats in the project directory. The files will be named after the main hashtag.

The CSV file will contain the following columns:

- Username
- Followers
- User Link
- Post Link
- Likes
- Comments
- Post Text
- Date of Publication

The JSON file will contain a dictionary with usernames as keys and corresponding Account objects as values. Each Account object will contain a list of Post objects with post details.

## Important Notes

- Make sure to remove any previously scraped data files from the directory before running the script again.
- The script may encounter pop-ups or variations in the Instagram website's structure, which may require updates to the code.

## License

This project is licensed under the GNU General Public License (GPL) - see the [LICENSE](LICENSE.txt) file for details.

## Acknowledgments

This project was inspired by the need to collect data for research purposes. Special thanks to the authors of the libraries used in this project, as well as the open-source community for their valuable contributions.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

