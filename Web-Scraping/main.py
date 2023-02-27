from selenium import webdriver  # allow launching browser
from selenium.webdriver.common.by import By  # allow search with parameters
from selenium.webdriver.support.ui import (
    WebDriverWait,
)  # allow waiting for page to load
from selenium.webdriver.support import (
    expected_conditions as EC,
)  # determine whether the web page has loaded
from selenium.common.exceptions import TimeoutException  # handling timeout situation
from selenium.webdriver.chrome.service import Service
import pandas as pd

driver_options = webdriver.ChromeOptions()
driver_options.add_argument(" --incognito")
chromedriver_path = "/usr/bin/chromedriver"
service = Service(executable_path=chromedriver_path)


def create_webdriver():
    return webdriver.Chrome(service=service, options=driver_options)


# Get the topics from user
topics = input("Enter the topic you'd like to search on github collections: ")
get_topics = topics.replace(" ", "-")

# Open the website
browser = create_webdriver()
browser.get("https://github.com/collections/" + get_topics)

# Extract all projects
projects = browser.find_elements(By.XPATH, "//h1[@class='h3 lh-condensed']")

# Check if the input topic is in github collection or not, if not then it
# quits.
if len(projects) == 0:
    print("No collections found")
    browser.quit()
    exit()

# Extract information for each project
project_list = {}
for proj in projects:
    proj_name = proj.text  # Project name
    proj_url = proj.find_elements(By.XPATH, "a")[0].get_attribute("href")
    project_list[proj_name] = proj_url

# Close connection
browser.quit()

# Extracting data
project_df = pd.DataFrame.from_dict(project_list, orient="index")

# Manipulate the table
project_df["project_name"] = project_df.index
project_df.columns = ["project_url", "project_name"]
project_df = project_df.reset_index(drop=True)

# Export project dataframe to CSV file of your input
project_df.to_csv(get_topics + ".csv")
