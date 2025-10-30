# ---------- ✅ common setup/teardown থাকবে ----------
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

'''
# ---------- BASE URL ----------
base_url = "https://uat-readygrocery.razinsoft.com/admin/login"
@pytest.fixture(scope="session")
def base_url():
    """Return base URL for all tests"""
    return base_url
'''
                    #or

# ✅ Base URL Fixture
@pytest.fixture(scope="session")
def base_url():
    return "https://uat-readygrocery.razinsoft.com/admin/login"

# ✅ Browser Setup Fixture
@pytest.fixture
def setup():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()
