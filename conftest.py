import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Firefox()
    driver.maximize_window()
    request.cls.driver = driver
    original_window = driver.current_window_handle
    
    yield
    
    # Закрываем все вкладки, кроме оригинальной, перед завершением
    if len(driver.window_handles) > 1:
        for window in driver.window_handles:
            if window != original_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(original_window)
    driver.quit()