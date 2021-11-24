from random import randint
from selenium import webdriver
from solve import Solve
from time import sleep

def Test():
    profile = webdriver.FirefoxOptions()
    profile.headless = True
    profile.accept_untrusted_certs = True
    profile.set_preference('intl.accept_languages', 'es-ES')
    profile.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
    driver = webdriver.Firefox(options=profile)

    driver.get("https://www.google.com/recaptcha/api2/demo")
    sleep(randint(0,5))

    if Solve(driver):
        print("Successfully solved reCAPTCHA challange!")

    # Submit form
    print("Submitting form...")
    submit = driver.find_element_by_id("recaptcha-demo-submit")
    driver.execute_script("arguments[0].click();", submit)
    sleep(randint(1,5))
    print("Printing page source:")
    print(driver.page_source)
    print("Closing browser...")
    driver.close()

if __name__ == "__main__":
    count = 0
    while True:
        print("Attempt number {}".format(count))
        Test()
        count += 1
