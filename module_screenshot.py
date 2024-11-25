import os
import time


def take_screenshot(driver):
    timestamp = int(time.time())
    screenshot_filename = os.path.join('images', f'result_{timestamp}.jpg')
    driver.save_screenshot(screenshot_filename)
    print(f"Создан скриншот: {screenshot_filename}")