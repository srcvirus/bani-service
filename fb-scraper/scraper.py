from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
import sys
import time
import calendar
import utils
from settings import BROWSER_EXE, FIREFOX_BINARY, GECKODRIVER, PROFILE
import json

class CollectPosts(object):
    """Collector of recent FaceBook posts.
           Note: We bypass the FaceBook-Graph-API by using a 
           selenium FireFox instance! 
           This is against the FB guide lines and thus not allowed.

           USE THIS FOR EDUCATIONAL PURPOSES ONLY. DO NOT ACTAULLY RUN IT.
    """

    def __init__(self, ids=["oxfess"], file="posts.csv", depth=5, delay=10):
        self.ids = ids
        self.out_file = file
        self.depth = depth + 1
        self.delay = delay
        # browser instance
        self.browser = webdriver.Firefox(executable_path=GECKODRIVER,
                                         firefox_binary=FIREFOX_BINARY,
                                         firefox_profile=PROFILE,)
        self.wait = WebDriverWait(self.browser, self.delay)
        utils.create_csv(self.out_file)


    def collect_page(self, page):
        banis = dict()
        # navigate to page
        self.browser.get(
            'https://m.facebook.com/' + page + '/')

        # Scroll down depth-times and wait delay seconds to load
        # between scrolls
        for scroll in range(self.depth):

            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.delay/2)

        # Once the full page is loaded, we can start scraping
        links = self.browser.find_elements_by_link_text("See more")
        for link in links:
            link.click()
        div = self.browser.find_element_by_id('structured_composer_async_container')
        posts = div.find_elements_by_xpath(".//article")
        print "Crawled " + str(len(posts)) + " posts."
        idx = 1
        for count, post in enumerate(posts):
            story_container = self.safe_find_element_by_xpath(post, ".//div[@class='story_body_container']")
            span_elems = self.safe_find_elements_by_xpath(story_container, ".//span")
            if span_elems is None:
                continue
            text = ""
            for span_elem in span_elems:
                if span_elem.text is not None and len(span_elem.text) > 0:
                    text = span_elem.text.encode("ascii", "ignore")
                    if len(text) > 0:
                        if (text.startswith('\"') or text.endswith('\"') or text.endswith('.')):
                            if text not in banis:
                                banis[text] = idx
                                idx += 1

                # Write row to csv
                # utils.write_to_csv(self.out_file, csv_row)
        print "Total " + str(len(banis.keys())) + " banis processed."
        json_dict = dict()
        json_dict["banis"] = []
        for bani in banis.keys():
            print ",".join([str(banis[bani]), bani])
            json_dict["banis"].append({"index": banis[bani], "text": bani})
        json_dict["banis"].sort(key = lambda x: x["index"])
        with open("posts.json", "w+") as f:
            f.write(json.dumps(json_dict))

    def collect_groups(self, group):
        # navigate to page
        self.browser.get(
            'https://m.facebook.com/groups/' + group + '/')

        # Scroll down depth-times and wait delay seconds to load
        # between scrolls
        for scroll in range(self.depth):

            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.delay)

        # Once the full page is loaded, we can start scraping
        links = self.browser.find_elements_by_link_text("See more")
        for link in links:
            link.click()
        posts = self.browser.find_elements_by_class_name(
            "userContentWrapper")
        poster_names = self.browser.find_elements_by_xpath(
            "//a[@data-hovercard-referer]")

        for count, post in enumerate(posts):
            # Creating first CSV row entry with the poster name (eg. "Donald Trump")
            analysis = [poster_names[count].text]

            # Creating a time entry.
            time_element = post.find_element_by_css_selector("abbr")
            utime = time_element.get_attribute("data-utime")
            analysis.append(utime)

            # Creating post text entry
            text = post.find_element_by_class_name("userContent").text
            status = utils.strip(text)
            analysis.append(status)

            # Write row to csv
            utils.write_to_csv(self.out_file, analysis)

    def collect(self, typ):
        if typ == "groups":
            for iden in self.ids:
                self.collect_groups(iden)
        elif typ == "pages":
            for iden in self.ids:
                self.collect_page(iden)
        self.browser.close()

    def safe_find_element_by_id(self, elem_id):
        try:
            return self.browser.find_element_by_id(elem_id)
        except NoSuchElementException:
            return None
    
    def safe_find_element_by_xpath(self, obj, xpath_str):
        try:
            return obj.find_element_by_xpath(xpath_str)
        except NoSuchElementException:
            return None

    def safe_find_elements_by_xpath(self, obj, xpath_str):
        try:
            return obj.find_elements_by_xpath(xpath_str)
        except NoSuchElementException:
            return None

    def login(self, email, password):
        try:

            #self.browser.get("https://www.facebook.com")
            self.browser.get("https://m.facebook.com")
            self.browser.maximize_window()

            # filling the form
            self.browser.find_element_by_name('email').send_keys(email)
            self.browser.find_element_by_name('pass').send_keys(password)

            # clicking on login button
            # self.browser.find_element_by_id('loginbutton').click()
            self.browser.find_element_by_name('login').click()
            # if your account uses multi factor authentication
            #mfa_code_input = self.safe_find_element_by_id('approvals_code')

            #if mfa_code_input is None:
            #    return

            #mfa_code_input.send_keys(input("Enter MFA code: "))
            #self.browser.find_element_by_id('checkpointSubmitButton').click()
            
            # there are so many screens asking you to verify things. Just skip them all
            #while self.safe_find_element_by_id('checkpointSubmitButton') is not None:
            #    dont_save_browser_radio = self.safe_find_element_by_id('u_0_3')
            #    if dont_save_browser_radio is not None:
            #        dont_save_browser_radio.click()

            #    self.browser.find_element_by_id(
            #        'checkpointSubmitButton').click()
            self.wait.until(EC.url_changes('https://m.facebook.com/'))
            self.browser.get('https://m.facebook.com/')

        except Exception as e:
            print("There was some error while logging in.")
            print(sys.exc_info()[0])
            exit()
