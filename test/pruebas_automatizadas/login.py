from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('http://127.0.0.1:8000/')
time.sleep(3)

inicio_sesion = driver.find_element(By.XPATH, '//*[@id="navbarSupportedContent"]/a[1]')
inicio_sesion.click()
time.sleep(2)
username = driver.find_element(By.XPATH,'//*[@id="id_username"]')
password = driver.find_element(By.XPATH,'//*[@id="id_password"]')

username.send_keys('testuser')
password.send_keys('hola1133')
time.sleep(3)
driver.find_element(By.XPATH,'/html/body/div/div/div/div/div/form/div[3]/div[2]/button').click()
time.sleep(5)
driver.quit()