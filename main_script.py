import time
import threading
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import indian_names

warnings.filterwarnings('ignore')
MUTEX = threading.Lock()
executable_path = ChromeDriverManager().install()
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
    options.add_experimental_option('w3c', True)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.binary_location = '/usr/bin/brave-browser'
    options.add_argument(f'--marionette-port=2828')  # Specify the port number here
    driver = webdriver.Chrome(executable_path=executable_path, options=options)
    return driver


def driver_wait(driver, locator, by, secs=10, condition=ec.element_to_be_clickable):
    wait = WebDriverWait(driver=driver, timeout=secs)
    element = wait.until(condition((by, locator)))
    return element


def start(name, proxy, user, wait_time):
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

    sync_print(f"{name} sleep for {wait_time} seconds ...")
    time.sleep(wait_time)
    sync_print(f"{name} ended!")
    driver.quit()  # Quit the driver after the thread has completed


def main():
    wait_time = sec * 60
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
        wk = threading.Thread(target=start, args=(
            f'[Thread{i}]', proxy, user, wait_time))
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
