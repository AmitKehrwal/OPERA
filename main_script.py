import time
import concurrent.futures
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.opera import OperaDriverManager

import indian_names

number = int(input("Enter number of Users: "))
meetingcode = input("Enter meeting code (No Space): ")
passcode = input("Enter Password (No Space): ")
sec = 60

executable_path = OperaDriverManager().install()


def sync_print(text):
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


def driver_wait(driver, locator, by, secs=10, condition=EC.element_to_be_clickable):
    wait = WebDriverWait(driver=driver, timeout=secs)
    element = wait.until(condition((by, locator)))
    return element


async def start(name, wait_time):
    user = indian_names.get_full_name()
    sync_print(f"{name} started!")
    driver = get_driver()

    try:
        driver.get(f'https://zoom.us/wc/join/{meetingcode}')
        time.sleep(10)

        inp = driver.find_element(By.XPATH, '//input[@type="text"]')
        inp.send_keys(f"{user}")
        time.sleep(5)

        inp2 = driver.find_element(By.XPATH, '//input[@type="password"]')
        inp2.send_keys(passcode)

        join_button = driver.find_element(By.XPATH, '//button[contains(@class,"preview-join-button")]')
        driver.execute_script("arguments[0].click();", join_button)

        query = '//button[text()="Join Audio by Computer"]'
        mic_button_locator = driver_wait(driver, query, By.XPATH, secs=60)
        mic_button_locator.click()
        sync_print(f"{name} mic aayenge.")

        sync_print(f"{name} sleep for {wait_time} seconds ...")
        while wait_time > 0:
            await asyncio.sleep(1)
            wait_time -= 1
        sync_print(f"{name} ended!")

    except Exception as e:
        sync_print(f"{name} failed: {e}")

    finally:
        driver.quit()


async def main():
    wait_time = sec * 90
    workers = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=number) as executor:
        loop = asyncio.get_running_loop()
        tasks = [loop.run_in_executor(executor, start, f'[Thread{i}]', wait_time) for i in range(number)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
