#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], 'src'))

from check_status import check_status
from feed_scanner import feed_scanner
from follow_protocol import follow_protocol
from instabot import InstaBot
from unfollow_protocol import unfollow_protocol

bot = InstaBot(
    login="username",
    password="password",
    like_per_day=1000,
    comments_per_day=0,
    tag_list=['follow4follow', 'f4f', 'cute'],
    tag_blacklist=['rain', 'thunderstorm'],
    user_blacklist={},
    max_like_for_one_tag=50,
    follow_per_day=300,
    follow_time=1 * 60,
    unfollow_per_day=300,
    unfollow_break_min=15,
    unfollow_break_max=30,
    log_mod=0,
    proxy='',
    # List of list of words, each of which will be used to generate comment
    # For example: "This shot feels wow!"
    comment_list=[["this", "the", "your"],
                  ["photo", "picture", "pic", "shot", "snapshot"],
                  ["is", "looks", "feels", "is really"],
                  ["great", "super", "good", "very good", "good", "wow",
                   "WOW", "cool", "GREAT","magnificent", "magical",
                   "very cool", "stylish", "beautiful", "so beautiful",
                   "so stylish", "so professional", "lovely",
                   "so lovely", "very lovely", "glorious","so glorious",
                   "very glorious", "adorable", "excellent", "amazing"],
                  [".", "..", "...", "!", "!!", "!!!"]],
    # Use unwanted_username_list to block usernames containing a string
    ## Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
    ### 'free_followers' will be blocked because it contains 'free'
    unwanted_username_list=[
        'second', 'stuff', 'art', 'project', 'love', 'life', 'food', 'blog',
        'free', 'keren', 'photo', 'graphy', 'indo', 'travel', 'art', 'shop',
        'store', 'sex', 'toko', 'jual', 'online', 'murah', 'jam', 'kaos',
        'case', 'baju', 'fashion', 'corp', 'tas', 'butik', 'grosir', 'karpet',
        'sosis', 'salon', 'skin', 'care', 'cloth', 'tech', 'rental', 'kamera',
        'beauty', 'express', 'kredit', 'collection', 'impor', 'preloved',
        'follow', 'follower', 'gain', '.id', '_id', 'bags'
    ],
    unfollow_whitelist=['example_user_1', 'example_user_2'])
while True:

    #print("# MODE 0 = ORIGINAL MODE BY LEVPASHA")
    #print("## MODE 1 = MODIFIED MODE BY KEMONG")
    #print("### MODE 2 = ORIGINAL MODE + UNFOLLOW WHO DON'T FOLLOW BACK")
    #print("#### MODE 3 = MODIFIED MODE : UNFOLLOW USERS WHO DON'T FOLLOW YOU BASED ON RECENT FEED")
    #print("##### MODE 4 = MODIFIED MODE : FOLLOW USERS BASED ON RECENT FEED ONLY")
    #print("###### MODE 5 = MODIFIED MODE : JUST UNFOLLOW EVERYBODY, EITHER YOUR FOLLOWER OR NOT")

    ################################
    ##  WARNING   ###
    ################################

    # DON'T USE MODE 5 FOR A LONG PERIOD. YOU RISK YOUR ACCOUNT FROM GETTING BANNED
    ## USE MODE 5 IN BURST MODE, USE IT TO UNFOLLOW PEOPLE AS MANY AS YOU WANT IN SHORT TIME PERIOD

    mode = 0

    #print("You choose mode : %i" %(mode))
    #print("CTRL + C to cancel this operation or wait 30 seconds to start")
    #time.sleep(30)

    if mode == 0:
        bot.new_auto_mod()

    elif mode == 1:
        check_status(bot)
        while bot.self_following - bot.self_follower > 200:
            unfollow_protocol(bot)
            time.sleep(10 * 60)
            check_status(bot)
        while bot.self_following - bot.self_follower < 400:
            while len(bot.user_info_list) < 50:
                feed_scanner(bot)
                time.sleep(5 * 60)
                follow_protocol(bot)
                time.sleep(10 * 60)
                check_status(bot)

    elif mode == 2:
        bot.bot_mode = 1
        bot.new_auto_mod()

    elif mode == 3:
        unfollow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 4:
        feed_scanner(bot)
        time.sleep(60)
        follow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 5:
        bot.bot_mode = 2
        unfollow_protocol(bot)

    else:
        print("Wrong mode!")
from user_info import get_user_info


def check_status(self):
    self.is_self_checking = True
    self.is_checked = False
    while self.is_checked != True:
        get_user_info(self, self.user_login)
    self.like_counter = 0
    self.follow_counter = 0
    self.unfollow_counter = 0
import random
import time

from likers_graber_protocol import likers_graber_protocol
from new_auto_mod_unfollow2 import new_auto_mod_unfollow2
from recent_feed import get_media_id_recent_feed
from user_feed import get_media_id_user_feed


def feed_scanner(self):
    #This is to limit how many people do you want to put into list before
    ##The bot start to check their profile one by one and start following them
    limit = random.randint(51, 90)
    while len(self.user_info_list) < limit:
        #First the bot try to collect media id on your recent feed
        get_media_id_recent_feed(self)
        #If your account is old enough, there will be 24 photos on your recent feed
        if len(self.media_on_feed) > 23:
            #Select the media on your recent feed randomly
            chooser = random.randint(0, len(self.media_on_feed) - 1)
            #The bot will save the owner of the media name and use it to try checking his/her profile
            self.current_user = self.media_on_feed[chooser]["node"]["owner"][
                "id"]
            self.current_id = self.media_on_feed[chooser]["node"]["owner"][
                "id"]

        #If your account is new, and you don't following anyone, your recent feed will be empty
        else:
            #If your recent feed is empty, then you start collecting media id by hashtag
            self.is_by_tag = True
            get_media_id_user_feed(self)
            max_media = 0
            while len(self.media_on_feed) > 5 and max_media < 5:
                chooser = random.randint(0, len(self.media_on_feed) - 1)
                self.current_id = self.media_on_feed[chooser]["node"]["owner"][
                    "id"]
                self.follow(self.current_id)
                self.media_on_feed[chooser] = None
                max_media += 1
                time.sleep(30)
            self.is_by_tag = False
            self.media_on_feed = []
        if len(self.user_info_list) < 10000:
            for index in range(len(self.ex_user_list)):
                if self.ex_user_list[index][0] in self.current_user:
                    print(
                        '============================== \nUpss ' +
                        self.current_user +
                        ' is already in ex user list... \n=============================='
                    )
                    break
            else:
                likers_graber_protocol(self)
                self.ex_user_list.append([self.current_user, self.current_id])
            self.user_list = []
            self.media_by_user = []
            self.media_on_feed = []

        if len(self.ex_user_list) > 20:
            chooser = random.randint(0, len(self.ex_user_list) - 1)
            self.current_user = self.ex_user_list[chooser][0]
            self.current_id = self.ex_user_list[chooser][1]
            print('Trying to unfollow : ' + self.current_user)
            new_auto_mod_unfollow2(self)
            del self.ex_user_list[chooser]
        time.sleep(random.randint(15, 22))
        import random
