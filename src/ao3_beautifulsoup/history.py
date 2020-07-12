# -*- encoding: utf-8

from datetime import datetime
import collections
import itertools
import re

from bs4 import BeautifulSoup, Tag
import requests

ReadingHistoryItem = collections.namedtuple(
    'ReadingHistoryItem', ['work_id', 'title', 'authors', 'fandoms', \
    'ships', 'characters', 'tags', 'summary', 'rating', 'warnings', \
    'categories', 'iswip', 'language', 'words', 'comments', 'kudos', 'bookmarks', \
    'hits', 'last_read'])

class User(object):

    def __init__(self, username, password=None, sess=None):
        self.username = username

        if sess == None:
            sess = requests.Session()

        if password != None:
            req = sess.get('https://archiveofourown.org')
            soup = BeautifulSoup(req.text, features='html.parser')

        authenticity_token = soup.find('input', {'name': 'authenticity_token'})['value']

        req = sess.post('https://archiveofourown.org/users/login', params={
            'authenticity_token': authenticity_token,
            'user[login]': username,
            'user[password]': password,
        })

        # Unfortunately AO3 doesn't use HTTP status codes to communicate
        # results -- it's a 200 even if the login fails.
        if 'Please try again' in req.text:
            raise RuntimeError(
                'Error logging in to AO3; is your password correct?')

        self.sess = sess
    def __repr__(self):
        return '%s(username=%r)' % (type(self).__name__, self.username)

    def _lookup_stat(self, li_tag, class_name, default=None):
        """Returns the value of a stat."""
        # The stats are stored in a series of divs of the form
        #
        #     <dd class="[field_name]">[field_value]</div>
        #
        dd_tag = li_tag.find('dd', attrs={'class': class_name})
        if dd_tag is None:
            return default
        # if 'tags' in dd_tag.attrs['class']:
        #     return self._lookup_list_stat(dd_tag=dd_tag)
        return dd_tag.contents[0]

    def reading_history(self):
        """Returns information about works in the user's reading history.

        This requires the user to turn on the Viewing History feature.

        """
        api_url = (
            'https://archiveofourown.org/users/%s/readings?page=%%d' %
            self.username)

        for page_no in itertools.count(start=1):
            print("PAGE NUM: " + str(page_no))
            req = self.sess.get(api_url % page_no)
            soup = BeautifulSoup(req.text, features='html.parser')

            # The entries are stored in a list of the form:
            #
            #     <ol class="reading work index group">
            #       <li id="work_12345" class="reading work blurb group">
            #         ...
            #       </li>
            #       <li id="work_67890" class="reading work blurb group">
            #         ...
            #       </li>
            #       ...
            #     </ol>
            #
            ol_tag = soup.find('ol', attrs={'class': 'reading'})
            for li_tag in ol_tag.find_all('li', attrs={'class': 'blurb'}):
                try:
                    work_id = li_tag.attrs['id'].replace('work_', '')
                    # print("id: " + work_id)

                    heading = li_tag.find('h4', attrs={'class': 'heading'})
                    if (heading.text == "Mystery Work"):
                        continue

                    title = heading.find('a').text
                    # print(title)

                    authors = []
                    for author in li_tag.find_all('a', attrs={'rel': 'author'}):
                        authors.append(author.text)
                    # print(authors)

                    fandoms_tag = li_tag.find('h5', attrs={'class': 'fandoms'})
                    fandoms = []
                    for fandom_a in fandoms_tag.find_all('a', attrs={'class': 'tag'}):
                        fandoms.append(fandom_a.text)
                    # print(fandoms)

                    ships = []
                    for ship in li_tag.find_all('li', attrs={'class': 'relationships'}):
                        ships.append(ship.text)
                    # print(ships)

                    characters = []
                    for character in li_tag.find_all('li', attrs={'class': 'characters'}):
                        characters.append(character.text)
                    # print(characters)

                    addl_tags = []
                    for tag in li_tag.find_all('li', attrs={'class': 'freeforms'}):
                        addl_tags.append(tag.text)
                    # print(addl_tags)

                    blockquote = li_tag.find('blockquote', attrs={'class': 'summary'})
                    if (blockquote == None):
                        summary = "none"
                    else:
                        summary = blockquote.renderContents().decode('utf8').strip()
                    # print(summary)

                    rating = li_tag.find('span', attrs={'class': 'rating'}).attrs['title']
                    # print("rating: " + rating)

                    warnings = li_tag.find('span', attrs={'class': 'warnings'}).attrs['title'].split(", ")
                    # print(warnings)

                    categories = li_tag.find('span', attrs={'class': 'category'}).attrs['title'].split(", ")
                    # print(categories)

                    iswip_tag = li_tag.find('span', attrs={'class': 'iswip'}).attrs['title']
                    if (iswip_tag == "Work in Progress"):
                        iswip = True
                    else:
                        iswip = False
                    # print("iswip: " + str(iswip))

                    language = self._lookup_stat(li_tag, 'language', 0)
                    # print("language: " + str(language))

                    words = int(self._lookup_stat(li_tag, 'words', 0).replace(',', ''))
                    # print("words: " + str(words))

                    # chapters = self._lookup_stat(li_tag, 'chapters', 0)
                    # print("chapters: " + str(chapters)) # needs a lot of work

                    comments_tag = self._lookup_stat(li_tag, 'comments', 0)
                    if (comments_tag == 0):
                        comments = 0
                    else:
                        comments = int(comments_tag.text)
                    # print("comments: " + str(comments))

                    kudos_tag = self._lookup_stat(li_tag, 'kudos', 0)
                    if (kudos_tag == 0):
                        kudos = 0
                    else:
                        kudos = int(kudos_tag.text)
                    # print("kudos: " + str(kudos))

                    bookmark_tag = self._lookup_stat(li_tag, 'bookmarks', 0)
                    if (bookmark_tag == 0):
                        bookmarks = 0
                    else:
                        bookmarks = bookmark_tag.text
                    # print("bookmarks: " + str(bookmrks))

                    hits = int(self._lookup_stat(li_tag, 'hits', 0))
                    # print("hits: " + str(hits))

                    # Within the <li>, the last viewed date is stored as
                    #
                    #     <h4 class="viewed heading">
                    #         <span>Last viewed:</span> 24 Dec 2012
                    #
                    #         (Latest version.)
                    #
                    #         Viewed once
                    #     </h4>
                    #
                    h4_tag = li_tag.find('h4', attrs={'class': 'viewed'})
                    date_str = re.search(
                        r'[0-9]{1,2} [A-Z][a-z]+ [0-9]{4}',
                        h4_tag.contents[2]).group(0)
                    date = datetime.strptime(date_str, '%d %b %Y').date()

                    yield ReadingHistoryItem(work_id, title, authors, fandoms, \
                    ships, characters, addl_tags, summary, rating, warnings, \
                    categories, iswip, language, words, comments, kudos, bookmarks, \
                    hits, date)
                except KeyError:
                    # A deleted work shows up as
                    #
                    #      <li class="deleted reading work blurb group">
                    #
                    # There's nothing that we can do about that, so just skip
                    # over it.
                    if 'deleted' in li_tag.attrs['class']:
                        pass
                    else:
                        raise

            # The pagination button at the end of the page is of the form
            #
            #     <li class="next" title="next"> ... </li>
            #
            # If there's another page of results, this contains an <a> tag
            # pointing to the next page.  Otherwise, it contains a <span>
            # tag with the 'disabled' class.
            try:
                next_button = soup.find('li', attrs={'class': 'next'})
                if next_button.find('span', attrs={'class': 'disabled'}):
                    break
            except:
                # In case of absence of "next"
                break
