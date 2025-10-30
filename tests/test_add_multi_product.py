#tests/test_add_multi_product.py
import time
import random
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("setup", "base_url")
def test_add_multiple_products(setup, base_url):
    driver = setup

    # ---------- STEP 1: Login ----------
    driver.get(base_url)
    driver.find_element(By.ID, "email").send_keys("root@grocery.com")
    driver.find_element(By.ID, "password").send_keys("secret@123")

    login_button = driver.find_element(By.CSS_SELECTOR, "button.loginButton")
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(2)  # wait for login to complete
    print("✅ Logged in successfully to admin panel")

    # ---------- STEP 2: Product List ----------
    products = [
        {
            "name": "Olitalia Olio Extra Virgin Di Oliva Oil 5LTR",
            "desc": "This product was added automatically.",
            "unit": "pieces",
            "buy_price": "15000",
            "price": "22000",
            "discount_price": "16728",
            "quantity": "50",
            "min_order": "1",
            "image_id": "7"
        },
        {
            "name": "Test Product 2",
            "desc": "Added using Selenium automation script.",
            "unit": "pcs",
            "buy_price": "200",
            "price": "260",
            "discount_price": "15",
            "quantity": "30",
            "min_order": "2",
            "image_id": "3"
        }
    ]

    # ---------- Helper Function: Open Menu Once ----------
    def open_product_menu_once():
        try:
            submenu_visible = driver.find_elements(By.XPATH, "//div[@id='productMenu']//a[contains(@href, '/shop/product/create')]")
            if submenu_visible:
                print("📂 Product Management menu already expanded")
                return
            product_menu = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Product Management']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", product_menu)
            # time.sleep(1)
            driver.execute_script("arguments[0].click();", product_menu)
            time.sleep(1)
            print("📦 Clicked Product Management menu")
        except Exception as e:
            print("⚠️ Failed to expand product menu:", e)
            
    # ---------- Helper Function: Add Product ----------
    def add_product(product):
        try:
            add_product_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='productMenu']//a[contains(@href, '/shop/product/create')]")
                )
            )
            driver.execute_script("arguments[0].click();", add_product_btn)
            print("🧾 Opened Add Product page")

            # ---------- STEP 3: Fill Form ----------
            driver.find_element(By.ID, "product_name").send_keys(product["name"])
            driver.find_element(By.NAME, "short_description").send_keys(product["desc"])
            print(f"✍️ Filling info for {product['name']}")
            
            # ---------- Description (Rich Text) ----------
            editor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='editor']//div[contains(@class,'ql-editor')]"))
            )
            description_text = f"<p><b>{product['name']}</b> - {product['desc']}</p>"
            driver.execute_script("arguments[0].innerHTML = arguments[1];", editor, description_text)
            print("📝 Description field filled successfully!")
            
            # ---------- Unit ----------
            driver.find_element(By.ID, "unit").send_keys(product["unit"])
            
            # ---------- SKU Generate ----------
            try:
                generate_code = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//label[contains(., 'Generate Code')]//span[contains(@onclick, 'generateCode')]")
                    )
                )
                driver.execute_script("arguments[0].click();", generate_code)
                print("✅ Product SKU generated successfully")
            except:
                print("⚠️ Could not generate SKU")

            # ---------- Prices fields----------
            for field_id, value in [
                ("buy_price", product["buy_price"]),
                ("price", product["price"]),
                ("discount_price", product["discount_price"]),
                ("quantity", product["quantity"]),
                ("min_order_quantity", product["min_order"])
            ]:
                f = driver.find_element(By.ID, field_id)
                f.clear()
                f.send_keys(value)
            print("💰 Filled pricing & quantity details successfully!")
            
            # ---------- Category ----------
            try:
                category_checkbox = driver.find_element(By.ID, "category_2")
                driver.execute_script("arguments[0].click();", category_checkbox)
                print("🍎 Selected category: Fruits")
            except:
                print("⚠️ Category not found, skipping...")

            # ---------- Upload Thumbnail ----------
            thumb_label = driver.find_element(By.CSS_SELECTOR, "label.mainThumbnail")
            driver.execute_script("arguments[0].click();", thumb_label)
            print("🖼️ Opened image upload modal")
            
            driver.switch_to.frame("lfmIframe")

            image_to_select = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.gridCart[data-id='{product['image_id']}']"))
            )
            image_to_select.click()

            confirm_button = driver.find_element(By.XPATH, "//nav[@id='actions']//a[@data-action='use']")
            confirm_button.click()
            driver.switch_to.default_content()

            # ---------- Submit from----------
            submit_btn = driver.find_element(By.XPATH, "//button[contains(.,'Submit') or contains(.,'Save')]")
            driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(1)
            print(f"🚀 Submitted product '{product['name']}'")
            
            # ---------- Validation ----------
            assert "products" in driver.current_url, f"❌ Product '{product['name']}' failed to add"
            print(f"🎉 '{product['name']}' added successfully!\n")

        except Exception as e:
            pytest.fail(f"⚠️ Error adding product {product['name']}: {e}")
            
    # ---------- STEP 3: Open Menu Once & Add All Products ----------
    # Run add products
    open_product_menu_once()
    for p in products:
        add_product(p)
    # ---------- Close Browser ----------
    driver.quit()
    print("✅ All products processed successfully!")
