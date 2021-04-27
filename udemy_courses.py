import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import regex as re
import os
import glob
import shutil


class Coursera:
	def __init__(self, driver_type, words, lang, level, duration, topic, rating):
		options = Options()
		# Headless false to get a Chrome Window
		options.headless = False
		self.driver = webdriver.Chrome(options=options, executable_path=driver_type)
		self.words = words
		self.lang = lang
		self.duration = duration
		self.level = level
		self.topic = topic
		self.rating = rating
		# self.count = 1
		self.root_url = ''
	
	def get_url(self):
		# Choses what language we want to scrape in
		languages = {1: 'English', 2: 'German', 3: 'Spanish', 4: 'Arabic', 5: 'Italian', 6: 'Russian', 7: 'French'}
		duration = {1: "Less Than 2 Hours", 2: "1-4 Weeks", 3: "1-3 Months", 4: "3 + Months"}
		# https://www.coursera.org/search?query=Python&index=prod_all_products_term_optimization&allLanguages=English&productDifficultyLevel=Beginner&productDurationEnum=1%20-
		#                                             &index=prod_all_products_term_optimization&productDurationEnum=1-3%20Months
		# dur = Less%20Than%202%20Hours, 1-4%20Weeks , 1-3%20Months , 3%2B%20Months (%2B == +)

		# ===========================================
		#
		# https://www.udemy.com/courses/search/?src=ukw&q=javaprint("Creating URL")
		# https://www.udemy.com/courses/search/?src=ukw&q=c%2B%2B
		# https://www.udemy.com/courses/search/?src=ukw&q=diet
		# https://www.udemy.com/courses/search/?src=ukw&q=python
		# https://www.udemy.com/topic/Yoga/?duration=medium&instructional_level=intermediate&lang=en&ratings=4.5&sort=popularity
		url = "https://www.udemy.com/"

		time.sleep(3)
		# url += "courses/search/?src=ukw&q={}".format(self.words)
		url += 'topic/{}/'.format(self.words)
		url += "?ratings={}".format(self.rating)
		url += "&duration={}".format(self.duration)
		url += "&instructional_level={}".format(self.level)
		if self.lang == 'English':
			self.lang = 'en'
			url += "&lang={}".format(self.lang)

		self.root_url = url
		# url += "?p={}".format(self.count)

		# https://www.udemy.com/topic/yoga/?ratings=4.5&sort=popularity
		# https://www.udemy.com/topic/Python/?ratings={}&duration={}&sort=popularity rating = [3.0, 3.5, 4.0, 4.5] duration = [short, medium, long, extraLong]
		# https://www.udemy.com/topic/Python/?duration={}&sort=popularity
		# https://www.udemy.com/courses/development/
		# https: // www.udemy.com / courses / development / web - development /
		# https://www.udemy.com/topic/health/
		# self.driver.find_element_by_xpath('//*[@id="u1279-popper-trigger--1"]/span').click()
		# #u1279-popper-trigger--1 > span
		self.driver.get(url)
		print(url)

		print("Initializing Containers and Pre-requisites")


	def update_final_url(self):
		pass
	
	def scroll_find_course(self):
		self.get_url()
		count = 1
		name = []
		provider = []
		difficulty = []
		avg_rating = []
		total_ratings = []
		while count <= 3:
			# print((time.time() - start_time), "<", self.max_time)
			# drv.send_keys(Keys.PAGE_DOWN)
			time.sleep(5)
			self.driver.execute_script(f"window.scrollTo(0, {5000});")
			
			print("Getting Containers of EACH courses")
			print(f"Getting details from page number: {count}")
			for number in range(1, 17):
				# try:
				# print(f"For iteration number: {number}")
				# container_list = self.driver.find_element_by_css_selector("#udemy > div.main-content-wrapper > div.main-content > div > div > div:nth-child(9) > div.course-directory--container--5ZPhr > div:nth-child(1) > div.filter-panel--filtered-paginated-course-list--2oGVh > div > div.filter-panel--paginated-course-list--2F0x1 > div.course-list--container--3zXPS")
				container = self.driver.find_elements_by_css_selector("#udemy > div.main-content-wrapper > "
																	  "div.main-content > div > div > div:nth-child(8) "
																	  "> div.course-directory--container--5ZPhr > "
																	  "div:nth-child(1) > "
																	  "div.filter-panel--filtered-paginated-course"
																	  "-list--2oGVh > div > "
																	  "div.filter-panel--paginated-course-list--2F0x1 "
																	  "> div.course-list--container--3zXPS > "
																	  "div:nth-child({})".format(number))
				# a = self.driver.fi
				# #udemy > div.main-content-wrapper > div.main-content > div > div > div:nth-child(8) > div.course-directory--container--5ZPhr > div:nth-child(1) > div.filter-panel--filtered-paginated-course-list--2oGVh > div > div.filter-panel--paginated-course-list--2F0x1 > div.course-list--container--3zXPS > div:nth-child(1)
				# #udemy > div.main-content-wrapper > div.main-content > div > div > div:nth-child(9) > div.course-directory--container--5ZPhr > div:nth-child(1) > div.filter-panel--filtered-paginated-course-list--2oGVh > div > div.filter-panel--paginated-course-list--2F0x1 > div.course-list--container--3zXPS > div:nth-child(1)
				# #udemy > div.main-content-wrapper > div.main-content > div > div > div:nth-child(9) > div.course-directory--container--5ZPhr > div:nth-child(1) > div.filter-panel--filtered-paginated-course-list--2oGVh > div > div.filter-panel--paginated-course-list--2F0x1 > div.course-list--container--3zXPS > div:nth-child(2)
				print(container)
				if len(container) == 0:
					container = self.driver.find_elements_by_css_selector("#udemy > div.main-content-wrapper > "
																		  "div.main-content > div > div > "
																		  "div:nth-child(9) > "
																		  "div.course-directory--container--5ZPhr > "
																		  "div:nth-child(1) > "
																		  "div.filter-panel--filtered-paginated-course"
																		  "-list--2oGVh > div > "
																		  "div.filter-panel--paginated-course-list"
																		  "--2F0x1 > div.course-list--container--3zXPS "
																		  "> div:nth-child({})".format(number))
					print(container)

					for courses in container:
						try:

							course_name = courses.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/div["
																			 "6]/div[3]/div[1]/div[2]/div/div[2]/div["
																			 "2]/div[{}]/a/div/div[2]/div[1]".
																			format(number))\

							# #u404-popper-trigger--150 > div > div.course-card--main-content--3xEIw.course-card--has-price-text--1Ikr0 > div.udlite-focus-visible-target.udlite-heading-md.course-card--course-title--2f7tE
							# #u404-popper-trigger--153 > div > div.course-card--main-content--3xEIw.course-card--has-price-text--1Ikr0 > div.udlite-focus-visible-target.udlite-heading-md.course-card--course-title--2f7tE
							# #u745-popper-trigger--124 > div > div.course-card--main-content--3xEIw.course-card--has-price-text--1Ikr0 > div.udlite-focus-visible-target.udlite-heading-md.course-card--course-title--2f7tE
							# #u745-popper-trigger--124 > div > div.course-card--main-content--3xEIw.course-card--has-price-text--1Ikr0
							print(course_name.text)
							# #u404-popper-trigger--150 > div > div.course-card--main-content--3xEIw.course-card--has-price-text--1Ikr0 > div.udlite-focus-visible-target.udlite-heading-md.course-card--course-title--2f7tE

							# udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE
							# udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE
							# //*[@id="u398-popper-trigger--603"]/div/div[2]/div[1]

							# //*[@id="u398-popper-trigger--606"]/div/div[2]/div[1]
							# //*[@id="u398-popper-trigger--651"]/div/div[2]/div[1]
							# /html/body/div[3]/div[3]/div/div/div[6]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div[1]/a/div/div[2]/div[1]
							# /html/body/div[3]/div[3]/div/div/div[6]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div[2]/a/div/div[2]/div[1]
							# /html/body/div[3]/div[3]/div/div/div[6]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div[3]/a/div/div[2]/div[1]
							# course_provider = courses.find_element_by_css_selector(
							# 	"#__next > div > div.rc-SearchPage > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div.tab-contents > div > div > div > div > ul > li:nth-child({}) > div > div > div > div > div > div.card-info.vertical-box > div:nth-child(2) > span".format(
							# 		number))
							#
							# course_difficulty = courses.find_element_by_css_selector(
							# 	"#__next > div > div.rc-SearchPage > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div.tab-contents > div > div > div > div > ul > li:nth-child({}) > div > div > div > div > div > div.card-info.vertical-box > div.rc-ProductInfo > div.product-difficulty > span".format(
							# 		number))
							#
							# course_rating = courses.find_element_by_css_selector(
							# 	"#__next > div > div.rc-SearchPage > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div.tab-contents > div > div > div > div > ul > li:nth-child({}) > div > div > div > div > div > div.card-info.vertical-box > div.rc-ProductInfo > div.rating-enroll-wrapper > div:nth-child(1) > div > span.ratings-text".format(
							# 		number))
							#
							# rated_by = courses.find_element_by_css_selector(
							# 	"#__next > div > div.rc-SearchPage > div > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div.tab-contents > div > div > div > div > ul > li:nth-child({}) > div > div > div > div > div > div.card-info.vertical-box > div.rc-ProductInfo > div.rating-enroll-wrapper > div:nth-child(1) > div > span.ratings-count > span".format(
							# 		number))
							# name.append(course_name.text)
							# provider.append(course_provider.text)
							# difficulty.append(course_difficulty.text)
							# avg_rating.append(course_rating.text)
							# total_ratings.append(rated_by.text)
							# self.driver.execute_script(f"window.scrollTo(0, {999});")

						except (NoSuchElementException, StaleElementReferenceException):
							if NoSuchElementException:
								print("No element present")
							elif StaleElementReferenceException:
								print('Some elements have been updated')

			# except:

			quit()
			# print(len(name),"\n","Provider", len(provider),"\n","Difficulty" ,len(difficulty),"\n","Avg", len(avg_rating),"\n","Total", len(total_ratings))
			# time.sleep(10)
			count += 1
			print("Dumping extracted values to List")
			print(f"Moving to page number: {count}")
			self.driver.find_element_by_css_selector("#udemy > div.main-content-wrapper > div.main-content > div > div > div:nth-child(8) > div.course-directory--container--5ZPhr > div.pagination--container--2wc6Z > a.udlite-btn.udlite-btn-medium.udlite-btn-secondary.udlite-btn-round.udlite-heading-sm.udlite-btn-icon.udlite-btn-icon-medium.udlite-btn-icon-round.pagination--next--5NrLo").click()
			time.sleep(3)
		# #udemy > div.main-content-wrapper > div.main-content > div > div > div:nth-child(8) > div.course-directory--container--5ZPhr > div.pagination--container--2wc6Z > a:nth-child(3)
		# #udemy > div.main-content-wrapper > div.main-content > div > div > div:nth-child(8) > div.course-directory--container--5ZPhr > div.pagination--container--2wc6Z > a:nth-child(4)
		# #udemy > div.main-content-wrapper > div.main-content > div > div > div:nth-child(8) > div.course-directory--container--5ZPhr > div.pagination--container--2wc6Z > a.udlite-btn.udlite-btn-medium.udlite-btn-secondary.udlite-btn-round.udlite-heading-sm.udlite-btn-icon.udlite-btn-icon-medium.udlite-btn-icon-round.pagination--next--5NrLo
		return name, provider, difficulty, avg_rating, total_ratings
	
	
	
