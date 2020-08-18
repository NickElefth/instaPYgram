from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re
import creds


class HomePage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.implicitly_wait(6)
        self.browser.get('https://www.instagram.com/')

    def go_to_login_page(self):
        sleep(2)
        return LoginPage(self.browser)


class LoginPage:
    def __init__(self, browser):
        self.browser = browser

    def login(self, username, password):
        username_input = self.browser.find_element_by_css_selector(
            "input[name='username']")
        password_input = self.browser.find_element_by_css_selector(
            "input[name='password']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = self.browser.find_element_by_xpath(
            "//button[@type='submit']")
        login_button.click()
        sleep(5)
        self.skip_login_popup_windows()

    def skip_login_popup_windows(self):
        self.browser.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]").click()
        sleep(2)
        try:
            self.browser.find_element_by_xpath(
                "//button[contains(text(), 'Not Now')]").click()
        except Exception:
            pass  # if there isn't a second Not Now popup do not throw an exception


class HashTagLikes():
    def __init__(self, username, browser):
        self.username = username
        self.browser = browser
        self.new_likes = 0
        self.new_comments = 0
        self.new_followed = []
        self.pics_already_liked = []

    def hashtag_farming(self, hashtag, comments_list):
        """
        Method used to like, comment and follow pictures posted using given hashtags
        """
        self.browser.get(
            "https://www.instagram.com/explore/tags/{0}/".format(hashtag))
        sleep(2)
        # Scrolling down to load images
        for i in range(2):
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
        # searching for picture links
        pic_hrefs_pattern = re.compile(
            "^https:\/\/www\.instagram\.com\/p\/.+\/")  # Only select picture links
        hrefs = self.browser.find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute(
            'href') for elem in hrefs if pic_hrefs_pattern.match(elem.get_attribute('href'))]
        print("{0} photos found: {1}".format(hashtag, len(pic_hrefs)))
        for pic_href in pic_hrefs:
            #  Multiple hashtags might lead to revisiting the same pic
            if pic_href in self.pics_already_liked:
                continue
            self.pics_already_liked.append(pic_href)
            sleep(2)
            self.browser.get(pic_href)
            sleep(3)
            # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") // Not needed to scroll at this point of time
            try:
                self.like_photo()
                self.comment_photo(comments_list)
                self.follow_user(pic_href)
            except Exception as ex:
                print("Exception thrown: {0}".format(ex))
                sleep(5)

    def like_photo(self):
        # like button
        self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
        sleep(randint(3, 10))  # Instagram limit of 200 likes per hour
        self.new_likes += 1

    def comment_photo(self, comments_list):
        # click comment button
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[2]/button').click()
        comment_section = self.browser.find_element_by_class_name("Ypffh")
        comment_section.click()
        comment_section.send_keys(
            comments_list[randint(0, len(comments_list)-1)])
        sleep(2)
        self.browser.find_element_by_xpath(
            "//button[contains(text(), 'Post')]").click()
        sleep(randint(3, 10))
        self.new_comments += 1

    def follow_user(self, pic_href):
        # follow button
        try:
            following = self.browser.find_element_by_xpath(
                "//button[contains(text(), 'Following')]")
        except NoSuchElementException as ex:
            following = ""
        if not following:
            # username xpath
            prospect_username = self.browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a")
            prospect_username_link = prospect_username.get_attribute('href')
            # check for number of followers
            self.browser.get(prospect_username_link)
            sleep(2)
            worth_follow = self.check_number_followers()
            if worth_follow:
                self.browser.find_element_by_xpath(
                    "//button[contains(text(), 'Follow')]").click()
                self.new_followed.append(prospect_username_link)
        sleep(randint(3, 10))

    def check_number_followers(self):
        num_of_followers = self.browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        num_of_followers = num_of_followers.get_attribute('title')
        num_of_followers = int(num_of_followers.replace(',', ''))
        if num_of_followers < 1500:
            return True
        return False


class InitializeInstaBot():
    def __init__(self, username, password):
        self.browser = webdriver.Firefox()
        self.username = username
        self.session = HomePage(self.browser)
        self.session = self.session.go_to_login_page()
        self.session = self.session.login(
            creds.getUsername(), creds.getPassword())
        sleep(3)
        self.hash_tag_settings = HashTagLikes(username=self.username,
                                              browser=self.browser)

    def hashtag_automation(self, hashtags, comments_list):
        for hashtag in hashtags:
            print(hashtag)
            self.hash_tag_settings.hashtag_farming(hashtag, comments_list)
        print("Hashtag automated session has ended:\n New Likes: {0}\n New Comments: {1},\n New Following: {2},\n List of new Following: \n{3}".format(self.hash_tag_settings.new_likes,
                                                                                                                                                       self.hash_tag_settings.new_comments,
                                                                                                                                                       len(
                                                                                                                                                           self.hash_tag_settings.new_followed),
                                                                                                                                                       self.hash_tag_settings.new_followed))

    def get_to_homepage(self):
        self.browser.get('https://www.instagram.com/')

    def get_to_my_profile(self):
        self.browser.find_element_by_xpath(
            "//a[contains(@href, '/{0}')]".format(self.username)).click()

    def get_my_followers_list(self):
        self.get_to_my_profile()
        return self._get_followers_list()

    def unfollow_unfollowers(self):
        not_followers = self.get_unfollowers()
        for href in not_followers.values():
            try:
                self.browser.get(href)
                sleep(2)
                # Unfollow button
                self.browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button').click()
                sleep(2)
                self.browser.find_element_by_xpath(
                    "/html/body/div[4]/div/div/div/div[3]/button[1]").click()
                print("unfollowed: {0}".format(href))
            except Exception as ex:
                print(
                    "## Couldnt unfollow: {0} \n Exception: {1}".format(href, ex))
        sleep(5)

    def get_unfollowers(self):
        self.get_to_homepage()
        sleep(2)
        self.get_to_my_profile()
        sleep(2)
        followers = self._get_followers_list()
        following = self._get_following_list()
        not_followers = {user: href for user,
                         href in following.items() if user not in followers}
        self._print_unfollowers(not_followers)
        return not_followers

    def _print_unfollowers(self, unfollowers):
        print("Unfollowers: \n")
        for unfollower in unfollowers:
            print("* {0}".format(unfollower))

    def _get_followers_list(self):
        self.browser.find_element_by_xpath("//a[contains(@href, '/followers')]")\
            .click()
        followers = self._get_names()
        return followers

    def _get_following_list(self):
        self.browser.find_element_by_xpath("//a[contains(@href, '/following')]")\
            .click()
        following = self._get_names()
        return following

    def _get_names(self):
        sleep(1)
        # sugggestions = self.browser.find_element_by_xpath("//h4[contains(text(), Suggestions)]")
        # self.browser.execute_script('arguments[0].scrollIntoView()', sugggestions)
        # sleep(1)
        scroll_box = self.browser.find_element_by_xpath(
            "/html/body/div[4]/div/div/div[2]")
        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            sleep(1)
            height = self.browser.execute_script("""
               arguments[0].scrollTo(0, arguments[0].scrollHeight);
               return arguments[0].scrollHeight;
            """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        # { username : href }
        names_hrefs_dict = {name.text: name.get_attribute(
            'href') for name in links if name.text != ''}
        # close button
        self.browser.find_element_by_xpath(
            '/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        return names_hrefs_dict

    def end_session(self):
        self.browser.close()
