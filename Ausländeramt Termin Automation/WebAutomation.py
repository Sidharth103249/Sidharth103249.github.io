import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process

def send_telegram_notification(message):
    TELEGRAM_BOT_TOKEN = ""
    TELEGRAM_CHAT_ID = "" 
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_appointment_1():
    driver = webdriver.Chrome()

    driver.get("https://termine.staedteregion-aachen.de/auslaenderamt/")

    button_cookies = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cookie_msg_btn_no"))
    )
    button_cookies.click()

    button_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "buttonfunktionseinheit-1"))
    )
    button_1.click()

    button_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "header_concerns_accordion-461"))
    )
    button_2.click()

    button_3 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "button-plus-310"))
    )
    button_3.click()

    button_4 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "WeiterButton"))
    )
    button_4.click()

    button_5 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "OKButton"))
    )
    button_5.click()

    button_6 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Ausländeramt Aachen - Aachen Arkaden, Trierer Straße 1, Aachen auswählen"]'))
    )
    button_6.click()

    button_7 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "filter_accordion"))
    )
    button_7.click()

    calendar_button_bis = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='filter_date_to'] + button"))
    )
    calendar_button_bis.click()

    prev_month_button_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui-datepicker-prev"))
    )
    prev_month_button_1.click()
    prev_month_button_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui-datepicker-prev"))
    )
    prev_month_button_2.click()
    prev_month_button_3 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui-datepicker-prev"))
    )
    prev_month_button_3.click()

    button_8 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Freitag, 28. Februar 2025"]'))
    )
    button_8.click()
    button_9 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Filtern']"))
    )
    button_9.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    try:
        error_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Kein freier Termin verfügbar')]")
        print("Found the error message: 'Kein freier Termin verfügbar1'")
        
        time.sleep(2)
        print("Quitting browser")
        driver.quit()
        time.sleep(60)
        check_appointment_1()
    except:
        print("Appointment available")
        send_email_notification("Infostelle - Appointment Available!", "An Infostelle appointment has become available. Book it quickly!")
        time.sleep(60)
        check_appointment_1()


def check_appointment_2():
    driver = webdriver.Chrome()

    driver.get("https://termine.staedteregion-aachen.de/auslaenderamt/")

    button_cookies = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cookie_msg_btn_no"))
    )
    button_cookies.click()

    button_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "buttonfunktionseinheit-1"))
    )
    button_1.click()

    button_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "header_concerns_accordion-455"))
    )
    button_2.click()

    button_3 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "button-plus-286"))
    )
    button_3.click()

    button_4 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "WeiterButton"))
    )
    button_4.click()

    button_5 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "OKButton"))
    )
    button_5.click()

    button_6 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Ausländeramt Aachen - Außenstelle RWTH auswählen"]'))
    )
    button_6.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    try:
        error_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Kein freier Termin verfügbar')]")
        print("No Visa Extension Appointments available")
        
        time.sleep(2)
        print("Quitting Visa Extension browser")
        driver.quit()
        time.sleep(60)
        check_appointment_2()
    except:
        print("Visa Extension Appointment available")
        send_email_notification("Visa extension - Appointment Available!", "A visa extension appointment has become available. Book it quickly!")
        time.sleep(60)
        check_appointment_2()

if __name__ == "__main__":
    # check_appointment_1()
    process1 = Process(target=check_appointment_1)
    process2 = Process(target=check_appointment_2)

    process1.start()
    process2.start()

    process1.join()
    process2.join()
