import time
import threading
import asyncio
import warnings

from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.opera.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.opera import OperaDriverManager

warnings.filterwarnings('ignore')
fake = Faker('en_IN')
MUTEX = threading.Lock()
executable_path = OperaDriverManager().install()
print(executable_path)


def sync_print(text):
    with MUTEX:
        print(text)


def getMIC(driver):
    print("Accessing Mic")
    pass


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


async def start(name, user, passcode, wait_time):
    sync_print(f"{name} started!")
    driver = get_driver()  # Create a new driver instance for each thread
    driver.get(f'https://zoom.us/wc/join/{meetingcode}')
    time.sleep(10)
    inp = driver.find_element(By.XPATH, '//input[@type="text"]')
    time.sleep(1)
    inp.send_keys(f"{user}")
    time.sleep(5)

    inp2 = driver.find_element(By.XPATH, '//input[@type="password"]')
    time.sleep(2)
    inp2.send_keys(passcode)

    # Click the "Join" button using JavaScript
    join_button = driver.find_element(By.XPATH, '//button[contains(@class,"preview-join-button")]')
    driver.execute_script("arguments[0].click();", join_button)

    try:
        query = '//button[text()="Join Audio by Computer"]'
        mic_button_locator = driver_wait(driver, query, By.XPATH, secs=35000)
        mic_button_locator.click()
        print(f"{name} mic aayenge.")
    except Exception as e:
        print(f"{name} mic nahe aayenge. ", e)

    sync_print(f"{name} sleep for {wait_time} seconds ...")
    while wait_time > 0:
        await asyncio.sleep(1)
        wait_time -= 1
    sync_print(f"{name} ended!")
    driver.quit()  # Quit the driver after the thread has completed


def main():
    wait_time = sec * 90
    workers = []

    for i in range(number):
        try:
            proxy = proxylist[i]
        except Exception:
            proxy = None
        try:
            user = fake.name()
        except IndexError:
            break
        wk = threading.Thread(target=asyncio.run, args=(start(f'[Thread{i}]', user, passcode, wait_time),))
        workers.append(wk)
    for wk in workers:
        wk.start()
    for wk in workers:
        wk.join()


if __name__ == '__main__':
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")
    sec = 60
    try:
        main()
    except:
        pass
