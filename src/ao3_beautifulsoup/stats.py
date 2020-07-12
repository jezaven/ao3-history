from history import User
# from ao3.works import TooManyRequests
import time
import requests
import pandas as pd
import random

start_time = time.time()
user = User("jeza", "crappypw")

df = pd.DataFrame(columns=('id', 'title', 'authors', \
                           'words', 'rating', 'category', \
                           'fandoms', 'warnings', 'relationships', \
                           'characters', 'additional_tags', 'summary', \
                           'language', 'chapters', 'comments', 'kudos', \
                           'bookmarks', 'hits', 'last_visited', \
                           'last_updated', 'published'))

count = 0
for work in user.reading_history():
    df.loc[count] = [work.work_id, work.title, work.authors, \
                                     work.words, work.rating, work.categories, \
                                     work.fandoms, work.warnings, work.ships, \
                                     work.characters, work.tags, work.summary, \
                                     work.language, "?", work.comments, work.kudos, \
                                     work.bookmarks, work.hits, work.last_read, \
                                     "", ""]
    print(str(count) + ": " + work.title)

    if (count % 10):
        df.to_csv('jeza_stats.csv')
    count += 1

print("--- %s seconds ---" % (time.time() - start_time))
