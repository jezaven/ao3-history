# AO3 History Scraper
![GitHub issues](https://img.shields.io/github/issues-raw/jezaven/ao3-history?style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/jezaven/ao3-history?style=flat-square) ![GitHub](https://img.shields.io/github/license/jezaven/ao3-history?style=flat-square)

Web scraper for collecting a user's personal [AO3](https://archiveofourown.org) reading history and organizing all the story information.
## Usage

To run the project, you need to clone our repo and cd to the ao3_scrapy folder with
```Python
cd src/ao3_scraper/ao3_scraper
```

Add in your account information in the file ``/src/ao3_scrapy/ao3_scrapy/spiders/ao3_spider.py`` in line ``147``. Please note that you **must** have a valid AO3 account and Reading History enabled to use this API.

You can run our spider with the following command:
```Python
scrapy crawl history
```

If you want to save the output in a json file, run the following command:
```Python
scrapy crawl history -o nameoffile.json
```

## Future Work
We have a long ways to go before finishing this project. Currently, we aim to package our scraper so that it's as accessible as possible. We're also planning on creating a web app that uses the data from this API and analyzes it and creates visualizations for users.

## License
[MIT License](LICENSE.md)

Copyright (c) 2020 Fiza Goyal, Jessica Yang