import time

from feed_scanner import feed_scanner
from user_info import get_user_info


def follow_protocol(self):
    limit = random.randint(5, 10)
    while self.follow_counter < limit:
        chooser = 0
        if len(self.user_info_list) > 0:
            chooser = random.randint(0, len(self.user_info_list) - 1)
            self.current_user = self.user_info_list[chooser][0]
            self.current_id = self.user_info_list[chooser][1]
            print('=============== \nCheck profile of ' + self.current_user +
                  '\n===============')
            get_user_info(self, self.current_user)
        else:
            print('xxxxxxx user info list is empty!!! xxxxxxxxx')
            feed_scanner(self)
        if self.is_selebgram != True and self.is_fake_account != True and self.is_active_user != False:
            if self.is_following != True:
                print('Trying to follow : ' + self.current_user +
                      ' with user ID :' + self.current_id)
                self.follow(self.current_id)
                print('delete ' + self.user_info_list[chooser][0] +
                      ' from user info list')
                del self.user_info_list[chooser]
        else:
            print('delete ' + self.user_info_list[chooser][0] +
                  ' from user info list')
            del self.user_info_list[chooser]

        time.sleep(random.randint(13, 26))
import atexit
import datetime
import itertools
import json
import logging
import random
import signal
import sys

if 'threading' in sys.modules:
    del sys.modules['threading']
import time
import requests
from unfollow_protocol import unfollow_protocol
from userinfo import UserInfo


