from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import numpy as np
import pandas as pd

startTime = time.time()
opts = Options()
opts.add_argument("--incognito")
PATH = "dataset/chromedriver"
driver = webdriver.Chrome(PATH , options=opts)

driver.maximize_window()
driver.get("https://www.udemy.com/")
print(driver.title)

courseId = 1
#providerId = 1
reviewId = 1

coursesDict = {}
#providerDict = {}

MasterTableDict = {
	"Course_ID"				:	[],
	"Tags_(Field_of_Study)" : 	[],
	"Tags_(Tools_and_Tech)" :   [],
	"Title"					:	[],
	"Description"			:	[],
	"Week_Titles"			:	[],
	"Language"				:	[],
	"Rating"				:	[],
	"Number_of_Ratings"		:	[],
	"Offered_By"			:	[],
	"Website"				:	[],
	"Enrolled_Students"		:	[],
	"Instructor"			:	[],
	"Level"					:	[],
	"Price"					:	[],
	"Time_(to_display)"		:	[],
	"Pace"					:	[],
	"Pre-requisite"			:	[],
	"Certificate"			:	[],
	"Link"					:	[],
	"Image_Link"			:	[],
	"Page"					:	[]
}

CourseTableDict = {
	"Course_ID"             : 	[],
	"Title"					:	[],
	"Tags_(Tools_and_Tech)" :   [],
	"Pre-requisite"			:	[],
}

ReviewTableDict = {
	"Review_ID"				:	[],
	"Course_ID"             : 	[],
	"Title"					:	[],
	"Review_Name"			:	[],
	"Review_Rating"			:	[],
	"Review_Body"			:	[]
}

#Remove links that are not required
clink = 0
#courseLinks = ["https://www.udemy.com/courses/development/", "https://www.udemy.com/courses/business/",
				#"https://www.udemy.com/courses/it-and-software/","https://www.udemy.com/courses/office-productivity/",
				#"https://www.udemy.com/courses/marketing/"]
