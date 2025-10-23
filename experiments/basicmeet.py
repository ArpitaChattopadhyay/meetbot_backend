from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# ---------- CONFIGURATION ----------
MEET_LINK = "https://meet.google.com/rzc-wacw-zmx"  # Replace with your link
EMAIL = "tanjirodemon@gmail.com"
PASSWORD = "demonslayer21"
# -----------------------------------

def join_google_meet():
    options = Options()
    options.add_argument(r"--user-data-dir=C:\Users\hp\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--profile-directory=Default")  # or "Profile 1"
    options.add_argument("--use-fake-ui-for-media-stream")  # Avoid mic/cam prompts
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_mic": 2,
                                              "profile.default_content_setting_values.media_stream_camera": 2,
                                              "profile.default_content_setting_values.notifications": 2})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Step 1: Go to Google Login Page
    driver.get("https://accounts.google.com/")
    wait = WebDriverWait(driver, 15)

    # Step 2: Login with email
    email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_input.send_keys(EMAIL)
    driver.find_element(By.ID, "identifierNext").click()

    # Step 3: Wait for password field to appear
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
    password_input.send_keys(PASSWORD)
    driver.find_element(By.ID, "passwordNext").click()


    # Step 3: Open the Meet link
    driver.get(MEET_LINK)
    time.sleep(10)

    # Step 4: Turn off mic and camera before joining
    try:
        mic_button = driver.find_element(By.XPATH, '//div[@aria-label="Turn off microphone (ctrl + d)"]')
        cam_button = driver.find_element(By.XPATH, '//div[@aria-label="Turn off camera (ctrl + e)"]')
        mic_button.click()
        cam_button.click()
    except:
        pass

    # Step 5: Click the Join button
    try:
        join_button = driver.find_element(By.XPATH, '//button[@aria-label="Join now"]')
        join_button.click()
        print("✅ Successfully joined the meeting!")
    except:
        print("⚠️ Could not find join button")

    # Keep the browser open (e.g., for 60 mins)
    time.sleep(3600)
    driver.quit()


if __name__ == "__main__":
    join_google_meet()
