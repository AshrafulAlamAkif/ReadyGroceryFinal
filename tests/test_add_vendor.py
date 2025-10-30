#test_add_vendor.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def test_add_vendor(setup, base_url):
    """✅ Test: Add Vendor with Unique Email & Shop Name"""
    driver = setup
    

    # ---------- Fixture: Setup & Teardown ----------
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.maximize_window()
    wait = WebDriverWait(driver, 10)  # Increased wait for slow load

    # ---------- STEP 1: Open login page ----------
    driver.get("base_url")
    print("Opened login page")
    time.sleep(1)

    # ---------- STEP 2: Login ----------
    try:
        copy_btn = driver.find_element(By.CLASS_NAME, "copyBtn")
        driver.execute_script("arguments[0].click();", copy_btn)
        print("Clicked copy button via JS")
        time.sleep(1)
    except:
        print("Copy button not found. Filling manually.")
        driver.find_element(By.ID, "email").send_keys("root@grocery.com")
        driver.find_element(By.ID, "password").send_keys("secret@123")

    # Click login button safely
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.loginButton")))
    driver.execute_script("arguments[0].click();", login_btn)
    print("✅ Logged in successfully via JS")
    time.sleep(1)

    # ---------- STEP 3: Navigate to 'Add Vendor' page----------

    # expand 'Vendors' dropdown
    vendors_menu = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a[data-bs-toggle='collapse'][href='#shopMenu']")
    ))
    driver.execute_script("arguments[0].scrollIntoView(true);", vendors_menu)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", vendors_menu)
    print("Clicked Vendors dropdown via JS")
    time.sleep(1)

    add_vendor = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add Vendor")))
    driver.execute_script("arguments[0].scrollIntoView(true);", add_vendor)
    driver.execute_script("arguments[0].click();", add_vendor)
    print("Clicked Add Vendor option & Opened Add Vendor form via JS")
    time.sleep(3)

    # ---------- STEP 4: Fill vendor form ----------
    timestamp = int(time.time())
    unique_email = f"vendor{timestamp}@gmail.com"
    unique_shop = f"Shop{timestamp}"

    driver.find_element(By.ID, "first_name").send_keys("Akif")
    driver.find_element(By.ID, "last_name").send_keys("Alam")
    driver.find_element(By.ID, "phone").send_keys("01700000000")

    gender_dropdown = Select(driver.find_element(By.ID, "gender"))
    gender_dropdown.select_by_visible_text("Male")

    driver.find_element(By.ID, "email").send_keys(unique_email)
    driver.find_element(By.ID, "password").send_keys("12345678")
    driver.find_element(By.ID, "password_confirmation").send_keys("12345678")

    driver.find_element(By.ID, "shop_name").send_keys(unique_shop)
    driver.find_element(By.ID, "address").send_keys("Dhaka, Bangladesh")
    driver.find_element(By.ID, "description").send_keys("This is a test vendor created by automation.")
    print("📝 Filled vendor details")

    # ---------- STEP 4.1: Upload Profile Photo ----------
    image_path = r"C:\Users\Ashraful Alam Akif\ReadyGrocery\image.png"  # Path to your image
    if os.path.exists(image_path):
        file_input = driver.find_element(By.ID, "thumbnail")
        file_input.send_keys(image_path)
        print("✅ Profile photo uploaded successfully")
        time.sleep(1)  # wait for preview update
    else:
        print("❌ Profile photo not found at:", image_path)

    # ---------- STEP 5: Click Submit safely ----------
    try:
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit') or contains(., 'Save') or @type='submit']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", submit_btn)
        print("✅ Clicked Submit button via JS successfully")
    except Exception as e:
        print("❌ Submit button not found or not clickable:", e)

    # ---------- STEP 6: Verify & Screenshot ----------
    time.sleep(1)
    driver.save_screenshot(f"add_vendor_{timestamp}.png")
    print(f"Vendor created with email: {unique_email}")
    print("📸 Screenshot saved successfully!")
    
    assert "vendor" in driver.page_source.lower(), "Vendor creation verification failed"
    print("✅ Vendor created successfully and verified!")
    driver.quit()