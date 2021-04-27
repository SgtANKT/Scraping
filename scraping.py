# from bs4 import BeautifulSoup
# import test as t
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from csv import DictWriter
# import pprint
# from selenium.webdriver.common.keys import Keys
# import datetime
# from datetime import date, timedelta
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException


class Twitter:
    def __init__(self, driver_type, words, lang):
        options = Options()
        # Headless false to get a Chrome Window
        options.headless = False
        self.driver = webdriver.Chrome(options=options, executable_path=driver_type)
        # self.start_date = start_date
        # self.end_date = end_date
        self.words = words
        self.lang = lang
        # self.max_time = max_time

    # def drivers(self):
    #     if self.driver == 1:
    #         driver = webdriver.Firefox(executable_path="C:\\Drivers\\FD\\geckodriver.exe")
    #     elif self.driver == 2:
    #         options = Options()
    #         options.headless = True
    #         driver = webdriver.Chrome(options=options ,executable_path="C:\\Drivers\\CD\\chromedriver.exe")
    #     elif self.driver == 3:
    #         driver = webdriver.Ie(executable_path="C:\\Drivers\\IED\\IEDriverServer.exe")
    #     elif self.driver == 4:
    #         driver = webdriver.Opera(executable_path="C:\\Drivers\\OD\\operadriver.exe")
    #     return driver

    def scroll_find_tweets(self):
        #Choses what language we want to scrape in
        languages = {1: 'English', 2: 'German', 3: 'Spanish', 4: 'Arabic', 5: 'Italian', 6: 'Russian', 7: 'French'}
        duration = {1:"Less Than 2 Hours", 2:"1-4 Weeks", 3:"1-3 Months", 4:"3 + Months"}
        # Do not  require to log into twitter so my account won't be facing any bans
        # https://www.coursera.org/search?query=python&index=prod_all_products_term_optimization&allLanguages=Spanish&productDifficultyLevel=Beginner&productDurationEnum=1-3%20Months&topic=Data%20Science
        # dur = Less%20Than%202%20Hours, 1-4%20Weeks , 1-3%20Months , 3%2B%20Months (%2B == +)
        url = "https://www.coursera.org/search?query="

        
        # https://twitter.com/search?q=
        # https://www.coursera.org/search?query=
        # words_to_search = self.words.split(',')
        #Loops over the words and adds it into our URL
        course_to_search = self.words
        url += course_to_search
        
        
        
        language = self.lang
        url += '&index=prod_all_products_term_optimization&allLanguages={}'.format(language)
        
        duration = self.duration
        if duration == "Less Than 2 Hours":
            duration.split(" ")
            url += "&productDifficultyLevel=Beginner&productDurationEnum={}%20{}%20{}%20{}".format(duration[0], duration[1])
        
        url += '&productDifficultyLevel=Beginner&productDurationEnum=1-3%20Months'
        
        
        self.driver.get(url)
        quit()
        
        
        # for words in words_to_search:
        #     words = words.strip()
        # for word in words_to_search[:-1]:
        #     url += "{}%20OR".format(word)
        # url += "{}%20".format(words_to_search[-1])
        # url += "since%3A{}%20until%3A{}&".format(self.start_date, self.end_date)
        #Appends language to url
        if self.lang != 0:
            url += "l={}&".format(languages[self.lang])
        url += "src=typd"
        print(url)
        self.driver.get(url)
        start_time = time.time()
        # Goes onto the url and starts scrolling
        # Could've used send_keys(keys.Page_Down) but it gives an error
        # last_height = self.driver.execute_script("return document.body.scrollHeight")
        while (time.time() - start_time) < self.max_time:
            print((time.time() - start_time), "<", self.max_time)
            # drv.send_keys(Keys.PAGE_DOWN)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(6)
            # finds the location of our tweet and saves it
            # for i in range(1):
            #     containers = drv.find_elements_by_css_selector("#react-root > div > div > "
            #                                               "div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div "
            #                                               "> div > div > div > div > div:nth-child(2) > div > div > "
            #                                               "section > div > div > div:nth-child({})".format(i))
            #
            name = []
            dates = []
            user_id = []
            user_tw = []
            for number in range(1, 19):
                container = self.driver.find_elements_by_css_selector(
                    "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(2) > div > div > section > div > div > div:nth-child({}) > div > div > article".format(number))
                for tweet_details in container:
                    # print(r.text)
                    # a = r.find
                    tweets = tweet_details.find_element_by_css_selector("#react-root > div > div > "
                                                       "div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > "
                                                       "div > div > div > div > div:nth-child(2) > div > div > "
                                                       "section > div > div > div:nth-child({}) > div > div > "
                                                       "article > div > div > div > div.css-1dbjc4n.r-18u37iz > "
                                                       "div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > "
                                                       "div:nth-child(2) > div:nth-child(1) > div".format(number))
                    
                    names = tweet_details.find_element_by_css_selector(
                        "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(2) > div > div > section > div > div > div:nth-child({}) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(1) > div > div".format(
                            number))
                    # Splits the data scraped into the Date,Name,Tweets,UserID accordingly
                    info = names.text.split('\n')
                    info_name = info[0]
                    name.append(info_name)
                    info_user_id = info[1]
                    user_id.append(info_user_id)
                    tweet_date = info[-1]
                    dates.append(tweet_date)
                    tweets_info = info_name+":"+info_user_id+":"+str(tweets.text)+f" -tweeted on {tweet_date}"
                    user_tweet = tweets.text
                    user_tw.append(user_tweet)

        return name, user_id, user_tw, dates

    def write_csv(self):
        user_and_tweet = self.scroll_find_tweets()
        name = user_and_tweet[0]
        user_id = user_and_tweet[1]
        date = user_and_tweet[-1]
        tweet = user_and_tweet[-2]

        dictionary = {'Date': date, 'Name': name,'UserID': user_id, 'Tweets': tweet}
        df = pd.DataFrame(dictionary)
        print("DF Length: ", len(df))
        print("List Length: ", len(tweet))
        df.to_csv("Twitter_Data_Test.csv", index=False)

    






if __name__ == "__main__":
    ed = Twitter("C:\Program Files (x86)\Google\Chrome\chromedriver.exe" ,"Python", "English")
    ed.write_csv()
    