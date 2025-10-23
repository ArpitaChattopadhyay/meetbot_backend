"""
meetbot.py

Usage:
    python meetbot.py "<meet_link>" "youremail@gmail.com" "yourpassword"

Notes:
* Install dependencies: pip install selenium webdriver-manager
* Preferably run with a clean test account or use user-data-dir to reuse a logged-in session.
* This script cannot bypass 2FA or CAPTCHA.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(reuse_profile_path: str | None = None, headless: bool = False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")

    if reuse_profile_path:
        chrome_options.add_argument(f"--user-data-dir={reuse_profile_path}")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    # ✅ FIXED LINE BELOW:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    return driver



def login_google(driver, email: str, password: str, timeout=30):
    wait = WebDriverWait(driver, timeout)
    driver.get("https://accounts.google.com/ServiceLogin")

    # Enter email
    email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_input.clear()
    email_input.send_keys(email)
    email_input.send_keys(Keys.ENTER)

    # Wait for password field
    try:
        pwd_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    except Exception as e:
        print("Could not find password input. Google may be challenging login (CAPTCHA/2FA).")
        raise

    time.sleep(0.5)
    pwd_input.clear()
    pwd_input.send_keys(password)
    pwd_input.send_keys(Keys.ENTER)

    # Wait until we reach an account page or Gmail (simple success check)
    try:
        wait.until(EC.url_contains("myaccount.google.com"), timeout=10)
        print("Login appears successful (redirected to myaccount).")
    except Exception:
        # Try a looser check: presence of Google account avatar or top bar
        time.sleep(3)
        print("Login attempted. If Google requested 2FA/CAPTCHA this script cannot continue automatically.")


def join_meet(driver, meet_link: str, timeout=30):
    wait = WebDriverWait(driver, timeout)
    # Go to the Meet link
    driver.get(meet_link)

    # Wait for page to load with preview controls; this varies by UI
    time.sleep(4)  # give time for camera/mic preview to load

    # Try to dismiss camera/mic permission dialogs (browser-level popups cannot be clicked by page JS)
    # If you run into permission prompts, pre-set Chrome prefs or run with an existing profile where permissions are given.

    # Try to turn off camera and microphone (if present)
    try:
        # Buttons are sometimes buttons with aria-labels "Turn off camera" or "Turn off microphone"
        for label_part in ["Turn off microphone", "Turn off camera", "microphone off", "camera off"]:
            try:
                btn = driver.find_element(By.XPATH, f"//div[@aria-label[contains(.,'{label_part}')]]")
                btn.click()
            except Exception:
                pass
    except Exception:
        pass

    # Attempt to click "Join now" or "Ask to join"
    joined = False
    join_xpaths = [
        "//span[contains(text(),'Join now')]/ancestor::button",
        "//span[contains(text(),'Ask to join')]/ancestor::button",
        "//button[@aria-label='Join call']",
        "//div[contains(@aria-label,'Join') and @role='button']",
        "//button[contains(., 'Join')]",
    ]
    for xp in join_xpaths:
        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, xp)), timeout=7)
            btn.click()
            print("Clicked join button using xpath:", xp)
            joined = True
            break
        except Exception:
            continue

    if not joined:
        # Fall back: try pressing Enter (sometimes join button focused)
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ENTER)
            print("Sent ENTER as fallback to join.")
        except Exception:
            print("Could not find a join button. The Meet UI may have changed.")

    # After joining, wait a bit
    time.sleep(5)
    print("Join attempt finished. Verify in the browser whether you've joined successfully.")


def main():

    meet_link = "https://meet.google.com/rzc-wacw-zmx"
    email = "tanjirodemon608@gmail.com"
    password = "demonslayer21"

    # Optionally set a path to reuse your Chrome profile (helps avoid repeated login)
    reuse_profile = None
    # reuse_profile = "/path/to/chrome/profile"  # uncomment/set if desired

    driver = create_driver(reuse_profile_path=reuse_profile, headless=False)
    try:
        login_google(driver, email, password)
        join_meet(driver, meet_link)
    except Exception as e:
        print("Error during automation:", e)
    finally:
        # keep browser open a bit for inspection
        print("Bot finished — keeping browser open for 30 seconds for inspection.")
        time.sleep(30)
        driver.quit()


if __name__ == "__main__":
    main()