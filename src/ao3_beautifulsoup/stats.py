from history import User
# from ao3.works import TooManyRequests
import time
import requests
import pandas as pd
import random

official_start_time = time.time()
user = User("jeza", "crappypw")

df = pd.DataFrame(columns=('id', 'title', 'authors', \
                           'words', 'rating', 'category', \
                           'fandoms', 'warnings', 'relationships', \
                           'characters', 'additional_tags', 'summary', \
                           'language', 'chapters', 'comments', 'kudos', \
                           'bookmarks', 'hits', 'last_visited', \
                           'last_updated', 'published'))

count = 0
start_time = time.time()
f1 = open('times.txt', 'a')

for work in user.reading_history():
    df.loc[count] = [work.work_id, work.title, work.authors, \
                                     work.words, work.rating, work.categories, \
                                     work.fandoms, work.warnings, work.ships, \
                                     work.characters, work.tags, work.summary, \
                                     work.language, "?", work.comments, work.kudos, \
                                     work.bookmarks, work.hits, work.last_read, \
                                     "", ""]
    print(str(count) + ": " + work.title)
    end_time = time.time()
    total_time = end_time - official_start_time
    print("--- %s seconds ---" % (total_time))
    f1.write(str(count) + ": " + str((end_time - start_time)) + "\n")
    start_time = end_time


    if (count % 10 == 0):
        df.to_csv('stats.csv')

    if (count % 1000 == 0):
        time.sleep(30.0)

    count += 1
