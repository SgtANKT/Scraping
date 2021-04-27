
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import regex as re
import os
import glob
import shutil


def test(word):
    li = word.split()
    print(len(li))


def merge_all_csv():
    out_path = r"C:\Users\ankit\Development\Twitter\Naukri"
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
    def __init__(self, driver_type, words):
        options = Options()
        # Headless false to get a Chrome Window
        options.headless = False
        options.add_experimental_option("prefs", {'protocol_handler.excluded_schemes.tel': False})
        # driver = webdriver.Chrome(chrome_options=options)
        self.driver = webdriver.Chrome(options=options, executable_path=driver_type)
        self.words = words
        # self.count = 1
        self.root_url = ''

    def get_url(self):
        # Choses what language we want to scrape in
        languages = {1: 'English', 2: 'German', 3: 'Spanish', 4: 'Arabic', 5: 'Italian', 6: 'Russian', 7: 'French'}
        duration = {1: "Less Than 2 Hours", 2: "1-4 Weeks", 3: "1-3 Months", 4: "3 + Months"}

        url = "https://www.naukri.com/"
        time.sleep(5)
        # https://www.naukri.com/python-jobs?k=python
        # https://www.naukri.com/c-sharp-jobs?k=c%23
        # https://www.naukri.com/c-plus-plus-jobs?k=c%2B%2B
        # https://www.naukri.com/content-writing-jobs?k=content%20writing
        word_list = self.words.split()
        if len(word_list) < 2:
            url += '{}-jobs?k={}'.format(self.words, self.words)
        elif len(word_list) == 2:
            url +='{}-{}-jobs?k={}%20{}'.format(word_list[0], word_list[1],word_list[0], word_list[1])

        self.root_url = url

        self.driver.get(url)
        # #root > div.search-result-container > div.content > section.listContainer.fleft > div.list > article:nth-child(1)
        # #root > div.search-result-container > div.content > section.listContainer.fleft > div.list > article:nth-child(2)
        # #root > div.search-result-container > div.content > section.listContainer.fleft > div.list > article:nth-child(4)
        # quit()
        print("Initializing Containers and Pre-requisites")

    def update_final_url(self):
        pass

    def scroll_find_course(self):
        self.get_url()
        count = 1
        title = []
        company = []
        experience = []
        description = []
        avg_rating = []
        total_ratings = []
        button_click = self.driver.find_element_by_css_selector("#root > div.search-result-container > div.privacyPolicy > div > button").click()
        while count < 20:

            time.sleep(5)
            self.driver.execute_script(f"window.scrollTo(0, {4430});")

            # print("Getting Containers of EACH courses")
            print(f"Getting details from page number: {count}")
            for number in range(1, 21):
                # try:
                # print(f"For iteration number: {number}")
                container = self.driver.find_elements_by_css_selector("#root > div.search-result-container > "
                                                                      "div.content > section.listContainer.fleft > "
                                                                      "div.list > article:nth-child({})".format(number))
                # a = self.driver.fi
                # print(container)
                # print(len(title), f"after {number} iteration")
                for jobs in container:
                    try:
                        job_name = jobs.find_element_by_css_selector("#root > div.search-result-container > "
                                                                           "div.content > section.listContainer.fleft "
                                                                           "> div.list > article:nth-child({}) > "
                                                                           "div.jobTupleHeader > div.info.fleft > a".
                                                                           format(number))
                        # print(course_name.text)
                        job_provider = jobs.find_element_by_css_selector("#root > div.search-result-container > "
                                                                            "div.content > "
                                                                            "section.listContainer.fleft > div.list > "
                                                                            "article:nth-child({}) > "
                                                                            "div.jobTupleHeader > div.info.fleft > "
                                                                            "div > a.subTitle.ellipsis.fleft".
                                                                            format(number))

                        job_experience = jobs.find_element_by_css_selector("#root > div.search-result-container > "
                                                                           "div.content > section.listContainer.fleft "
                                                                           "> div.list > article:nth-child({}) > "
                                                                           "div.jobTupleHeader > div.info.fleft > ul "
                                                                           "> "
                                                                           "li.fleft.grey-text.br2.placeHolderLi"
                                                                           ".experience > span".format(number))

                        # descr = jobs.find_element_by_css_selector()
                        job_description = jobs.find_element_by_css_selector("#root > div.search-result-container > "
                                                                            "div.content > "
                                                                            "section.listContainer.fleft > div.list > "
                                                                            "article:nth-child({}) > ul".
                                                                            format(number))


                        # print(job_description.text.split('\n'))
                        # print(type(job_description.text),'\n',"====================================")
                        job_rating = jobs.find_element_by_css_selector("#root > div.search-result-container > "
                                                                       "div.content > section.listContainer.fleft > "
                                                                       "div.list > article:nth-child({}) > "
                                                                       "div.jobTupleHeader > div.info.fleft > div > "
                                                                       "span".format(number))
                        rated_by = jobs.find_element_by_css_selector("#root > div.search-result-container > "
                                                                     "div.content > section.listContainer.fleft > "
                                                                     "div.list > article:nth-child({}) > "
                                                                     "div.jobTupleHeader > div.info.fleft > div > "
                                                                     "a.reviewsCount.ml-5.fleft.blue-text".
                                                                     format(number))

                        # self.driver.execute_script(f"window.scrollTo(0, {999});")
                        title.append(job_name.text)
                        company.append(job_provider.text)
                        experience.append(job_experience.text)
                        desc_split = job_description.text.split()
                        description.append(desc_split)
                        avg_rating.append(job_rating.text)
                        total_ratings.append(rated_by.text)
                        # print(len(title), f"after {number} iteration")

                    except (NoSuchElementException, StaleElementReferenceException):
                        if NoSuchElementException:
                            print("No element present")
                        elif StaleElementReferenceException:
                            print('Some elements have been updated')

            # for i in description:
            #     i.split('\n')
            # description = [i.split('\n') for i in description]
            print(description)
                # print("Job Title: ", job_name.text,'\n',"Company: ", job_provider.text)
            # except:
            # print(len(title) ,"\n" ,"Provider: ", len(company) ,"\n" ,"Experience: " ,len(experience), "\n", "Avg: ",
            #       len(avg_rating), "\n", "Total: ", len(total_ratings), '\n', "Description: ", len(description))

            count += 1
            # print("Dumping extracted values to List")
            print(f"Moving to page number: {count}")
            self.driver.find_element_by_css_selector("#root > div.search-result-container > div.content > "
                                                     "section.listContainer.fleft > div.pagination.mt-64.mb-60 > "
                                                     "a.fright.fs14.btn-secondary.br2".format(count)).click()
            #
            # "#root > div.search-result-container > div.content > section.listContainer.fleft > div.pagination.mt-64.mb-60 > div > a:nth-child({})"
            time.sleep(3)

        return title, company, experience, description, avg_rating, total_ratings

    def write_csv(self):
        naukri_jobs = self.scroll_find_course()
        print("Dumping to Dictionary")
        dictionary = {'Job_Title': naukri_jobs[0], 'Company': naukri_jobs[1], 'Experience': naukri_jobs[2],
                      'Description': naukri_jobs[3],
                      'AverageRatings': naukri_jobs[-2], 'TotalRatings': naukri_jobs[-1]}
        df = pd.DataFrame(dictionary)
        print("DF Length: ", len(df))
        # print("List Length: ", len(tweet))
        print("Dumping to CSV")
        df.to_csv(f"Naukri\JobDatabase_Naukri_{self.words}.csv", index=False)

    def merge_all_csv(self):
        out_path = r"/"
        allFiles = glob.glob(out_path + "/*.csv")
        allFiles.sort()  # glob lacks reliable ordering, so impose your own if output order matters
        with open(out_path + r"\consolidated\Naukri_Combined_Jobs.csv", 'wb') as outfile:
            for i, fname in enumerate(allFiles):
                with open(fname, 'rb') as infile:
                    if i != 0:
                        infile.readline()  # Throw away header on all  but first file
                    # Block copy rest of file from input to output without parsing
                    shutil.copyfileobj(infile, outfile)
                    print(fname + " has been imported.")



if __name__ == '__main__':
    # 'Python', 'Java', "Content Writing", "Javascript", "Illustrator", "Social Media", "Marketing", "Sales","Chef",
    # "Block chain", "Lab", "Electrician", "Mechanic", "Engine Operator", "Coach", "Tutor"
    # "Tech Support", "Dev Ops", "PHP", "Public Speaking","Advertising", "Vet", "Video Editor", "Sound Engineer"
    job_list = ["SQL","Tech Support", "Dev Ops", "PHP", "Public Speaking","Advertising", "Vet", "Video Editor", "Sound Engineer"]
    for job in job_list:
        ed = Coursera("C:\Program Files (x86)\Google\Chrome\chromedriver.exe", job)
        ed.write_csv()
    # test("Post Marital")
    merge_all_csv()