if __name__ == '__main__':
	ed = Coursera("C:\Program Files (x86)\Google\Chrome\chromedriver.exe", "Java", "English", "", "medium", "", "4.0")
	ed.scroll_find_course()


	# #u368-popper-trigger--122 > div
	# #u368-popper-trigger--125 > div
	# #u368-popper-trigger--131 > div
	# #u368-popper-trigger--134 > div


# #u368-popper-trigger--210 > div > div.course-card--main-content--3xEIw.course-card--has-price-text--1Ikr0 > div.udlite-focus-visible-target.udlite-heading-md.course-card--course-title--2f7tE
# #u368-popper-trigger--213 > div > div.course-card--main-content--3xEIw.course-card--has-price-text--1Ikr0 > div.udlite-focus-visible-target.udlite-heading-md.course-card--course-title--2f7tE



# //*[@id="u368-popper-trigger--210"]/div/div[2]/div[1]
# //*[@id="u368-popper-trigger--213"]/div/div[2]/div[1]
# //*[@id="u368-popper-trigger--216"]/div/div[2]/div[1]
# //*[@id="u368-popper-trigger--219"]/div/div[2]/div[1]
# //*[@id="u368-popper-trigger--222"]/div/div[2]/div[1]

# //*[@id="u368-popper-trigger--234"]/div/div[2]/div[1]
# //*[@id="u545-popper-trigger--93"]/div/div[2]/div[1]


# udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE
# udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE