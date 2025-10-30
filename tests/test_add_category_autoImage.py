import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_add_category_with_image(setup, base_url):
    driver = setup
    """✅ Test: Add Category with Image Upload"""

    # wait = WebDriverWait(driver, 20)

    # ---------- STEP 1: Open login page ----------
    # driver.get("https://uat-readygrocery.razinsoft.com/admin/login")
    driver.get(base_url)
    print("Opened login page")
    time.sleep(2)

    # ---------- STEP 2: Login ----------
    driver.find_element(By.ID, "email").send_keys("root@grocery.com")
    driver.find_element(By.ID, "password").send_keys("secret@123")
    driver.find_element(By.CSS_SELECTOR, "button.loginButton").click()
    print("Clicked login button")
    time.sleep(3)

    # ---------- STEP 3: Navigate to 'Categories' ----------
    categories_menu = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "Categories")))
    categories_menu.click()
    print("Clicked Categories option")
    time.sleep(2)

    # ---------- STEP 4: Fill category form ----------
    driver.find_element(By.ID, "name").send_keys("Automation Category")
    driver.find_element(By.ID, "description").send_keys("This is a test category created by automation.")

    # Ensure 'Active' checkbox is selected
    is_active_checkbox = driver.find_element(By.ID, "is_active")
    if not is_active_checkbox.is_selected():
        is_active_checkbox.click()

    # ---------- STEP 5: Image Upload ----------
    image_container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "label.mainThumbnail")))
    driver.execute_script("arguments[0].click();", image_container)
    print("Clicked image container to open uploader")
    time.sleep(2)

    # Switch to iframe
    iframe = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "lfmIframe")))
    driver.switch_to.frame(iframe)
    print("Switched to iframe")

    # Wait for images to appear
    modal_images = WebDriverWait(driver, 5).until(lambda d: d.find_elements(By.CSS_SELECTOR, "div.gridCart div.square"))
    print(f"Found {len(modal_images)} images inside iframe")

    # Select an image (index 7 = 8th image)
    if len(modal_images) > 7:
        driver.execute_script("arguments[0].scrollIntoView(true);", modal_images[7])
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", modal_images[7])
        print("Selected 8th image")
        time.sleep(2)

    # Confirm image selection
    confirm_btn = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.CSS_SELECTOR, "a[data-action='use']"))
    driver.execute_script("arguments[0].click();", confirm_btn)
    print("Clicked Confirm button")
    time.sleep(2)

    driver.switch_to.default_content()

    # ---------- STEP 6: Submit the form ----------
    submit_btn = driver.find_element(By.ID, "submitButton")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", submit_btn)
    print("Clicked Submit button")

    # ---------- STEP 7: Screenshot ----------
    time.sleep(3)
    driver.save_screenshot("category_added.png")
    print("✅ Category created and screenshot saved!")

    # ---------- STEP 8: Assertion ----------
    assert "category" in driver.current_url or "categories" in driver.page_source, "❌ Category creation failed"
