
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = Path(__file__).with_name("index.html").as_uri()


def run_test(driver, test_name, username, password, expected):
    print(f"\nRunning: {test_name}")
    print(f"Expected Result: {expected}")

    try:
        driver.get(URL)

        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        actual = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "message"))
        ).text

        print(f"Actual Result: {actual}")

        assert actual == expected, (
            f"Expected '{expected}', but got '{actual}'"
        )

        print(f"Status: PASS - {test_name}")
        return True

    except Exception as error:
        print(f"Status: FAIL - {test_name}")
        print(f"Error: {error}")
        return False


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:
        results = []

        results.append(run_test(
            driver,
            "TC01 - Valid Login",
            "student",
            "Password123",
            "Login Successful"
        ))

        results.append(run_test(
            driver,
            "TC02 - Invalid Login",
            "student",
            "Wrong123",
            "Invalid username or password"
        ))

        print("\n========== TEST SUMMARY ==========")
        print(f"Total Tests: {len(results)}")
        print(f"Passed: {sum(results)}")
        print(f"Failed: {len(results) - sum(results)}")
        print("==================================")

        if not all(results):
            raise SystemExit(1)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