class InstaBot:
    """
    Instagram bot v 1.1.0
    like_per_day=1000 - How many likes set bot in one day.

    media_max_like=0 - Don't like media (photo or video) if it have more than
    media_max_like likes.

    media_min_like=0 - Don't like media (photo or video) if it have less than
    media_min_like likes.

    tag_list = ['cat', 'car', 'dog'] - Tag list to like.

    max_like_for_one_tag=5 - Like 1 to max_like_for_one_tag times by row.

    log_mod = 0 - Log mod: log_mod = 0 log to console, log_mod = 1 log to file,
    log_mod = 2 no log.

    https://github.com/LevPasha/instabot.py
    """

    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_detail = 'https://www.instagram.com/%s/?__a=1'

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    # If instagram ban you - query return 400 error.
    error_400 = 0
    # If you have 3 400 error in row - looks like you banned.
    error_400_to_ban = 3
    # If InstaBot think you are banned - going to sleep.
    ban_sleep_time = 2 * 60 * 60

    # All counter.
    bot_mode = 0
    like_counter = 0
    follow_counter = 0
    unfollow_counter = 0
    comments_counter = 0
    current_user = 'hajka'
    current_index = 0
    current_id = 'abcds'
    # List of user_id, that bot follow
    bot_follow_list = []
    user_info_list = []
    user_list = []
    ex_user_list = []
    unwanted_username_list = []
    is_checked = False
    is_selebgram = False
    is_fake_account = False
    is_active_user = False
    is_following = False
    is_follower = False
    is_rejected = False
    is_self_checking = False
    is_by_tag = False
    is_follower_number = 0

    self_following = 0
    self_follower = 0

    # Log setting.
    log_file_path = ''
    log_file = 0

    # Other.
    user_id = 0
    media_by_tag = 0
    media_on_feed = []
    media_by_user = []
    login_status = False

    # For new_auto_mod
    next_iteration = {"Like": 0, "Follow": 0, "Unfollow": 0, "Comments": 0}

    def __init__(self,
                 login,
                 password,
                 like_per_day=1000,
                 media_max_like=50,
                 media_min_like=0,
                 follow_per_day=0,
                 follow_time=5 * 60 * 60,
                 unfollow_per_day=0,
                 comment_list=[["this", "the", "your"],
                               ["photo", "picture", "pic", "shot", "snapshot"],
                               ["is", "looks", "feels", "is really"],
                               ["great", "super", "good", "very good", "good",
                                "wow", "WOW", "cool", "GREAT", "magnificent",
                                "magical", "very cool", "stylish", "beautiful",
                                "so beautiful", "so stylish", "so professional",
                                "lovely", "so lovely", "very lovely", "glorious",
                                "so glorious", "very glorious", "adorable",
                                "excellent", "amazing"],[".", "..", "...", "!",
                                                         "!!", "!!!"]],
                 comments_per_day=0,
                 tag_list=['cat', 'car', 'dog'],
                 max_like_for_one_tag=5,
                 unfollow_break_min=15,
                 unfollow_break_max=30,
                 log_mod=0,
                 proxy="",
                 user_blacklist={},
                 tag_blacklist=[],
                 unwanted_username_list=[],
                 unfollow_whitelist=[]):

        self.bot_start = datetime.datetime.now()
        self.unfollow_break_min = unfollow_break_min
        self.unfollow_break_max = unfollow_break_max
        self.user_blacklist = user_blacklist
        self.tag_blacklist = tag_blacklist
        self.unfollow_whitelist = unfollow_whitelist
        self.comment_list = comment_list

        self.time_in_day = 24 * 60 * 60
        # Like
        self.like_per_day = like_per_day
        if self.like_per_day != 0:
            self.like_delay = self.time_in_day / self.like_per_day

        # Follow
        self.follow_time = follow_time
        self.follow_per_day = follow_per_day
        if self.follow_per_day != 0:
            self.follow_delay = self.time_in_day / self.follow_per_day

        # Unfollow
        self.unfollow_per_day = unfollow_per_day
        if self.unfollow_per_day != 0:
            self.unfollow_delay = self.time_in_day / self.unfollow_per_day

        # Comment
        self.comments_per_day = comments_per_day
        if self.comments_per_day != 0:
            self.comments_delay = self.time_in_day / self.comments_per_day

        # Don't like if media have more than n likes.
        self.media_max_like = media_max_like
        # Don't like if media have less than n likes.
        self.media_min_like = media_min_like
        # Auto mod seting:
        # Default list of tag.
        self.tag_list = tag_list
        # Get random tag, from tag_list, and like (1 to n) times.
        self.max_like_for_one_tag = max_like_for_one_tag
        # log_mod 0 to console, 1 to file
        self.log_mod = log_mod
        self.s = requests.Session()
        # if you need proxy make something like this:
        # self.s.proxies = {"https" : "http://proxyip:proxyport"}
        # by @ageorgios
        if proxy != "":
            proxies = {
                'http': 'http://' + proxy,
                'https': 'http://' + proxy,
            }
            self.s.proxies.update(proxies)
        # convert login to lower
        self.user_login = login.lower()
        self.user_password = password
        self.bot_mode = 0
        self.media_by_tag = []
        self.media_on_feed = []
        self.media_by_user = []
        self.unwanted_username_list = unwanted_username_list
        now_time = datetime.datetime.now()
        log_string = 'Instabot v1.1.0 started at %s:\n' % \
                     (now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        self.login()
        self.populate_user_blacklist()
        signal.signal(signal.SIGTERM, self.cleanup)
        atexit.register(self.cleanup)

    def populate_user_blacklist(self):
        for user in self.user_blacklist:
            user_id_url = self.url_user_detail % (user)
            info = self.s.get(user_id_url)

            # prevent error if 'Account of user was deleted or link is invalid
            from json import JSONDecodeError
            try:
                all_data = json.loads(info.text)
            except JSONDecodeError as e:
                self.write_log('Account of user %s was deleted or link is '
                               'invalid' % (user))
            else:
                # prevent exception if user have no media
                id_user = all_data['user']['id']
                # Update the user_name with the user_id
                self.user_blacklist[user] = id_user
                log_string = "Blacklisted user %s added with ID: %s" % (user,
                                                                        id_user)
                self.write_log(log_string)
                time.sleep(5 * random.random())

    def login(self):
        log_string = 'Trying to login as %s...\n' % (self.user_login)
        self.write_log(log_string)
        self.s.cookies.update({
            'sessionid': '',
            'mid': '',
            'ig_pr': '1',
            'ig_vw': '1920',
            'csrftoken': '',
            's_network': '',
            'ds_user_id': ''
        })
        self.login_post = {
            'username': self.user_login,
            'password': self.user_password
        }
        self.s.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': self.accept_language,
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })
        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.s.post(
            self.url_login, data=self.login_post, allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(5 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                ui = UserInfo()
                self.user_id = ui.get_user_id_by_login(self.user_login)
                self.login_status = True
                log_string = '%s login success!' % (self.user_login)
                self.write_log(log_string)
            else:
                self.login_status = False
                self.write_log('Login error! Check your login data!')
        else:
            self.write_log('Login error! Connection error!')

    def logout(self):
        now_time = datetime.datetime.now()
        log_string = 'Logout: likes - %i, follow - %i, unfollow - %i, comments - %i.' % \
                     (self.like_counter, self.follow_counter,
                      self.unfollow_counter, self.comments_counter)
        self.write_log(log_string)
        work_time = datetime.datetime.now() - self.bot_start
        log_string = 'Bot work time: %s' % (work_time)
        self.write_log(log_string)

        try:
            logout_post = {'csrfmiddlewaretoken': self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            self.write_log("Logout success!")
            self.login_status = False
        except:
            self.write_log("Logout error!")

    def cleanup(self, *_):
        # Unfollow all bot follow
        if self.follow_counter >= self.unfollow_counter:
            for f in self.bot_follow_list:
                log_string = "Trying to unfollow: %s" % (f[0])
                self.write_log(log_string)
                self.unfollow_on_cleanup(f[0])
                sleeptime = random.randint(self.unfollow_break_min,
                                           self.unfollow_break_max)
                log_string = "Pausing for %i seconds... %i of %i" % (
                    sleeptime, self.unfollow_counter, self.follow_counter)
                self.write_log(log_string)
                time.sleep(sleeptime)
                self.bot_follow_list.remove(f)

        # Logout
        if (self.login_status):
            self.logout()
        exit(0)

    def get_media_id_by_tag(self, tag):
        """ Get media ID set, by your hashtag """

        if (self.login_status):
            log_string = "Get media id by tag: %s" % (tag)
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = self.url_tag % (tag)
                try:
                    r = self.s.get(url_tag)
                    all_data = json.loads(r.text)

                    self.media_by_tag = list(all_data['tag']['media']['nodes'])
                except:
                    self.media_by_tag = []
                    self.write_log("Except on get_media!")
            else:
                return 0

    def like_all_exist_media(self, media_size=-1, delay=True):
        """ Like all media ID that have self.media_by_tag """

        if self.login_status:
            if self.media_by_tag != 0:
                i = 0
                for d in self.media_by_tag:
                    # Media count by this tag.
                    if media_size > 0 or media_size < 0:
                        media_size -= 1
                        l_c = self.media_by_tag[i]['likes']['count']
                        if ((l_c <= self.media_max_like and
                             l_c >= self.media_min_like) or
                            (self.media_max_like == 0 and
                             l_c >= self.media_min_like) or
                            (self.media_min_like == 0 and
                             l_c <= self.media_max_like) or
                            (self.media_min_like == 0 and
                             self.media_max_like == 0)):
                            for blacklisted_user_name, blacklisted_user_id in self.user_blacklist.items(
                            ):
                                if self.media_by_tag[i]['owner'][
                                        'id'] == blacklisted_user_id:
                                    self.write_log(
                                        "Not liking media owned by blacklisted user: "
                                        + blacklisted_user_name)
                                    return False
                            if self.media_by_tag[i]['owner'][
                                    'id'] == self.user_id:
                                self.write_log(
                                    "Keep calm - It's your own media ;)")
                                return False

                            try:
                                caption = self.media_by_tag[i][
                                    'caption'].encode(
                                        'ascii', errors='ignore')
                                tag_blacklist = set(self.tag_blacklist)
                                if sys.version_info[0] == 3:
                                    tags = {
                                        str.lower(
                                            (tag.decode('ASCII')).strip('#'))
                                        for tag in caption.split()
                                        if (tag.decode('ASCII')
                                            ).startswith("#")
                                    }
                                else:
                                    tags = {
                                        unicode.lower(
                                            (tag.decode('ASCII')).strip('#'))
                                        for tag in caption.split()
                                        if (tag.decode('ASCII')
                                            ).startswith("#")
                                    }

                                if tags.intersection(tag_blacklist):
                                    matching_tags = ', '.join(
                                        tags.intersection(tag_blacklist))
                                    self.write_log(
                                        "Not liking media with blacklisted tag(s): "
                                        + matching_tags)
                                    return False
                            except:
                                self.write_log(
                                    "Couldn't find caption - not liking")
                                return False

                            log_string = "Trying to like media: %s" % \
                                         (self.media_by_tag[i]['id'])
                            self.write_log(log_string)
                            like = self.like(self.media_by_tag[i]['id'])
                            # comment = self.comment(self.media_by_tag[i]['id'], 'Cool!')
                            # follow = self.follow(self.media_by_tag[i]["owner"]["id"])
                            if like != 0:
                                if like.status_code == 200:
                                    # Like, all ok!
                                    self.error_400 = 0
                                    self.like_counter += 1
                                    log_string = "Liked: %s. Like #%i." % \
                                                 (self.media_by_tag[i]['id'],
                                                  self.like_counter)
                                    self.write_log(log_string)
                                elif like.status_code == 400:
                                    log_string = "Not liked: %i" \
                                                 % (like.status_code)
                                    self.write_log(log_string)
                                    # Some error. If repeated - can be ban!
                                    if self.error_400 >= self.error_400_to_ban:
                                        # Look like you banned!
                                        time.sleep(self.ban_sleep_time)
                                    else:
                                        self.error_400 += 1
                                else:
                                    log_string = "Not liked: %i" \
                                                 % (like.status_code)
                                    self.write_log(log_string)
                                    return False
                                    # Some error.
                                i += 1
                                if delay:
                                    time.sleep(self.like_delay * 0.9 +
                                               self.like_delay * 0.2 *
                                               random.random())
                                else:
                                    return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
            else:
                self.write_log("No media to like!")

    def like(self, media_id):
        """ Send http request to like media by ID """
        if self.login_status:
            url_likes = self.url_likes % (media_id)
            try:
                like = self.s.post(url_likes)
                last_liked_media_id = media_id
            except:
                self.write_log("Except on like!")
                like = 0
            return like

    def unlike(self, media_id):
        """ Send http request to unlike media by ID """
        if self.login_status:
            url_unlike = self.url_unlike % (media_id)
            try:
                unlike = self.s.post(url_unlike)
            except:
                self.write_log("Except on unlike!")
                unlike = 0
            return unlike

    def comment(self, media_id, comment_text):
        """ Send http request to comment """
        if self.login_status:
            comment_post = {'comment_text': comment_text}
            url_comment = self.url_comment % (media_id)
            try:
                comment = self.s.post(url_comment, data=comment_post)
                if comment.status_code == 200:
                    self.comments_counter += 1
                    log_string = 'Write: "%s". #%i.' % (comment_text,
                                                        self.comments_counter)
                    self.write_log(log_string)
                return comment
            except:
                self.write_log("Except on comment!")
        return False

    def follow(self, user_id):
        """ Send http request to follow """
        if self.login_status:
            url_follow = self.url_follow % (user_id)
            try:
                follow = self.s.post(url_follow)
                if follow.status_code == 200:
                    self.follow_counter += 1
                    log_string = "Followed: %s #%i." % (user_id,
                                                        self.follow_counter)
                    self.write_log(log_string)
                return follow
            except:
                self.write_log("Except on follow!")
        return False

    def unfollow(self, user_id):
        """ Send http request to unfollow """
        if self.login_status:
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    log_string = "Unfollow: %s #%i." % (user_id,
                                                        self.unfollow_counter)
                    self.write_log(log_string)
                return unfollow
            except:
                self.write_log("Exept on unfollow!")
        return False

    def unfollow_on_cleanup(self, user_id):
        """ Unfollow on cleanup by @rjmayott """
        if self.login_status:
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    log_string = "Unfollow: %s #%i of %i." % (
                        user_id, self.unfollow_counter, self.follow_counter)
                    self.write_log(log_string)
                else:
                    log_string = "Slow Down - Pausing for 5 minutes so we don't get banned!"
                    self.write_log(log_string)
                    time.sleep(300)
                    unfollow = self.s.post(url_unfollow)
                    if unfollow.status_code == 200:
                        self.unfollow_counter += 1
                        log_string = "Unfollow: %s #%i of %i." % (
                            user_id, self.unfollow_counter,
                            self.follow_counter)
                        self.write_log(log_string)
                    else:
                        log_string = "Still no good :( Skipping and pausing for another 5 minutes"
                        self.write_log(log_string)
                        time.sleep(300)
                    return False
                return unfollow
            except:
                log_string = "Except on unfollow... Looks like a network error"
                self.write_log(log_string)
        return False

    def auto_mod(self):
        """ Star loop, that get media ID by your tag list, and like it """
        if self.login_status:
            while True:
                random.shuffle(self.tag_list)
                self.get_media_id_by_tag(random.choice(self.tag_list))
                self.like_all_exist_media(random.randint \
                                              (1, self.max_like_for_one_tag))

    def new_auto_mod(self):
        while True:
            # ------------------- Get media_id -------------------
            if len(self.media_by_tag) == 0:
                self.get_media_id_by_tag(random.choice(self.tag_list))
                self.this_tag_like_count = 0
                self.max_tag_like_count = random.randint(
                    1, self.max_like_for_one_tag)
            # ------------------- Like -------------------
            self.new_auto_mod_like()
            # ------------------- Follow -------------------
            self.new_auto_mod_follow()
            # ------------------- Unfollow -------------------
            self.new_auto_mod_unfollow()
            # ------------------- Comment -------------------
            self.new_auto_mod_comments()
            # Bot iteration in 1 sec
            time.sleep(3)
            # print("Tic!")

    def new_auto_mod_like(self):
        if time.time() > self.next_iteration["Like"] and self.like_per_day != 0 \
                and len(self.media_by_tag) > 0:
            # You have media_id to like:
            if self.like_all_exist_media(media_size=1, delay=False):
                # If like go to sleep:
                self.next_iteration["Like"] = time.time() + \
                                              self.add_time(self.like_delay)
                # Count this tag likes:
                self.this_tag_like_count += 1
                if self.this_tag_like_count >= self.max_tag_like_count:
                    self.media_by_tag = [0]
            # Del first media_id
            del self.media_by_tag[0]

    def new_auto_mod_follow(self):
        if time.time() > self.next_iteration["Follow"] and \
                        self.follow_per_day != 0 and len(self.media_by_tag) > 0:
            if self.media_by_tag[0]["owner"]["id"] == self.user_id:
                self.write_log("Keep calm - It's your own profile ;)")
                return
            log_string = "Trying to follow: %s" % (
                self.media_by_tag[0]["owner"]["id"])
            self.write_log(log_string)

            if self.follow(self.media_by_tag[0]["owner"]["id"]) != False:
                self.bot_follow_list.append(
                    [self.media_by_tag[0]["owner"]["id"], time.time()])
                self.next_iteration["Follow"] = time.time() + \
                                                self.add_time(self.follow_delay)

    def new_auto_mod_unfollow(self):
        if time.time() > self.next_iteration["Unfollow"] and \
                        self.unfollow_per_day != 0 and len(self.bot_follow_list) > 0:
            if self.bot_mode == 0:
                for f in self.bot_follow_list:
                    if time.time() > (f[1] + self.follow_time):
                        log_string = "Trying to unfollow #%i: " % (
                            self.unfollow_counter + 1)
                        self.write_log(log_string)
                        self.auto_unfollow()
                        self.bot_follow_list.remove(f)
                        self.next_iteration["Unfollow"] = time.time() + \
                                                          self.add_time(self.unfollow_delay)
            if self.bot_mode == 1:
                unfollow_protocol(self)

    def new_auto_mod_comments(self):
        if time.time() > self.next_iteration["Comments"] and self.comments_per_day != 0 \
                and len(self.media_by_tag) > 0 \
                and self.check_exisiting_comment(self.media_by_tag[0]['code']) == False:
            comment_text = self.generate_comment()
            log_string = "Trying to comment: %s" % (self.media_by_tag[0]['id'])
            self.write_log(log_string)
            if self.comment(self.media_by_tag[0]['id'], comment_text) != False:
                self.next_iteration["Comments"] = time.time() + \
                                                  self.add_time(self.comments_delay)

    def add_time(self, time):
        """ Make some random for next iteration"""
        return time * 0.9 + time * 0.2 * random.random()

    def generate_comment(self):
        c_list = list(itertools.product(*self.comment_list))

        repl = [("  ", " "), (" .", "."), (" !", "!")]
        res = " ".join(random.choice(c_list))
        for s, r in repl:
            res = res.replace(s, r)
        return res.capitalize()

    def check_exisiting_comment(self, media_code):
        url_check = self.url_media_detail % (media_code)
        check_comment = self.s.get(url_check)
        all_data = json.loads(check_comment.text)
        if all_data['graphql']['shortcode_media']['owner']['id'] == self.user_id:
                self.write_log("Keep calm - It's your own media ;)")
                # Del media to don't loop on it
                del self.media_by_tag[0]
                return True
        comment_list = list(all_data['graphql']['shortcode_media']['edge_media_to_comment']['edges'])
        for d in comment_list:
            if d['node']['owner']['id'] == self.user_id:
                self.write_log("Keep calm - Media already commented ;)")
                # Del media to don't loop on it
                del self.media_by_tag[0]
                return True
        return False

    def auto_unfollow(self):
        chooser = 1
        current_user = 'abcd'
        current_id = '12345'
        checking = True
        self.media_on_feed = []
        if len(self.media_on_feed) < 1:
            self.get_media_id_recent_feed()
        if len(self.media_on_feed) != 0:
            chooser = random.randint(0, len(self.media_on_feed) - 1)
            current_id = self.media_on_feed[chooser]['node']["owner"]["id"]
            current_user = self.media_on_feed[chooser]['node']["owner"][
                "username"]

            while checking:
                for wluser in self.unfollow_whitelist:
                    if wluser == current_user:
                        chooser = random.randint(0,
                                                 len(self.media_on_feed) - 1)
                        current_id = self.media_on_feed[chooser]['node'][
                            "owner"]["id"]
                        current_user = self.media_on_feed[chooser]['node'][
                            "owner"]["username"]
                        log_string = (
                            "found whitelist user, starting search again")
                        self.write_log(log_string)
                        break
                else:
                    checking = False

        if self.login_status:
            now_time = datetime.datetime.now()
            log_string = "%s : Get user info \n%s" % (
                self.user_login, now_time.strftime("%d.%m.%Y %H:%M"))
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = self.url_user_detail % (current_user)
                try:
                    r = self.s.get(url_tag)
                    all_data = json.loads(r.text)

                    self.user_info = all_data['user']
                    i = 0
                    log_string = "Checking user info.."
                    self.write_log(log_string)

                    while i < 1:
                        follows = self.user_info['follows']['count']
                        follower = self.user_info['followed_by']['count']
                        media = self.user_info['media']['count']
                        follow_viewer = self.user_info['follows_viewer']
                        followed_by_viewer = self.user_info[
                            'followed_by_viewer']
                        requested_by_viewer = self.user_info[
                            'requested_by_viewer']
                        has_requested_viewer = self.user_info[
                            'has_requested_viewer']
                        log_string = "Follower : %i" % (follower)
                        self.write_log(log_string)
                        log_string = "Following : %s" % (follows)
                        self.write_log(log_string)
                        log_string = "Media : %i" % (media)
                        self.write_log(log_string)
                        if follower / follows > 2:
                            self.is_selebgram = True
                            self.is_fake_account = False
                            print('   >>>This is probably Selebgram account')
                        elif follows / follower > 2:
                            self.is_fake_account = True
                            self.is_selebgram = False
                            print('   >>>This is probably Fake account')
                        else:
                            self.is_selebgram = False
                            self.is_fake_account = False
                            print('   >>>This is a normal account')

                        if follows / media < 10 and follower / media < 10:
                            self.is_active_user = True
                            print('   >>>This user is active')
                        else:
                            self.is_active_user = False
                            print('   >>>This user is passive')

                        if follow_viewer or has_requested_viewer:
                            self.is_follower = True
                            print("   >>>This account is following you")
                        else:
                            self.is_follower = False
                            print('   >>>This account is NOT following you')

                        if followed_by_viewer or requested_by_viewer:
                            self.is_following = True
                            print('   >>>You are following this account')

                        else:
                            self.is_following = False
                            print('   >>>You are NOT following this account')
                        i += 1

                except:
                    media_on_feed = []
                    self.write_log("Except on get_info!")
                    time.sleep(20)
                    return 0
            else:
                return 0

            if self.is_selebgram is not False or self.is_fake_account is not False or self.is_active_user is not True or self.is_follower is not True:
                print(current_user)
                self.unfollow(current_id)
                try:
                    del self.media_on_feed[chooser]
                except:
                    self.media_on_feed = []
            self.media_on_feed = []

    def get_media_id_recent_feed(self):
        if self.login_status:
            now_time = datetime.datetime.now()
            log_string = "%s : Get media id on recent feed" % (self.user_login)
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = 'https://www.instagram.com/?__a=1'
                try:
                    r = self.s.get(url_tag)
                    all_data = json.loads(r.text)

                    self.media_on_feed = list(
                        all_data['graphql']['user']['edge_web_feed_timeline'][
                            'edges'])

                    log_string = "Media in recent feed = %i" % (
                        len(self.media_on_feed))
                    self.write_log(log_string)
                except:
                    self.media_on_feed = []
                    self.write_log("Except on get_media!")
                    time.sleep(20)
                    return 0
            else:
                return 0

    def write_log(self, log_text):
        """ Write log by print() or logger """

        if self.log_mod == 0:
            try:
                print(log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")
        elif self.log_mod == 1:
            # Create log_file if not exist.
            if self.log_file == 0:
                self.log_file = 1
                now_time = datetime.datetime.now()
                self.log_full_path = '%s%s_%s.log' % (
                    self.log_file_path, self.user_login,
                    now_time.strftime("%d.%m.%Y_%H:%M"))
                formatter = logging.Formatter('%(asctime)s - %(name)s '
                                              '- %(message)s')
                self.logger = logging.getLogger(self.user_login)
                self.hdrl = logging.FileHandler(self.log_full_path, mode='w')
                self.hdrl.setFormatter(formatter)
                self.logger.setLevel(level=logging.INFO)
                self.logger.addHandler(self.hdrl)
            # Log to log file.
            try:
                self.logger.info(log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")
import random
import time

from likers_protocol import likers_protocol
from new_auto_mod_unfollow2 import new_auto_mod_unfollow2
from user_feed import get_media_id_user_feed


def likers_graber_protocol(self):
    limit = random.randint(1, 3)
    counterx = 0
    self.is_checked = False
    self.is_rejected = False
    while counterx <= limit:
        # ------------------- Get media_id -------------------
        if len(self.media_by_user) == 0:
            self.is_checked = False
            self.is_rejected = False
            get_media_id_user_feed(self)
        # ------------------- Like -------------------
        if self.is_rejected is not False:
            self.is_checked = False
            new_auto_mod_unfollow2(self)
            return 0
        likers_protocol(self)
        time.sleep(random.randint(13, 35))
        counterx += 1
import random

from post_page import get_user_id_post_page
from username_checker import username_checker


def likers_protocol(self):
    if len(self.media_by_user) > 0:
        # You have media_id to like:
        self.current_index = random.randint(0, len(self.media_by_user) - 1)
        log_string = "Current Index = %i of %i medias" % (
            self.current_index, len(self.media_by_user))
        self.write_log(log_string)

        if self.media_by_user[self.
                              current_index]["likes"]["count"] >= 10 and self.media_by_user[self.
                                                                                            current_index]["likes"]["count"] < 100:
            get_user_id_post_page(
                self, self.media_by_user[self.current_index]["code"])
            username_checker(self)
        del self.media_by_user[self.current_index]
import random

from new_auto_mod_likeall import new_like_all_exist_media


def new_auto_mod_like2(self):
    if len(self.media_by_user) > 0:
        # You have media_id to like:
        self.current_index = random.randint(0, len(self.media_by_user) - 1)
        log_string = "Current Index = %i of %i medias" % (
            self.current_index, len(self.media_by_user))
        self.write_log(log_string)

        new_like_all_exist_media(self)
        # Del first media_id
        del self.media_by_user[self.current_index]
def new_like_all_exist_media(self):
    i = self.current_index
    # Media count by this user.
    l_c = self.media_by_user[i]['likes']['count']
    if l_c <= self.media_max_like and l_c >= self.media_min_like:
        log_string = "Trying to like media: %s" %\
                      (self.media_by_user[i]['id'])
        self.write_log(log_string)
        like = self.like(self.media_by_user[i]['id'])
        if like != 0:
            if like.status_code == 200:
                log_string = "Liked: %s. Likes: #%i." %\
                              (self.media_by_user[i]['id'],
                               self.media_by_user[i]['likes']['count'])
                self.write_log(log_string)
            elif like.status_code == 400:
                log_string = "Not liked: %i" \
                              % (like.status_code)
                self.write_log(log_string)
            else:
                log_string = "Not liked: %i" \
                              % (like.status_code)
                self.write_log(log_string)
                return False
        else:
            return False
    else:
        print('Too much liker for this media!!! LC = %i' % (l_c))
        return True
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from new_unfollow import new_unfollow


def new_auto_mod_unfollow2(self):
    log_string = "Trying to unfollow: %s" % (self.current_user)
    self.write_log(log_string)
    new_unfollow(self, self.current_id, self.current_user)


def new_unfollow(self, user_id, user_name):
    """ Send http request to unfollow """
    url_unfollow = self.url_unfollow % (user_id)
    try:
        unfollow = self.s.post(url_unfollow)
        if unfollow.status_code == 200:
            self.unfollow_counter += 1
            log_string = "Unfollow: %s #%i." % (user_name,
                                                self.unfollow_counter)
            self.write_log(log_string)
        return unfollow
    except:
        self.write_log("Exept on unfollow!")
        return False
import json
import time


def get_user_id_post_page(self, code):
    if self.login_status:
        log_string = 'Get user id on post page'
        self.write_log(log_string)
        url = 'https://www.instagram.com/p/%s/?__a=1' % (code)
        try:
            r = self.s.get(url)
            all_data = json.loads(r.text)

            self.user_list = list(all_data['media']['likes']['nodes'])
            log_string = "User likes this post = %i" % (
                all_data['media']['likes']['count'])
            self.write_log(log_string)
        except:
            self.media_on_feed = []
            self.write_log("Except on get user list!!!!")
            time.sleep(10)
            return 0
    else:
        return 0
import datetime
import json
import time


def get_media_id_recent_feed(self):
    if self.login_status:
        now_time = datetime.datetime.now()
        log_string = "%s : Get media id on recent feed \n %s" % (
            self.user_login, now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        url = 'https://www.instagram.com/?__a=1'
        try:
            r = self.s.get(url)
            all_data = json.loads(r.text)

            self.media_on_feed = list(all_data['graphql']['user']['edge_web_feed_timeline']['edges'])
            log_string = "Media in recent feed = %i" % (
                len(self.media_on_feed))
            self.write_log(log_string)
        except:
            self.media_on_feed = []
            self.write_log('Except on get media!!')
            time.sleep(20)
            return 0
    else:
        return 0

import random
import time

from follow_protocol import follow_protocol
from new_auto_mod_unfollow2 import new_auto_mod_unfollow2
from recent_feed import get_media_id_recent_feed
from user_feed_protocol import user_feed_protocol


def unfollow_protocol(self):
    limit = random.randint(10, 22) + 1
    while self.unfollow_counter <= limit:
        get_media_id_recent_feed(self)
        if len(self.media_on_feed) == 0:
            self.follow_counter = 0
            follow_protocol(self)
        if len(self.media_on_feed) != 0 and self.is_follower_number < 5:
            chooser = random.randint(0, len(self.media_on_feed) - 1)
            self.current_user = self.media_on_feed[chooser]["node"]["owner"][
                "username"]
            self.current_id = self.media_on_feed[chooser]["node"]["owner"][
                "id"]
            if self.bot_mode == 2:
                new_auto_mod_unfollow2(self)
                time.sleep(30)
                return
            user_feed_protocol(self)
            self.like_counter = 0
            self.media_by_user = []
            if self.is_selebgram is not False or self.is_fake_account is not False or self.is_active_user is not True or self.is_follower is not True:
                new_auto_mod_unfollow2(self)
                try:
                    del self.media_on_feed[chooser]
                except:
                    self.media_on_feed = []
        else:
            follow_protocol(self)
            self.is_follower_number = 0
            time.sleep(13 + 5)
import random
import time

from instabot import InstaBot
from userinfo import UserInfo

#use userinfo
ui = UserInfo()
ui.search_user(user_name="login")

#take following
ui.get_following()
following = ui.following

#take followers
ui.get_followers()
followers = ui.followers

#favorite id list
favorites = ['111', '222', '333']

#some lists
newlist = []
endlist = []
followerslist = []

#get following id
for item in following:
    newlist.append(item['id'])

#get followers id
for item in followers:
    followerslist.append(item['id'])

#create final list with followers
endlist = set.difference(set(newlist), set(favorites), set(followerslist))

#create final list without followers
'''
endlist = set.difference(set(newlist), set(favorites))
'''

#use instabot
bot = InstaBot('login', 'password')

print('Number of unnecessary subscriptions:', len(endlist), '\n')

for items in endlist:
    rnd = random.randint(1, 16)
    bot.unfollow(items)
    print('Wait', 30 + rnd, 'sec')
    time.sleep(30 + rnd)

print('All done.')
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
import time

from user_info import get_user_info


def get_media_id_user_feed(self):
    if self.login_status:
        if self.is_by_tag != True:
            log_string = "======> Get media id by user: %s <======" % (
                self.current_user)
            if self.is_checked != True:
                get_user_info(self, self.current_user)
            if self.is_fake_account != True and self.is_active_user != False and self.is_selebgram != True or self.is_by_tag != False:
                url = 'https://www.instagram.com/%s/?__a=1' % (self.current_user)
        else:
            log_string = "======> Get media id by Tag <======"
            url = 'https://www.instagram.com/explore/tags/%s/?__a=1' % (
                random.choice(self.tag_list))
        self.write_log(log_string)

        if self.login_status == 1 and self.is_fake_account != True and self.is_active_user != False and self.is_selebgram != True or self.is_by_tag != False:
            try:
                r = self.s.get(url)
                all_data = json.loads(r.text)

                if self.is_by_tag != True:
                    self.media_by_user = list(all_data['user']['media']['nodes'])
                else:
                    self.media_by_user = list(all_data['tag']['media']['nodes'])
                log_string = "Get media by user success!"
                self.write_log(log_string)
            except:
                self.media_by_user = []
                self.write_log("XXXXXXX Except on get_media! XXXXXXX")
                time.sleep(60)
                return 0
        else:
            log_string = "Reject this account \n=================== \nReason : \n   Is Selebgram : %s \n   Is Fake Account : %s \n   Is Active User : %s \n" % (
                self.is_selebgram, self.is_fake_account, self.is_active_user)
            self.write_log(log_string)
            self.is_rejected = True
            self.media_by_user = []
            self.media_on_feed = []
            return 0
import random
import time

from new_auto_mod_like2 import new_auto_mod_like2
from user_feed import get_media_id_user_feed


def user_feed_protocol(self):
    #To limit how many photos to scan
    limit = random.randint(4, 6)
    counterz = 0
    self.is_checked = False
    self.is_rejected = False
    while counterz <= limit:
        # ------------------- Get media_id -------------------
        if len(self.media_by_user) is 0:
            get_media_id_user_feed(self)
            # ------------------- Like -------------------
        if self.is_rejected is not False:
            return 0
        if self.is_follower is not False:
            print(
                "@@@@@@@@@@@@@@ This is your follower B****h!!! @@@@@@@@@@@@@")
            self.is_follower_number += 1
            time.sleep(5)
            return
        new_auto_mod_like2(self)
        counterz += 1
        time.sleep(3 * 15)
import datetime
import json
import random
import time


def get_user_info(self, username):
    if self.login_status:
        now_time = datetime.datetime.now()
        log_string = "%s : Get user info \n%s" % (
            self.user_login, now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)
        if self.login_status == 1:
            url = 'https://www.instagram.com/%s/?__a=1' % (username)
            try:
                r = self.s.get(url)

                user_info = json.loads(r.text)

                log_string = "Checking user info.."
                self.write_log(log_string)

                follows = user_info['user']['follows']['count']
                follower = user_info['user']['followed_by']['count']
                if self.is_self_checking is not False:
                    self.self_following = follows
                    self.self_follower = follower
                    self.is_self_checking = False
                    self.is_checked = True
                    return 0
                media = user_info['user']['media']['count']
                follow_viewer = user_info['user']['follows_viewer']
                followed_by_viewer = user_info['user']['followed_by_viewer']
                requested_by_viewer = user_info['user'][
                    'requested_by_viewer']
                has_requested_viewer = user_info['user'][
                    'has_requested_viewer']
                log_string = "Follower : %i" % (follower)
                self.write_log(log_string)
                log_string = "Following : %s" % (follows)
                self.write_log(log_string)
                log_string = "Media : %i" % (media)
                self.write_log(log_string)

                if follower / follows > 2:
                    self.is_selebgram = True
                    self.is_fake_account = False
                    print('   >>>This is probably Selebgram account')
                elif follows / follower > 2:
                    self.is_fake_account = True
                    self.is_selebgram = False
                    print('   >>>This is probably Fake account')
                else:
                    self.is_selebgram = False
                    self.is_fake_account = False
                    print('   >>>This is a normal account')

                if follows / media < 10 and follower / media < 10:
                    self.is_active_user = True
                    print('   >>>This user is active')
                else:
                    self.is_active_user = False
                    print('   >>>This user is passive')

                if follow_viewer or has_requested_viewer:
                    self.is_follower = True
                    print("   >>>This account is following you")
                else:
                    self.is_follower = False
                    print('   >>>This account is NOT following you')

                if followed_by_viewer or requested_by_viewer:
                    self.is_following = True
                    print('   >>>You are following this account')
                else:
                    self.is_following = False
                    print('   >>>You are NOT following this account')
                    self.is_checked = True
            except:
                self.media_on_feed = []
                self.write_log("Except on get_info!")
                time.sleep(20)
                return 0
        else:
            return 0

import json

import requests


class UserInfo:
    '''
    This class try to take some user info (following, followers, etc.)
    '''
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")

    url_user_info = "https://www.instagram.com/%s/?__a=1"
    url_list = {
        "ink361": {
            "main": "http://ink361.com/",
            "user": "http://ink361.com/app/users/%s",
            "search_name": "https://data.ink361.com/v1/users/search?q=%s",
            "search_id": "https://data.ink361.com/v1/users/ig-%s",
            "followers": "https://data.ink361.com/v1/users/ig-%s/followed-by",
            "following": "https://data.ink361.com/v1/users/ig-%s/follows",
            "stat": "http://ink361.com/app/users/ig-%s/%s/stats"
        }
    }

    def __init__(self, info_aggregator="ink361"):
        self.i_a = info_aggregator
        self.hello()

    def hello(self):
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': self.user_agent})
        main = self.s.get(self.url_list[self.i_a]["main"])
        if main.status_code == 200:
            return True
        return False

    def get_user_id_by_login(self, user_name):
        url_info = self.url_user_info % (user_name)
        info = self.s.get(url_info)
        all_data = json.loads(info.text)
        id_user = all_data['user']['id']
        return id_user

    def search_user(self, user_id=None, user_name=None):
        '''
        Search user_id or user_name, if you don't have it.
        '''
        self.user_id = user_id or False
        self.user_name = user_name or False

        if not self.user_id and not self.user_name:
            # you have nothing
            return False
        elif self.user_id:
            # you have just id
            search_url = self.url_list[self.i_a]["search_id"] % self.user_id
        elif self.user_name:
            # you have just name
            search_url = self.url_list[self.i_a][
                "search_name"] % self.user_name
        else:
            # you have id and name
            return True

        search = self.s.get(search_url)

        if search.status_code == 200:
            r = json.loads(search.text)
            if self.user_id:
                # you have just id
                self.user_name = r["data"]["username"]
            else:
                for u in r["data"]:
                    if u["username"] == self.user_name:
                        t = u["id"].split("-")
                        self.user_id = t[1]
                # you have just name
            return True
        return False

    def get_followers(self, limit=-1):
        self.followers = None
        self.followers = []
        if self.user_id:
            next_url = self.url_list[self.i_a]["followers"] % self.user_id
            while True:
                followers = self.s.get(next_url)
                r = json.loads(followers.text)
                for u in r["data"]:
                    if limit > 0 or limit < 0:
                        self.followers.append({
                            "username": u["username"],
                            #"profile_picture": u["profile_picture"],
                            "id": u["id"].split("-")[1],
                            #"full_name": u["full_name"]
                        })
                        limit -= 1
                    else:
                        return True
                if r["pagination"]["next_url"]:
                    # have more data
                    next_url = r["pagination"]["next_url"]
                else:
                    # end of data
                    return True
        return False

    def get_following(self, limit=-1):
        self.following = None
        self.following = []
        if self.user_id:
            next_url = self.url_list[self.i_a]["following"] % self.user_id
            while True:
                following = self.s.get(next_url)
                r = json.loads(following.text)
                for u in r["data"]:
                    if limit > 0 or limit < 0:
                        self.following.append({
                            "username": u["username"],
                            #"profile_picture": u["profile_picture"],
                            "id": u["id"].split("-")[1],
                            #"full_name": u["full_name"]
                        })
                        limit -= 1
                    else:
                        return True
                if r["pagination"]["next_url"]:
                    # have more data
                    next_url = r["pagination"]["next_url"]
                else:
                    # end of data
                    return True
        return False

    def get_stat(self, limit):
        # todo
        return False


'''
# example
ui = UserInfo()
# search by user_name:
ui.search_user(user_name="danbilzerian")
# or if you know user_id ui.search_user(user_id="50417061")
print(ui.user_name)
print(ui.user_id)

# get following list with no limit
ui.get_following()
print(ui.following)

# get followers list with limit 10
ui.get_followers(limit=10)
print(ui.followers)
'''
def username_checker(self):
    chooser = 0
    while len(self.user_list) > 0 and chooser < len(self.user_list):
        self.current_user = self.user_list[chooser]["user"]["username"]
        self.current_id = self.user_list[chooser]["user"]["id"]
        for index in range(len(self.unwanted_username_list)):
            if self.unwanted_username_list[index] in self.current_user:
                print('Username = ' + self.current_user + '\n      ID = ' +
                      self.current_id + '      <<< rejected ' +
                      self.unwanted_username_list[index] + ' is found!!!')
                break
        else:
            for index in range(len(self.user_info_list)):
                if self.current_user in self.user_info_list[index][0]:
                    print(
                        'Username = ' + self.current_user + '\n      ID = ' +
                        self.current_id +
                        '      <<< rejected this user is already in user info list!!!'
                    )
                    break
            else:
                print('Username = ' + self.current_user + '\n      ID = ' +
                      self.current_id + '      <<< added to user info list')
                self.user_info_list.append(
                    [self.current_user, self.current_id])
        chooser += 1
    log_string = "\nSize of user info list : %i Size of ex user list : %i \n" % (
        len(self.user_info_list), len(self.ex_user_list))
    self.write_log(log_string)
