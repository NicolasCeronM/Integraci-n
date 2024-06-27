from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('http://127.0.0.1:8000/')
time.sleep(3)

buscador = driver.find_element(By.XPATH,'//*[@id="busqueda"]/div/input')
buscador.send_keys('Martillo')
time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="busqueda"]/div/span/button').click()
time.sleep(5)

driver.find_element(By.XPATH,'/html/body/div[2]/div[4]/div[1]/div/a').click()
time.sleep(5)

driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/a').click()
time.sleep(5)

username = driver.find_element(By.XPATH,'//*[@id="id_username"]')
password = driver.find_element(By.XPATH,'//*[@id="id_password"]')

username.send_keys('testuser')
password.send_keys('hola1133')
time.sleep(3)
driver.find_element(By.XPATH,'/html/body/div/div/div/div/div/form/div[3]/div[2]/button').click()
time.sleep(5)
driver.quit()