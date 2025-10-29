# File: tests/test_login.py
import time
import pytest
from selenium.webdriver.common.by import By

# ---------- Setup ----------
# def test_admin_login(setup):
#     driver = setup
#     driver.get("https://uat-readygrocery.razinsoft.com/admin/login")
#     time.sleep(1)  # wait for page load

def test_admin_login(setup, base_url):
    driver = setup
    driver.get(base_url)   # ✅ এখানে আমরা conftest.py থেকে URL নিচ্ছি
    time.sleep(1)

    # ---------- STEP 1: Try copy button auto-fill ----------
    try:
        copy_btn = driver.find_element(By.CLASS_NAME, "copyBtn")
        driver.execute_script("arguments[0].click();", copy_btn)
        print("✅ Copy button clicked, credentials auto-filled")
        time.sleep(1)
    except Exception as e:
        print(f"⚠️ Copy button not found, filling manually. Error: {e}")

    # ---------- STEP 2: Fill email & password manually (fallback) ----------
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    email_field.clear()
    email_field.send_keys("root@grocery.com")
    password_field.clear()
    password_field.send_keys("secret@123")

    # ---------- STEP 3: Click Login ----------
    login_button = driver.find_element(By.CSS_SELECTOR, "button.loginButton")
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(2)

    # ---------- STEP 4: Validation & Screenshot ----------
    current_url = driver.current_url
    if "/admin" in current_url:
        driver.save_screenshot("reports/login_success.png")
        print("✅ Login Successful")
        assert True
    else:
        driver.save_screenshot("reports/login_failed.png")
        print("❌ Login Failed")
        assert False, f"Unexpected URL: {current_url}"
    # ---------- STEP 5: Close Browser ----------
    driver.quit()

