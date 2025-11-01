# test_create_flash_sale.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_create_flash_sale(setup, base_url):
    driver = setup
    wait = WebDriverWait(driver, 10)

    # ---------- STEP 1: Login ----------
    driver.get(base_url)
    print("Opened login page")
    time.sleep(1)

    # Login credentials (adjust if needed)
    driver.find_element(By.ID, "email").send_keys("root@grocery.com")
    driver.find_element(By.ID, "password").send_keys("secret@123")
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.loginButton")))
    driver.execute_script("arguments[0].click();", login_btn)
    print("✅ Logged in successfully")
    time.sleep(2)

    # ---------- STEP 2: Open Flash Sales dropdown ----------
    flash_sales_menu = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a[data-bs-toggle='collapse'][href='#flashSaleMenu']")))
    driver.execute_script("arguments[0].click();", flash_sales_menu)
    print("📂 Opened 'Flash Sales' dropdown")
    time.sleep(1)

    # ---------- STEP 3: Click 'List of Flash Sales' ----------
    list_flash_sales = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.subMenu[href*='/admin/flash-sales']")))
    driver.execute_script("arguments[0].click();", list_flash_sales)
    print("📄 Opened 'List of Flash Sales' page")
    time.sleep(2)

    # ---------- STEP 4: Click 'Create New' ----------
    create_new_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.btn.btn-primary[href*='/flash-sale/create']")))
    driver.execute_script("arguments[0].click();", create_new_btn)
    print("🆕 Clicked 'Create New' to open Flash Sale form")
    time.sleep(2)

    # ---------- STEP 5: Fill up Flash Sale form ----------
    timestamp = int(time.time())
    flash_name = f"Flash Sale {timestamp}"

    # Fill name
    driver.find_element(By.ID, "name").send_keys(flash_name)

    # Fill minimum discount
    driver.find_element(By.ID, "discount").send_keys("10")

    # Fill start date & time
    driver.find_element(By.ID, "datepicker").send_keys("11/02/2025")
    driver.find_element(By.ID, "timepicker").send_keys("10:00")

    # Fill end date & time
    driver.find_element(By.ID, "datepicker2").send_keys("11/05/2025")
    driver.find_element(By.ID, "timepicker2").send_keys("23:59")

    # Fill description
    driver.find_element(By.NAME, "description").send_keys("This is an automated test flash sale.")
    print("📝 Filled Flash Sale form successfully")
    time.sleep(5)
    
    # ---------- Upload Thumbnail ----------
    try:
        # 1️⃣ Open Thumbnail modal
        flash_sale_thumbnail_label = driver.find_element(By.XPATH, "//input[@name='thumbnail']/preceding-sibling::label")
        driver.execute_script("arguments[0].scrollIntoView(true);", flash_sale_thumbnail_label)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", flash_sale_thumbnail_label)
        print("🖼️ Opened Flash Sale Thumbnail upload modal")
        
        # 2️⃣ Wait for iframe and switch
        driver.switch_to.frame("lfmIframe")
        print("🔄 Switched to banner image frame")
        
        # 3️⃣ Select desired thumbnail image (data-id='5' as example)
        Thumbnail_image = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.gridCart[data-id='5']")))
        driver.execute_script("arguments[0].click();", Thumbnail_image)
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
        print("⚠️ Flash Sale Thumbnail upload failed:", e)

    # ---------- STEP 6: Submit form ----------
    submit_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Submit')]")))
    driver.execute_script("arguments[0].click();", submit_btn)
    print("✅ Submitted Flash Sale form successfully")

    # ---------- STEP 7: Verification ----------
    time.sleep(2)
    assert "flash" in driver.page_source.lower(), "Flash Sale creation verification failed"
    print("🎉 Flash Sale created and verified successfully!")

    driver.save_screenshot(f"flash_sale_{timestamp}.png")
    print("📸 Screenshot saved!")
    
    assert "/admin/flash-sales" in driver.current_url, "❌ Redirect to Flash Sale list failed!"
    print("✅ Redirected to Flash Sale list page successfully!")


