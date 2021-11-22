from os import system
from random import randint
from selenium import webdriver
from time import sleep
import requests
import speech_recognition as sr

def Solve():
    profile = webdriver.FirefoxOptions()
    profile.headless = False
    profile.accept_untrusted_certs = True
    profile.set_preference('intl.accept_languages', 'es-ES')
    profile.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
    driver = webdriver.Firefox(options=profile)

    try:
        driver.get("https://www.google.com/recaptcha/api2/demo")
        sleep(randint(0,5))

        # Click Captcha button
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@title='reCAPTCHA']"))
        driver.find_element_by_class_name("recaptcha-checkbox-border").click()
        driver.execute_script("window.scrollTo(0,{})".format(randint(10,200)))
        sleep(randint(5,10))

        # Check if challange was requested
        if driver.find_element_by_id("recaptcha-anchor").get_attribute("class") != "recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-clearOutline":
            try:
                driver.switch_to.parent_frame()
                sleep(randint(1,2))

                submit = driver.find_element_by_id("recaptcha-demo-submit")
                driver.execute_script("arguments[0].click();", submit)
                sleep(randint(0,5))
            except Exception as e:
                print("Error: {}".format(e))
                pass

        driver.switch_to.parent_frame()

        # Click Audio button
        driver.execute_script("window.scrollTo(0,{})".format(randint(10,200)))
        driver.switch_to.frame(2)
        driver.find_element_by_id("recaptcha-audio-button").click()

        driver.switch_to.parent_frame()

        # Search for mp3 URL   
        driver.execute_script("window.scrollTo(0,{})".format(randint(10,200)))
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@title='El reCAPTCHA caduca dentro de dos minutos']"))
        sleep(randint(1,2))
        element = driver.find_element_by_xpath("//a[contains(@href,'/api2/payload/audio.mp3')]")
        audioMp3 = element.get_attribute("href")

        # Download mp3 and resolve to text
        response = requests.get(audioMp3)
        with open('./audio.mp3','wb') as f:
            f.write(response.content)

        system('bash -c "ffmpeg -y -i audio.mp3 audio.wav >/dev/null 2>&1"')
        sleep(1.0)

        r = sr.Recognizer()
        with sr.AudioFile("audio.wav") as source:
            audio = r.record(source)

        try:
            text = r.recognize_google(audio, language="es-ES")
        except Exception:
            text = r.recognize_google(audio, language="en-US")

        # Submit audio response
        driver.find_element_by_id("audio-response").send_keys(text)
        sleep(randint(1,5))
        driver.find_element_by_id("recaptcha-verify-button").click()
        sleep(randint(1,2))

        driver.switch_to.parent_frame()
        sleep(randint(1,2))

        # Submit form
        submit = driver.find_element_by_id("recaptcha-demo-submit")
        driver.execute_script("arguments[0].click();", submit)
        sleep(randint(1,5))

        print(driver.page_source)
        driver.close()
    except KeyboardInterrupt:
        driver.close()
        exit()
    except Exception as e:
        print("Error: {}".format(e))
        exit()

if __name__ == "__main__":
    while True:
        Solve()
        sleep(10.0)
