# Instagram Business Post Scraper

## Overview

This project is a Python script that allows you to scrape Instagram posts under a specific hashtag from business accounts in the category "Restaurant." The script uses the Selenium and selenium-wire to interact with the Instagram website and collect data about the posts, including post text, likes, comments, and date of publication.

## Requirements

- Python 3.x
- Google Chrome web browser

## Installation

1. Clone the repository to your local machine:
`git clone https://github.com/yourusername/instagram-post-scraper.git
cd instagram-post-scraper`

2. Install the required Python packages:
`pip install -r requirements.txt`

## Usage

1. Run the `main.py` script:

2. The script will prompt you to handle cookies and log in to Instagram using your username and password.

3. Enter the main hashtag and the secondary hashtag to search for in the post captions.

4. Specify the number of business accounts you want to scrape.

5. The script will start scraping the posts and display a progress bar with the total number of accounts to scrape.

6. After the scraping process is complete, the data will be saved in CSV and JSON formats with filenames based on the hashtags.

7. The script will also display the total duration of the scraping process and the number of posts scrolled.

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

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This project is intended for educational and personal use only. Scraping data from websites without permission may violate their terms of service. Use this script responsibly and at your own risk.

## Acknowledgments

This project was inspired by the need to collect data for research purposes. Special thanks to the authors of the libraries used in this project, as well as the open-source community for their valuable contributions.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.