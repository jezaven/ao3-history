# BeautifulSoup Usage
Earlier version of the scraper using BeautifulSoup. This was switched to scrapy for speed reasons.

## Testing Results
| # of Fics           | Fiza's Time     | Jessica's Time                  |
|:--------------------| ----------------| -------------------------------:|
| 53                  | 5.177 seconds   | 4.13 seconds                    |
| 2238                |                 | 194.7 seconds (before crashing) |
| 2316                | 284.977 seconds |                                 |
| 3390                |                 | 448.43 seconds (before crashing)|

The scraper can get through approximately 8-10 fics per second.

## Usage

To run the test file created, navigate to this folder and run `python3 stats.py`. You can replace the sample username and password with your own. It will store a csv file for you.

For other purposes, do the following:

Import the api with

`from history import User`

You can log in to your account with the following:

`user = User("username", "password")`

If you have Viewing History enabled, you can get information from that history, like so:

```
for work in user.reading_history():
    print(work.work_id)
    print(work.title)
    print(work.authors)
    print(work.words)
    print(work.rating)
    print(work.categories)
    print(work.fandoms)
    print(work.warnings)
    print(work.ships)
    print(work.characters)
    print(work.tags)
    print(work.summary)
    print(work.language)
    print(work.comments)
    print(work.kudos)
    print(work.bookmarks)
    print(work.hits)
    print(work.last_read)

```
