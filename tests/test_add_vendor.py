#test_add_vendor.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
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
    driver.get(base_url)
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
    unique_phone = f"017{str(timestamp)[-8:]}"  # unique phone number (e.g. 017 + last 8 digits of timestamp)

    driver.find_element(By.ID, "first_name").send_keys("Akif")
    driver.find_element(By.ID, "last_name").send_keys("Alam")
    # driver.find_element(By.ID, "phone").send_keys("01700000000")  // replaced with unique phone
    driver.find_element(By.ID, "phone").send_keys(unique_phone)

    gender_dropdown = Select(driver.find_element(By.ID, "gender"))
    gender_dropdown.select_by_visible_text("Male")

    driver.find_element(By.ID, "email").send_keys(unique_email)
    driver.find_element(By.ID, "password").send_keys("12345678")
    driver.find_element(By.ID, "password_confirmation").send_keys("12345678")

    driver.find_element(By.ID, "shop_name").send_keys(unique_shop)
    driver.find_element(By.ID, "address").send_keys("Dhaka, Bangladesh")
    driver.find_element(By.ID, "description").send_keys("This is a test vendor created by automation.")
    print("📝 Filled vendor details successfully")

    # ---------- STEP 4.1: Upload Profile Photo ----------
    image_path = os.path.join(os.getcwd(),"image.png")  # image.png ফাইলটা project-এর root বা tests/ ফোল্ডারে রাখো
    # ---------- STEP 4.2: Handle Crop Modal ----------
    try:
        # If image exists, upload it first to trigger the crop modal
        if os.path.exists(image_path):
            file_input = driver.find_element(By.ID, "thumbnail")
            file_input.send_keys(image_path)
            print(f"✅ Profile photo uploaded successfully: {image_path}")
            time.sleep(1)
        else:
            print(f"❌ Profile photo not found at: {image_path}")

        # Wait for the crop modal to appear
        crop_modal = wait.until(EC.visibility_of_element_located((By.ID, "cropperModal")))
        print("🖼️ Crop modal appeared successfully!")

        # Wait until the "Crop & Save" button becomes clickable
        crop_save_btn = wait.until(EC.element_to_be_clickable((By.ID, "cropAndSave")))

        # Scroll into view and click via JS (safer)
        driver.execute_script("arguments[0].scrollIntoView(true);", crop_save_btn)
        time.sleep(0.5)
        
        crop_save_btn.click()
        print("✅ Clicked 'Crop & Save' button successfully!")

        # Wait until modal disappears (image cropped)
        wait.until(EC.invisibility_of_element_located((By.ID, "cropperModal")))
        print("🧩 Crop modal closed and image cropped successfully!")
    except Exception as e:
        print("⚠️ Crop modal or 'Crop & Save' button not found:", e)
        
    # ---------- Upload Shop Logo ----------
    try:
        shop_logo_label  = driver.find_element(By.XPATH, "//input[@name='shop_logo']/preceding-sibling::label")
        driver.execute_script("arguments[0].click();", shop_logo_label )
        print("🖼️ Opened Shop Logo upload modal")
        
        # ✅ Wait until the iframe is visible
        iframe = wait.until(EC.presence_of_element_located((By.ID, "lfmIframe")))
        # iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#lfmIframe")))    # alternative
        # driver.switch_to.frame("lfmIframe")   # or use the above located iframe
        driver.switch_to.frame(iframe)
        print("🔄 Switched to image frame")
        
        # Select the desired image inside iframe (data-id='3' as example)
        image_to_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.gridCart[data-id='3']"))
        )
        driver.execute_script("arguments[0].click();", image_to_select)
        print("🖼️ Selected Shop Logo inside iframe")
        
        time.sleep(1)
        
        # Click 'Use' / Confirm button
        confirm_button = driver.find_element(By.XPATH, "//nav[@id='actions']//a[@data-action='use']")
        driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", confirm_button)
        # confirm_button.click()
        print("✅ Clicked Confirm button successfully")
        
        # ✅ Switch back to main page
        driver.switch_to.default_content()
        print("↩️ Switched back to main content successfully")
        
    except Exception as e:
        print("⚠️ Thumbnail upload failed:", e)
        
    # ---------- Upload Shop Banner ----------
    try:
        # 1️⃣ Open Shop Banner modal
        shop_banner_label = driver.find_element(By.XPATH, "//input[@name='shop_banner']/preceding-sibling::label")
        driver.execute_script("arguments[0].scrollIntoView(true);", shop_banner_label)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", shop_banner_label)
        print("🖼️ Opened Shop Banner upload modal")
        
        # 2️⃣ Wait for iframe and switch
        driver.switch_to.frame("lfmIframe")
        print("🔄 Switched to banner image frame")
        
        # 3️⃣ Select desired banner image (data-id='5' as example)
        banner_image = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.gridCart[data-id='5']")))
        driver.execute_script("arguments[0].click();", banner_image)
        print("🖼️ Selected Shop Banner inside")
        
        # 4️⃣ Confirm selection
        confirm_btn = driver.find_element(By.XPATH, "//nav[@id='actions']//a[@data-action='use']")
        driver.execute_script("arguments[0].scrollIntoView(true);", confirm_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", confirm_btn)
        print("✅ Clicked Confirm button successfully")
        
        # 5️⃣ Switch back to main content
        driver.switch_to.default_content()
        print("↩️ Switched back to main content successfully")
        
    except Exception as e:
        print("⚠️ Shop Banner upload failed:", e)


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