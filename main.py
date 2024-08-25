import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
score = os.getenv("SCORE")

def setUpDriver():
    driver = webdriver.Chrome()
    return driver

def login(driver):
    driver.get("https://online.mis.pens.ac.id")
    driver.find_element(By.CSS_SELECTOR, "a[title='login']").click()
    driver.find_element(By.CSS_SELECTOR, "a[title='login mahasiswa/dosen/staff']").click()
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='submit']")))
    
    input_username = driver.find_element(By.ID, "username")
    input_username.send_keys(username)
    
    input_password = driver.find_element(By.ID, "password")
    input_password.send_keys(password)
    
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

def fill_questionnaires(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "cbMatakuliah")))
    
    select_element = driver.find_element(By.ID, "cbMatakuliah")
    select = Select(select_element)
    
    for i in range(1, len(select.options)):
        select.select_by_index(i)
        
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div/div[3]/table/tbody/tr[1]/td/div/table[3]/tbody/tr/td/h3")))
        driver.find_element(By.ID, "Simpan").click()
        
        for radio in driver.find_elements(By.XPATH, f"//input[@value='{score}']"):
            radio.click()

        driver.find_element(By.ID, "Simpan").click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='tdData']/span")))
        
        driver.get('https://online.mis.pens.ac.id')

def navigate_to_theory_quetionnaires(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='logout']")))
    
    driver.find_element(By.XPATH, "//a[text()='Non Akademik']").click()
    driver.find_element(By.CSS_SELECTOR, "a[href='mQuiz_Intro_Teori.php']").click()
    
    wait.until(EC.visibility_of_element_located(By.XPATH, "a[text()='Klik disini untuk melanjutkan']"))    
    driver.find_element(By.XPATH, "a[text()='Klik disini untuk melanjutkan']").click()

def logout(driver):
    driver.find_element(By.CSS_SELECTOR, "a[title='logout']").click()
    
def tearDownDriver(driver):
    driver.close()

def main():
    driver = setUpDriver()
    login(driver)
    navigate_to_theory_quetionnaires(driver)
    logout(driver)
    tearDownDriver(driver)
    
if __name__ == "__main__":
    main()