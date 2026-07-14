from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # exécution sans interface

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.python.org")
print(driver.title)  # devrait afficher "Welcome to Python.org"
driver.quit()