courseLinks = ["https://www.udemy.com/courses/business/"]
#Remove searchWords that are not required
#searchList = ["Development" , "Business", "IT and Software", "Office Productivity", "Marketing"]
searchList = ["Business"]
for searchWord in searchList:
	print("\n")
	print("Searching for: " + searchWord)
	courseNumber = 1
	#driver.get(courseLinks[clink])

	#Comment out the above line of code and uncomment the below code to star from a specific page
	#Change pageLimit variable accordingly

	driver.get("https://www.udemy.com/courses/business/?p=88")
	clink += 1

	try:
		pageLimitElement = WebDriverWait(driver, 20).until(
			lambda x: x.find_element(By.XPATH , "//span[@class='udlite-heading-sm pagination--page--3FKqV']")
			)
		
		#Change pageLimit here
		#Also take care of loop condition of pages

		#pageLimit = int(pageLimitElement.text)			#Use this to run for all pages
		pageLimit = 100                               	#Use this to run in batches
		startPage = 88							    #Change in case of specific pages 

														#Incase of running in batches, be sure to remove
														#the tables created in each batch run or they will
														#be overwritten

														#In case of any error, data will be stored in excel
														#Last page link and course link will be logged
		for pageNumber in range(startPage,pageLimit+1):
			levelPointer = 0
			levelList = []

			imgList = []
			imgPointer = 0
			# if courseNumber >= courseLimit:
			# 	print(courseLimit , " Limit Reached in " + searchWord)
			# 	break
			print("Page Number: " , pageNumber)
			try:
				elements = WebDriverWait(driver, 20).until(
						lambda x: x.find_elements(By.XPATH, "//div[@class='course-list--container--3zXPS']/div[@class='popper--popper--19faV popper--popper-hover--4YJ5J']/a[@class='udlite-custom-focus-visible browse-course-card--link--3KIkQ']")
					)
			except:
				continue
			currURL = driver.current_url
			print("Page link: ", currURL)
			links = []
			for element in elements:
				links.append(element.get_attribute('href'))
				imgsrc = element.find_element(By.XPATH,".//img[@class='course-card--course-image--2sjYP browse-course-card--image--35hYN']")
				imgsrc = imgsrc.get_attribute("src")
				#print(imgsrc)
				imgList.append(imgsrc)
				try:
					InfoElement = element.find_element(By.XPATH, ".//div[@class='udlite-text-xs course-card--row--1OMjg course-card--course-meta-info--1hHb3']")
					levelList.append(InfoElement.text.split("\n")[-1])
				except:
					levelList.append("No level given")
					continue
				
			for link in links:
				print ('Course Link: ' + link)
				#time.sleep(2)
				driver.get(link)	

				# Skip if course is already present
				# if link in coursesDict:
				# 	for i in range(len(MasterTableDict['Link'])):
				# 		if(MasterTableDict['Link'][i] == link):
				# 			MasterTableDict['Tags_(Field_of_Study)'][i] += ("," + searchWord)
				# 			break
				# 	print("Course Already Present. Tag Added. Skipping ...")
				# 	continue

				if driver.current_url != link:
					imgPointer += 1
					levelPointer += 1
					continue
				## ------------------------------ MASTER TABLE ---------------------------------##
				#----- Course Id ----- #
				coursesDict[link] = courseId
				MasterTableDict["Course_ID"].append(courseId)
				courseId += 1	
				#----- Course Id ----- #

				#---- Image Link -----#
				#print(imgList[imgPointer])
				MasterTableDict['Image_Link'].append(imgList[imgPointer])
				imgPointer += 1
				#---- Image Link -----#

				#---- Page -----#
				MasterTableDict['Page'].append(pageNumber)
				#---- Page -----#

				# #---- Source ID -----#
				# MasterTableDict['Source_ID'].append(2)
				# #---- Source ID -----#

				#---- Website -----#
				MasterTableDict['Website'].append('Udemy')
				#---- Website -----#

				#---- Pace -----#
				MasterTableDict['Pace'].append('Self Paced')
				#---- Pace -----#

				#---- Certificate -----#
				try:
					CertificateElement = WebDriverWait(driver,8).until(
						lambda x : x.find_element(By.XPATH,"//span[@data-purpose='incentive-certificate']")
					)
					MasterTableDict['Certificate'].append('Yes')
				except:
					MasterTableDict['Certificate'].append('No')
				#---- Certificate -----#

				#---- Link -----#
				MasterTableDict['Link'].append(link)
				#---- Link -----#

				#---- Week Titles -----#
				MasterTableDict['Week_Titles'].append("No Titles")
				#---- Week Titles -----#

				#---- Level -----#
				MasterTableDict['Level'].append(levelList[levelPointer])
				levelPointer += 1
				#---- Level -----#

				#---- Tags Field of Study -----#
				try:
					tagsElement = WebDriverWait(driver, 5).until(
						lambda x : x.find_elements(By.XPATH, "//div[@class='topic-menu udlite-breadcrumb']/a")
					)
					tagList = []
					for tags in tagsElement:
						tagList.append(tags.text)
					#print(tagList)
					MasterTableDict['Tags_(Field_of_Study)'].append(",".join(tagList))
				except:
					MasterTableDict['Tags_(Field_of_Study)'].append(searchWord)
				#---- Tags Field of Study -----#

				#----- Title ----- #
				try:
					titleElement = WebDriverWait(driver, 5).until(
						lambda x: x.find_element(By.XPATH, "//h1[@class='udlite-heading-xl clp-lead__title clp-lead__title--small']")
						)
					#print(titleElement.text)
					MasterTableDict['Title'].append(titleElement.text)
				except:
					MasterTableDict['Title'].append("No Title Given")
				#----- Title ----- #


				#----- Rating and Number of Ratings ----- #
				try:
					RatingElement = driver.find_element(By.XPATH, "//html/body[@id='udemy']/div[@class='main-content-wrapper']/div[@class='main-content']/div[@class='paid-course-landing-page__container']/div[@class='top-container dark-background']/div[@class='dark-background-inner-position-container']/div/div[@class='course-landing-page__main-content dark-background-inner-text-container'][2]/div[@class='clp-component-render']/div[@class='udlite-text-sm clp-lead']/div[@class='clp-lead__badge-ratings-enrollment']/div[@class='clp-lead__element-item clp-lead__element-item--row']/div[@class='clp-component-render'][1]/div[@class='clp-component-render']/div[@class='ud-component--course-landing-page-udlite--rating']/div[@class='styles--rating-wrapper--5a0Tr']")
					txtList = RatingElement.text.split("\n")
					space = txtList[-1].find(' ')
					numberOfRatings = txtList[-1][1:space]
					ratings = txtList[1]
					#print(ratings, numberOfRatings)
					MasterTableDict['Rating'].append(ratings)
					MasterTableDict['Number_of_Ratings'].append(numberOfRatings)
				except:
					MasterTableDict['Rating'].append("No ratings given")
					MasterTableDict['Number_of_Ratings'].append("No Number of Ratings given")
				#----- Rating and Number of Ratings ----- #

				#----- Enrolled -----#
				try:
					EnrolledElement = driver.find_element(By.XPATH , "//html/body[@id='udemy']/div[@class='main-content-wrapper']/div[@class='main-content']/div[@class='paid-course-landing-page__container']/div[@class='top-container dark-background']/div[@class='dark-background-inner-position-container']/div/div[@class='course-landing-page__main-content dark-background-inner-text-container'][2]/div[@class='clp-component-render']/div[@class='udlite-text-sm clp-lead']/div[@class='clp-lead__badge-ratings-enrollment']/div[@class='clp-lead__element-item clp-lead__element-item--row']/div[@class='clp-component-render'][2]/div")
					space = EnrolledElement.text.find(' ')
					txt = EnrolledElement.text[0:space]
					#print(txt)
					MasterTableDict['Enrolled_Students'].append(txt)
				except:
					MasterTableDict['Enrolled_Students'].append("No Enrolled Students")
				#----- Enrolled -----#

				#----- Offered By and Instructor + Provider ID-----#
				try:
					OfferedByElement = driver.find_element(By.XPATH, "//span[@class='instructor-links--names--7UPZj']")
					txtList = OfferedByElement.text[11:].split(',')
					#print(txtList)
					MasterTableDict['Offered_By'].append(",".join(txtList))
					MasterTableDict['Instructor'].append(",".join(txtList))
				except:
					MasterTableDict['Offered_By'].append("No Offered_By Given")
					MasterTableDict['Instructor'].append("No Instructor Given")
				# for txt in txtList:
				# 	if txt not in providerDict:
				# 		providerDict[txt] = providerId
				# 		providerId += 1
				# 	else:
				# 		continue
				#----- Offered By and Instructor + Provider ID-----#

				#----- Language -----#
				try:
					LanguageElement = driver.find_element(By.XPATH, "//div[@class='clp-lead__element-item clp-lead__locale' and @data-purpose='lead-course-locale']")
					txt = LanguageElement.text
					#print(txt) 
					MasterTableDict['Language'].append(txt)
				except:
					MasterTableDict['Language'].append("No Language Given")
				#----- Language -----#

				#----- Price -----#
				try:
					PriceElement = WebDriverWait(driver, 10).until(
						lambda x : x.find_element(By.XPATH, "/html/body[@id='udemy']/div[@class='main-content-wrapper']/div[@class='main-content']/div[@class='paid-course-landing-page__container']/div[@class='sidebar-container-position-manager']/div[@class='clp-component-render']/div[@class='clp-component-render']/div[@class='ud-component--course-landing-page-udlite--sidebar-container']/div[@class='course-landing-page_sidebar-container ']/div[@class='sidebar-container--content--gsvyJ']/div[@class='sidebar-container--content-group--1upV8'][1]/div[@class='sidebar-container--purchase-section--17KRp']/div[@class='generic-purchase-section--main-cta-container--3xxeM']/div[@class='generic-purchase-section--buy-box-main--siIXV']/div[@class='buy-box--buy-box--3d_i8']/div[@class='buy-box--buy-box-item--1Qbkl'][2]/div/div[@class='price-text--container--Ws-fP udlite-clp-price-text']/div[@class='price-text--price-part--Tu6MH udlite-clp-discount-price udlite-heading-xxl']/span[2]/span")
						)
					txt = PriceElement.text
					#print(txt)
					MasterTableDict['Price'].append(txt)
				except:
					MasterTableDict['Price'].append("No Price Given")
				#----- Price -----#


				#---- Time -----#
				try:
					TimeElement = WebDriverWait(driver, 2).until(
						lambda x : x.find_element(By.XPATH, "//div[@class='udlite-text-sm' and @data-purpose='curriculum-stats']/span[@class='curriculum--content-length--1XzLS']/span/span")
						)
					txt = TimeElement.text
					#print(txt)
					MasterTableDict['Time_(to_display)'].append(txt)
				except:
					MasterTableDict['Time_(to_display)'].append("No Time Given")
				#---- Time -----#


				#----- Pre-requisites -----#
				# try:
				# 	RequisiteElement = driver.find_element(By.XPATH, "//div[@class='ud-component--course-landing-page-udlite--requirements']/div/ul[@class='unstyled-list udlite-block-list']")
				# 	txt = RequisiteElement.text.split("\n")
					
				# 	txt = ",".join(txt)
				# 	print(txt)
				# 	MasterTableDict['Pre-requisite'].append(txt)
				# except:
				# 	MasterTableDict['Pre-requisite'].append("No Pre-requisite Given")
				MasterTableDict['Pre-requisite'].append("Null")
				#----- Pre-requisites -----#


				#----- Skill Tags -----#
				# try:
				# 	SkillElement = driver.find_element(By.XPATH, "//ul[@class='unstyled-list udlite-block-list what-you-will-learn--objectives-list--2cWZN']")
				# 	txt = SkillElement.text.split("\n")
					
				# 	txt = ",".join(txt)
				# 	print(txt)
				# 	MasterTableDict['Tags_(Tools_and_Tech)'].append(txt)
				# except:
				# 	MasterTableDict['Tags_(Tools_and_Tech)'].append("No Tags Given")
				MasterTableDict['Tags_(Tools_and_Tech)'].append("Null")
				#----- Skill Tags -----#

				#----- Description -----#
				try:
					DescriptionElement = driver.find_element(By.XPATH, "//div[@data-purpose='safely-set-inner-html:description:description']")
					#print(DescriptionElement.text)
					txt = DescriptionElement.text
					MasterTableDict['Description'].append(txt)
				except:
					MasterTableDict['Description'].append("No Description Given")
				#----- Description -----#

				## ------------------------------ MASTER TABLE ---------------------------------##

				## ------------------------------ COURSES TABLE ---------------------------------##
				CourseTableDict["Course_ID"].append(courseId-1)
				CourseTableDict['Title'].append(titleElement.text)

				#----- Pre-requisites -----#
				try:
					RequisiteElement = driver.find_element(By.XPATH, "//div[@class='ud-component--course-landing-page-udlite--requirements']/div/ul[@class='unstyled-list udlite-block-list']")
					txt = RequisiteElement.text.split("\n")
					
					txt = ",".join(txt)
					#print(txt)
					CourseTableDict['Pre-requisite'].append(txt)
				except:
					CourseTableDict['Pre-requisite'].append("No Pre-requisite Given")
				#----- Pre-requisites -----#


				#----- Skill Tags -----#
				try:
					SkillElement = driver.find_element(By.XPATH, "//ul[@class='unstyled-list udlite-block-list what-you-will-learn--objectives-list--2cWZN']")
					txt = SkillElement.text.split("\n")
					
					txt = ",".join(txt)
					#print(txt)
					CourseTableDict['Tags_(Tools_and_Tech)'].append(txt)
				except:
					CourseTableDict['Tags_(Tools_and_Tech)'].append("No Tags Given")
				#----- Skill Tags -----#

				## ------------------------------ COURSES TABLE ---------------------------------##

				## ------------------------------ REVIEW TABLE ---------------------------------##
				#----- Reviews -----#
				try:
					TotalReviewElement = WebDriverWait(driver, 3).until(
						lambda x : x.find_elements(By.XPATH, "//div[@class='reviews-section--review-container--3F3NE']")
					)
					currReviewNumber = 1
					for Review in TotalReviewElement:
						reviewList = Review.text.split("\n")
						if len(reviewList[0]) <= 2:
							currReviewName = reviewList[1]
							currReviewStars = reviewList[2]
							currReviewBody = reviewList[4]
						else:
							currReviewName = reviewList[0]
							currReviewStars = reviewList[1]
							currReviewBody = reviewList[3]
						#print(reviewList)
						#print(currReviewStars,currReviewBody)
						ReviewTableDict["Review_ID"].append(reviewId)
						ReviewTableDict["Course_ID"].append(courseId - 1)
						ReviewTableDict["Title"].append(titleElement.text)
						ReviewTableDict["Review_Name"].append(currReviewName)
						ReviewTableDict["Review_Rating"].append(currReviewStars)
						ReviewTableDict["Review_Body"].append(currReviewBody)
						reviewId += 1
						currReviewNumber += 1
						if(currReviewNumber == 3):	
							break

				except:
					print("No Reviews Available")	
				#----- Reviews -----#
				## ------------------------------ REVIEW TABLE ---------------------------------##


				#driver.back()
				# if courseNumber == courseLimit:
				# 	break
				# else:
				# 	courseNumber += 1

			driver.get(currURL)
			nextpage = WebDriverWait(driver, 10).until(
					lambda x: x.find_element(By.XPATH, "//a[@data-page='+1']")
			)
			nextpage.click()
			time.sleep(2)

	except:
		print("Error Found Somewhere")
		#driver.refresh()
		break


driver.close()
endTime = time.time()
print(endTime - startTime)

minVal = 1000
for arr in MasterTableDict:
	minVal = min(minVal, len(MasterTableDict[arr]))
for arr in MasterTableDict:
	while len(MasterTableDict[arr]) > minVal:
		MasterTableDict[arr].pop()

minVal = 1000
for arr in CourseTableDict:
	minVal = min(minVal, len(CourseTableDict[arr]))
for arr in CourseTableDict:
	while len(CourseTableDict[arr]) > minVal:
		CourseTableDict[arr].pop()

#----- OUTPUT TO EXCEL FILE -----#

MasterDf = pd.DataFrame.from_dict(MasterTableDict)
MasterDf.to_excel("udemy_MasterTablenew.xlsx")

courseDf = pd.DataFrame.from_dict(CourseTableDict)
courseDf.to_excel("udemy_Courses_Tablenew.xlsx")

reviewDf = pd.DataFrame.from_dict(ReviewTableDict)
reviewDf.to_excel("udemy_Review_Tablenew.xlsx")

#----- OUTPUT TO EXCEL FILE -----#

