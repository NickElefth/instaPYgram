from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from dataLogger import *
import re
import creds
import json

MAX_NUMBER_OF_FOLLOWERS = 1500


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
        sleep(6)
        login_button.click()

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
    def __init__(self, username, browser, only_likes):
        self.username = username
        self.browser = browser
        self.new_likes = 0
        self.new_comments = 0
        self.new_followed = []
        self.pics_already_liked = []
        self.only_likes = only_likes

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
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            sleep(2)
        # searching for picture links
        # Only select picture links pylint: disable=anomalous-backslash-in-string
        pic_hrefs_pattern = re.compile(
            "^https:\/\/www\.instagram\.com\/p\/.+\/")
        hrefs = self.browser.find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute(
            'href') for elem in hrefs if pic_hrefs_pattern.match(elem.get_attribute('href'))]
        print("{0} photos found: {1}".format(hashtag, len(pic_hrefs)))
        logged_refs = gather_logged_hrefs()
        for iteration, pic_href in enumerate(pic_hrefs):
            print(
                "Currently on iteration {0}/{1}".format(iteration + 1, len(pic_hrefs)))
            #  Multiple hashtags might lead to revisiting the same pic
            if pic_href in self.pics_already_liked:
                continue
            if pic_href in logged_refs:
                continue  # if we liked/commented/followed pic in the last 24 hours skip it
            self.pics_already_liked.append(pic_href)
            sleep(2)
            try:
                self.browser.get(pic_href)
            except selenium.common.exceptions.TimeoutException as ex:
                print("Timeout Exception on pic href {0} Error: {1}".format(
                    pic_href, ex))
                continue
            sleep(3)
            # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") // Not needed to scroll at this point of time
            try:
                self._like_photo()
                if not self.only_likes:  # Option to only like pictures and ignore comments/follows
                    self._comment_photo(comments_list)
                    self._follow_user(pic_href)
            except Exception as ex:
                print("Exception thrown: {0}".format(ex))
                sleep(5)
        # append links to the json instagram logger file
        log_instagram_hrefs(pic_hrefs)

    def _like_photo(self):
        # like button
        self.browser.find_element_by_css_selector(
            #'/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
            '.fr66n > button:nth-child(1)').click()
        sleep(randint(3, 10))  # Instagram limit of 200 likes per hour
        self.new_likes += 1

    def _comment_photo(self, comments_list):
        # click comment button
        self.browser.find_element_by_css_selector(
            # '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[2]/button').click()
            '._15y0l > button:nth-child(1)').click()
        comment_section = self.browser.find_element_by_class_name("Ypffh")
        comment_section.click()
        comment_section.send_keys(
            comments_list[randint(0, len(comments_list)-1)])
        sleep(2)
        self.browser.find_element_by_xpath(
            "//button[contains(text(), 'Post')]").click()
        sleep(randint(3, 10))
        self.new_comments += 1

    def _follow_user(self, pic_href):
        # follow button
        try:
            following = self.browser.find_element_by_xpath(
                "//button[contains(text(), 'Following')]")
        except NoSuchElementException as ex:
            following = ""
        if not following:
            # username xpath
            prospect_username = self.browser.find_element_by_css_selector(
                # "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a")
                ".e1e1d > span:nth-child(1) > a:nth-child(1)")
            prospect_username_link = prospect_username.get_attribute('href')
            # check for number of followers
            self.browser.get(prospect_username_link)
            sleep(2)
            worth_follow = self._check_number_followers()
            if worth_follow:
                self.browser.find_element_by_xpath(
                    "//button[contains(text(), 'Follow')]").click()
                self.new_followed.append(prospect_username_link)
        sleep(randint(3, 10))

    def _check_number_followers(self):
        num_of_followers = self.browser.find_element_by_css_selector(
            "html.js.logged-in.client-root.js-focus-visible.sDN5V body div#react-root section._9eogI.E3X2T main.SCxLW.o64aR div.v9tJq.AAaSh.VfzDr header.vtbgv section.zwlfE ul.k9GMp li.Y8-fY a.-nal3")
        num_of_followers = num_of_followers.get_attribute('title')
        num_of_followers = int(num_of_followers.replace(',', ''))
        if num_of_followers < MAX_NUMBER_OF_FOLLOWERS:
            return True
        return False


class InstaBot():
    def __init__(self, username, password, only_likes=False):
        self.browser = webdriver.Firefox()
        self.username = username
        self.session = HomePage(self.browser)
        self.session = self.session.go_to_login_page()
        self.session = self.session.login(
            creds.getUsername(), creds.getPassword())
        sleep(3)
        self.hash_tag_settings = HashTagLikes(username=self.username,
                                              browser=self.browser,
                                              only_likes=only_likes)

    def hashtag_automation(self, hashtags, comments_list):
        current_followers = self.get_my_followers_number()
        print("followers {}".format(current_followers))

        current_following = self.get_my_following_number()
        print("following {}".format(current_following))

        for hashtag in hashtags:
            print(hashtag)
            self.hash_tag_settings.hashtag_farming(hashtag, comments_list)
        log_instagram_stats(self.hash_tag_settings.new_likes,
                            self.hash_tag_settings.new_comments,
                            len(self.hash_tag_settings.new_followed),
                            hashtags, comments_list,
                            current_followers,
                            current_following)  # pylint: disable=too-many-arguments
        print("Hashtag automated session has ended:\n New Likes: {0}\n New Comments: {1},\n New Following: {2},\n List of new Following: \n{3}".format(self.hash_tag_settings.new_likes,
                                                                                                                                                       self.hash_tag_settings.new_comments,
                                                                                                                                                       len(
                                                                                                                                                           self.hash_tag_settings.new_followed),
                                                                                                                                                       self.hash_tag_settings.new_followed))

    def get_to_homepage(self):
        self.browser.get('https://www.instagram.com/')

    def get_to_my_profile(self):
        self.get_to_homepage()
        sleep(3)
        self.browser.find_element_by_xpath(
            "//a[contains(@href, '/{0}')]".format(self.username)).click()

    def get_my_followers_list(self):
        self.get_to_my_profile()
        return self._get_followers_list()

    def get_my_followers_number(self):
        """
        Get number of followers
        """
        self.get_to_my_profile()
        sleep(4)
        num_of_followers = self.browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        return self._cleanup_follow_number(num_of_followers)

    def get_my_following_number(self):
        """
        Get number of following
        """
        self.get_to_my_profile()
        sleep(4)
        num_of_following = self.browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span")
        return self._cleanup_follow_number(num_of_following)

    def _cleanup_follow_number(self, number_element):
        """
        Number of following/followers does not appear in a numerical format
        This is a helper method to convert the string into a number
        """
        numerical_value = number_element.get_attribute('title')
        if not numerical_value:
            numerical_value = number_element.get_attribute('innerHTML')
        try:
            numerical_value = int(numerical_value.replace(',', ''))
        except ValueError:
            pass
        return numerical_value

    def unfollow_unfollowers(self, unfollow_limit=None):
        not_followers = self.get_unfollowers()
        if not unfollow_limit:
            unfollow_limit = len(not_followers)
        for user_number, href in enumerate(not_followers.values()):
            if user_number == unfollow_limit:
                break  # Exit loop if we reached the specified number of unfollowers
            try:
                self.browser.get(href)
                sleep(15)
                # Unfollow button
                self.browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button').click()
                sleep(15)
                self.browser.find_element_by_xpath(
                    "/html/body/div[4]/div/div/div/div[3]/button[1]").click()
                print(
                    "unfollowed: {0}\n Unfollowing 1 person every 30 seconds".format(href))
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
        self.browser.find_element_by_xpath(
            "//a[contains(@href, '/followers')]").click()
        followers = self._get_names()
        return followers

    def _get_following_list(self):
        self.browser.find_element_by_xpath(
            "//a[contains(@href, '/following')]").click()
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

    # TODO
    # def like_following_feed(self):
    #     # for picture_index in range(5,10):
    #     try:
    #         # print("Picture index: {0}/50".format(picture_index + 1))
    #         # self.browser.execute_script("window.scrollTo({ bottom: 800, behavior: 'smooth' });")
    #         # sleep(3)
    #         buttons = self.browser.find_elements_by_tag_name('button')
    #         like_buttons = [button for button in buttons if button.get_attribute('class') == 'wpO6b ']
    #         print ("Will like {0} pictures".format(len(like_buttons)))
    #         sleep(10)
    #         for like_button in like_buttons:
    #             like_button.click()
    #             sleep(10)
    #     except Exception as ex:
    #         print(ex)

    def end_session(self):
        self.browser.close()
