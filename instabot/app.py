# import autoit
import pyautogui
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

username = "gaaans_tolle_email@web.de"  # Enter your username
password = "ganstollespasswort"  # Enter your password
image_path = r"~/Downloads/image.png"  # The written path is just an example, Delete the path and Enter the Path of your image. #1. path should not start with a back slash
caption = "gaaaans toll"  # Enter the caption

mobile_emulation = {"deviceName": "Pixel 2"}
opts = webdriver.ChromeOptions()
opts.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(
    executable_path=r"/usr/bin/chromedriver", options=opts
)  # you must enter the path to your driver

main_url = "https://www.instagram.com"
wait = WebDriverWait(driver, 5)
driver.get(main_url)
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")


def login():
    cookie_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/button[1]"))
    )
    cookie_button.click()
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Log In')]",))
    )
    login_button.click()
    username_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='username']"))
    )
    username_input.send_keys(username)
    password_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='password']"))
    )
    password_input.send_keys(password)
    password_input.submit()

    while EC.text_to_be_present_in_element(
        (By.XPATH, '//*[@id="slfErrorAlert"]'),
        "We couldn't connect to Instagram. Make sure you're connected to the internet and try again.",
    ):
        if EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="slfErrorAlert"]'),
            "Please wait a few minutes before you try again.",
        ):
            sleep(10)

        sleep(0.5)
        try:
            password_input.submit()
        except:
            break
        print("Login failed")


login()


def close_reactivated():
    try:
        not_now_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Not Now')]"))
        )
        not_now_btn.click()
    except:
        pass


close_reactivated()


def close_notification():
    try:
        close_noti_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Not Now')]")
            )
        )
        close_noti_btn.click()
    except:
        pass


close_notification()


def close_add_to_home():
    close_addHome_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Cancel')]"))
    )
    close_addHome_btn.click()


close_add_to_home()

close_notification()

# new_post_btn = driver.find_element_by_xpath("//div[@role='menuitem']").click()
new_post_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@role='menuitem']",))
)
new_post_btn.click()
sleep(10)
with pyautogui.hold("ctrlright"):
    pyautogui.press("l")

sleep(2)
pyautogui.write("home/user/Downloads/image.png")
sleep(1.5)
pyautogui.press("enter")
# autoit.win_active("Open")
# autoit.control_send("Open", "Edit1", image_path)
# autoit.control_send("Open", "Edit1", "{ENTER}")

sleep(2)

next_btn = driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()

sleep(1.5)

caption_field = driver.find_element_by_xpath(
    "//textarea[@aria-label='Write a caption…']"
)
caption_field.send_keys(caption)

share_btn = driver.find_element_by_xpath("//button[contains(text(),'Share')]").click()

sleep(25)

driver.close()
