import time
import threading
import asyncio
import warnings
import indian_names
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.opera import OperaDriverManager

warnings.filterwarnings('ignore')
MUTEX = threading.Lock()
executable_path = OperaDriverManager().install()
print(executable_path)

running = True  # Added a global variable to control the main loop


def sync_print(text):
    with MUTEX:
        print(text)


def get_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_experimental_option('w3c', True)
    driver = webdriver.Chrome(executable_path=executable_path, options=options)
    return driver


def driver_wait(driver, locator, by, secs=10, condition=ec.element_to_be_clickable):
    wait = WebDriverWait(driver=driver, timeout=secs)
    element = wait.until(condition((by, locator)))
    return element


def start(name, user, wait_time, meetingcode, passcode):
    print(f"{name} started!")

    driver = get_driver()  # Create a new driver instance for each thread
    driver.get(f'https://zoom.us/wc/join/{meetingcode}')

    try:
        query = '//button[@id="onetrust-accept-btn-handler"]'
        accept_button = driver_wait(driver, query, By.XPATH, secs=5000)
        accept_button.click()
    except Exception as e:
        pass

    try:
        query = '//button[@id="wc_agree1"]'
        agree_button = driver_wait(driver, query, By.XPATH, secs=5000)
        agree_button.click()
    except Exception as e:
        pass

    try:
        query = 'input[type="text"]'
        username_input = driver_wait(driver, query, By.CSS_SELECTOR, secs=200000)
        username_input.send_keys(user)

        query = 'input[type="password"]'
        password_input = driver_wait(driver, query, By.CSS_SELECTOR, secs=200000)
        password_input.send_keys(passcode)

        query = 'button.preview-join-button'
        join_button = driver_wait(driver, query, By.CSS_SELECTOR, secs=200000)
        join_button.click()
    except Exception as e:
        pass

    try:
        query = '//button[text()="Join Audio by Computer"]'
        mic_button_locator = driver_wait(driver, query, By.XPATH, secs=35000)
        mic_button_locator.click()
        print(f"{name} mic aayenge.")
    except Exception as e:
        print(f"{name} mic nahe aayenge. ", e)

    print(f"{name} sleep for {wait_time} seconds ...")
    while running and wait_time > 0:
        time.sleep(1)
        wait_time -= 1
    print(f"{name} ended!")
    driver.quit()  # Quit the driver after the thread has completed


def main():
    global running
    wait_time = sec * 90
    workers = []

    for i in range(number):
        try:
            proxy = proxylist[i]
        except Exception:
            proxy = None
        try:
            user = indian_names.get_full_name()
        except IndexError:
            break
        start(f'[Thread{i}]', user, wait_time, meetingcode, passcode)


if __name__ == '__main__':
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")
    sec = 60
    try:
        main()
    except:
        running = False  # Stop the main loop if an exception occurs
