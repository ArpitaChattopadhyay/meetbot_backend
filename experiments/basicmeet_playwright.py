from playwright.sync_api import sync_playwright
import time

# ==== CONFIGURATION ====
MEET_LINK = "https://meet.google.com/rzc-wacw-zmx"  # Replace with your meet link
CHROME_PROFILE_PATH = r"C:\Users\hp\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Default"  # or "Profile 1", etc.
BOT_NAME = "MeetBot"
REPRESENTING = "Soumyajit Datta"  # 👈 Change this to who the bot represents
STAY_DURATION = 60 * 60  # seconds (1 hour)
# =======================


def join_google_meet():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=f"{CHROME_PROFILE_PATH}\\{PROFILE_NAME}",
            headless=False,
            args=[
                "--use-fake-ui-for-media-stream",
                "--disable-infobars",
                "--disable-notifications",
                "--start-maximized",
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        page = browser.new_page()
        print("🌐 Opening Google Meet...")
        page.goto(MEET_LINK)
        page.wait_for_load_state("networkidle")

        # Wait for UI to fully load
        time.sleep(5)

        # Step 1: Fill name if “What’s your name?” field appears
        try:
            name_input = page.locator('input[aria-label*="name"]')
            if name_input.count() > 0:
                name_input.fill(BOT_NAME)
                print(f"🧠 Filled name as: {BOT_NAME}")
        except Exception as e:
            print("⚠️ Could not fill name field:", e)

        # Step 2: Turn off microphone
        try:
            mic_button = page.locator('div[aria-label*="microphone"], button[aria-label*="microphone"]')
            if mic_button.count() > 0:
                mic_button.nth(0).click()
                print("🎤 Microphone turned off.")
        except Exception as e:
            print("⚠️ Could not disable microphone:", e)

        # Step 3: Turn off camera
        try:
            cam_button = page.locator('div[aria-label*="camera"], button[aria-label*="camera"]')
            if cam_button.count() > 0:
                cam_button.nth(0).click()
                print("📷 Camera turned off.")
        except Exception as e:
            print("⚠️ Could not disable camera:", e)

        # Step 4: Click “Join now” or “Ask to join”
        try:
            join_now = page.locator('button:has-text("Join now")')
            ask_to_join = page.locator('button:has-text("Ask to join")')

            if join_now.count() > 0:
                join_now.first.click()
                print("✅ Joined meeting instantly!")
            elif ask_to_join.count() > 0:
                ask_to_join.first.click()
                print("🚪 Sent join request (waiting for host approval).")
            else:
                print("⚠️ Could not find Join button.")
        except Exception as e:
            print("⚠️ Could not click Join button:", e)

        # Wait briefly after joining
        time.sleep(8)

        # Step 5: Send polite disclaimer messages in chat
        try:
            print("💬 Sending disclaimer messages...")
            chat_button = page.locator('button[aria-label*="Chat"], div[aria-label*="Chat"]')
            chat_button.first.click()
            time.sleep(2)

            # Locate chat input
            chat_box = page.locator('textarea[aria-label*="Send a message"], div[aria-label*="Send a message"]')

            messages = [
                f"👋 Hi everyone, I’m {BOT_NAME}.",
                f"I’m an AI assistant attending on behalf of {REPRESENTING}.",
                "I’ll be recording this conversation. Please let me know if you have any concerns. 😊"
            ]

            for msg in messages:
                chat_box.fill(msg)
                page.keyboard.press("Enter")
                time.sleep(2)

            print("✅ Disclaimer messages sent.")
        except Exception as e:
            print("⚠️ Could not send chat messages:", e)

        # Step 6: Stay in the meeting
        print(f"⏳ Staying in meeting for {STAY_DURATION // 60} minutes...")
        time.sleep(STAY_DURATION)

        browser.close()
        print("👋 MeetBot has left the meeting.")


if __name__ == "__main__":
    join_google_meet()
