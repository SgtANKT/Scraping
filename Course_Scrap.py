import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import regex as re
import os
import glob
import shutil
import numpy as np


def merge_all_csv():
    out_path = r"C:\Users\ankit\Development\Twitter\Coursea"
    allFiles = glob.glob(out_path + "/*.csv")
    allFiles.sort()  # glob lacks reliable ordering, so impose your own if output order matters
    with open(out_path + r"\consolidated\Courses_Combined_Coursera.csv", 'wb') as outfile:
        for i, fname in enumerate(allFiles):
            with open(fname, 'rb') as infile:
                if i != 0:
                    infile.readline()  # Throw away header on all  but first file
                # Block copy rest of file from input to output without parsing
                shutil.copyfileobj(infile, outfile)
                print(fname + " has been imported.")


class Coursera:
    def __init__(self, driver_type, words, lang, level, duration, topic):
        options = Options()
        # Headless false to get a Chrome Window
        options.headless = False
        self.driver = webdriver.Chrome(options=options, executable_path=driver_type)
        self.words = words
        self.lang = lang
        self.duration = duration
        self.level = level
        self.topic = topic


    def get_url(self):
        # Choses what language we want to scrape in
        languages = {1: 'English', 2: 'German', 3: 'Spanish', 4: 'Arabic', 5: 'Italian', 6: 'Russian', 7: 'French'}
        duration = {1: "Less Than 2 Hours", 2: "1-4 Weeks", 3: "1-3 Months", 4: "3 + Months"}
        # dur = Less%20Than%202%20Hours, 1-4%20Weeks , 1-3%20Months , 3%2B%20Months (%2B == +)

        print("Creating URL")
        url = "https://www.coursera.org/search?query="
        # https://www.coursera.org/search?query=c%2B%2B
        course_to_search = self.words
        if '+' in course_to_search:
            print("C++")
            url += 'c%2B%2B'
        elif '#' in course_to_search:
            print("C#")
            url += 'c%23'
        else:
            url += course_to_search

        language = self.lang
        print(len(language))
        if len(language) == 0:
            url += "&index=prod_all_products_term_optimization"
        else:
            url += '&index=prod_all_products_term_optimization&allLanguages={}'.format(language)

        level = self.level
        if len(level) == 0:
            pass
        else:
            url += "&productDifficultyLevel={}".format(level)

        duration = self.duration
        if len(duration) == 0:
            pass
        elif duration == "Less Than 2 Hours":
            url += "&productDurationEnum=Less%20Than%202%20Hours"
        elif duration == "1-4 Weeks" or duration == "1-3 Months":
            split_words = duration.split()
            url += "&productDurationEnum={}%20{}".format(split_words[0], split_words[1])
        else:
            url += "&productDurationEnum=3%2B%20Months"

        topic = self.topic
        if len(topic) == 0:
            pass
        else:
            split_topics = topic.split()
            if len(split_topics) == 1:
                url += "&topic={}".format(split_topics[0])
            elif len(split_topics) == 2:
                url += "&topic={}%20{}".format(split_topics[0], split_topics[1])
            elif len(split_topics) == 3:
                url += "&topic={}%20{}%20{}".format(split_topics[0], split_topics[1], split_topics[2])

        self.driver.get(url)
        print(url)

    def scroll_find_course(self):
        self.get_url()
        page_count = 10
        count = 1
        name = []
        provider = []
        difficulty = []
        avg_rating = []
        total_ratings = []

        while count <= int(page_count):
            print(count, "<=", page_count)
            time.sleep(10)

            self.driver.execute_script(f"window.scrollTo(0, {2100});")
            print(f"Getting details from page number: {count}")
            for number in range(1, 11):
                # print(f"For iteration number: {number}")
                container = self.driver.find_elements_by_css_selector("#main > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div > div > div > div > div > ul > li:nth-child({}) > div > div".format(number))
                # print(container)

                for courses in container:
                    try:

                        course_name = courses.find_element_by_css_selector("#main > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div > div > div > div > div > ul > li:nth-child({}) > div > div > div > div > div > div.card-info.vertical-box > div:nth-child(1) > h2".format(number))

                        name.append(course_name.text)
                    except (NoSuchElementException, StaleElementReferenceException):
                        if NoSuchElementException:
                            print("No element present")
                            name.append(np.nan)
                        elif StaleElementReferenceException:
                            print('Some elements have been updated')
                            name.append(np.nan)
                    try:
                        course_provider = courses.find_element_by_css_selector("#main > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div > div > div > div > div > ul > li:nth-child({}) > div > div > div > div > div > div.card-info.vertical-box > div:nth-child(2) > span".
                                                                               format(number))

                        provider.append(course_provider.text)

                    except (NoSuchElementException, StaleElementReferenceException):
                        if NoSuchElementException:
                            print("No such element present")
                            provider.append(np.nan)
                        elif StaleElementReferenceException:
                            print('Some elements have been updated')
                            provider.append(np.nan)
                    try:
                        course_difficulty = courses.find_element_by_css_selector("#main > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div > div > div > div > div > ul > li:nth-child({}) > div > div > div > div > div > div.card-info.vertical-box > div.rc-ProductInfo > div.product-difficulty > span".format(number))

                        difficulty.append(course_difficulty.text)
                    except (NoSuchElementException, StaleElementReferenceException):
                        if NoSuchElementException:
                            print("No element present")
                            difficulty.append(np.nan)
                        elif StaleElementReferenceException:
                            print('Some elements have been updated')
                            difficulty.append(np.nan)
                    try:
                        course_rating = courses.find_element_by_css_selector("#main > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div > div > div > div > div > ul > li:nth-child({}) > div > div > div > div > div > div.card-info.vertical-box > div.rc-ProductInfo > div.rating-enroll-wrapper > div:nth-child(1) > div > span.ratings-text".format(number))

                        avg_rating.append(course_rating.text)
                    except (NoSuchElementException, StaleElementReferenceException):
                        if NoSuchElementException:
                            print("No element present")
                            avg_rating.append(np.nan)
                        elif StaleElementReferenceException:
                            print('Some elements have been updated')
                            avg_rating.append(np.nan)

                    try:
                        rated_by = courses.find_element_by_css_selector("#main > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div > div > div > div > div > ul > li:nth-child({}) > div > div > div > div > div > div.card-info.vertical-box > div.rc-ProductInfo > div.rating-enroll-wrapper > div:nth-child(1) > div > span.ratings-count > span".
                                                                        format(number))

                        total_ratings.append(rated_by.text)
                    except (NoSuchElementException, StaleElementReferenceException):
                        if NoSuchElementException:
                            print("No element present")
                            total_ratings.append(np.nan)
                        elif StaleElementReferenceException:
                            print('Some elements have been updated')
                            total_ratings.append(np.nan)




            # print("Name: ",len(name),"\n","Provider: ", len(provider),"\n","Difficulty: " ,len(difficulty),"\n","Avg: ", len(avg_rating),"\n","Total: ", len(total_ratings))
            # time.sleep(10)
            count += 1
            # print("Dumping extracted values to List")
            print(f"Moving to page number: {count}")

            try:
                self.driver.find_element_by_css_selector(
                "#pagination_number_box_{}".format(count)).click()
            except NoSuchElementException:
                try:
                    self.driver.find_element_by_css_selector(
                    "#main > div.ais-InstantSearch__root > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div > div > div > div > div > div.rc-PaginationControls.horizontal-box.align-items-right.large-style > div > button:nth-child(7)").click()
                except:
                    self.driver.find_element_by_css_selector(
                        "#main > div.ais-InstantSearch__root > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div > div > div > div > div > div.rc-PaginationControls.horizontal-box.align-items-right.large-style > div > button:nth-child(8)").click()

            time.sleep(3)

        return name, provider, difficulty, avg_rating, total_ratings

    def write_csv(self):
        courses_coursera = self.scroll_find_course()
        # print("Dumping to Dictionary")
        dictionary = {'CourseName': courses_coursera[0], 'CourseCurator': courses_coursera[1],
                      'Difficulty': courses_coursera[2], 'AverageRatings': courses_coursera[-2],
                      'TotalRatings': courses_coursera[-1]}
        df = pd.DataFrame(dictionary)
        print("DF Length: ", len(df))
        # print("List Length: ", len(tweet))
        print("Creating CSV")
        df.to_csv(f"CourseDatabase_Coursera_{self.words}.csv", index=False)



class Udemy(Coursera):
    def __init__(self, driver_type, words, lang, level, duration, topic):
        super().__init__(driver_type, words, lang, level, duration, topic)


# def get_url(self):


# 		https://www.udemy.com/courses/health-and-fitness/yoga/?search-query=yoga
#       https://www.udemy.com/courses/search/?src=ukw&q=python
#


if __name__ == "__main__":
    course_list = ["Accounting", "Career", "brand management"]
    for course in course_list:
        ed = Coursera("C:\Program Files (x86)\Google\Chrome\chromedriver.exe", course, "English", "", "", "")
        ed.write_csv()

    merge_all_csv()
