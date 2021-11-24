from os import system, remove
from random import randint
from selenium import webdriver
from time import sleep
import requests
import speech_recognition as sr

def Solve(driver):
    try:
        # Click Captcha button
        print("Clicking captcha button...")
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@title='reCAPTCHA']"))
        driver.find_element_by_class_name("recaptcha-checkbox-border").click()
        driver.execute_script("window.scrollTo(0,{})".format(randint(10,200)))
        sleep(randint(5,10))

        # Check if challange was requested
        print("Checking is challenge was requested...")
        if driver.find_element_by_id("recaptcha-anchor").get_attribute("class") != "recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-clearOutline":
            try:
                print("Challange not requested, reCAPTCHA solved!")
                driver.switch_to.parent_frame()

                return True
            except Exception as e:
                print("Error: {}".format(e))
                pass

        driver.switch_to.parent_frame()

        # Click Audio button
        print("Clicking audio button...")
        driver.execute_script("window.scrollTo(0,{})".format(randint(10,200)))
        driver.switch_to.frame(2)
        driver.find_element_by_id("recaptcha-audio-button").click()

        driver.switch_to.parent_frame()

        solved = SolveAudioChallange(driver)

        # Check for errors
        while driver.find_element_by_class_name("rc-audiochallenge-error-message").text == "Debes resolver más captchas." or solved == False:
            print("Error: Need to solve more captchas, retrying...")
            sleep(randint(2,5))

            driver.find_element_by_id("recaptcha-reload-button").click()
            driver.switch_to.parent_frame()
            solved = SolveAudioChallange(driver)

        driver.switch_to.parent_frame()

        remove("audio.mp3")
        remove("audio.wav")

        return True
    except KeyboardInterrupt:
        driver.close()
        return False
    except Exception as e:
        print("Error: {}".format(e))
        return False

def SolveAudioChallange(driver):
    try:
        # Search for mp3 URL
        print("Searching for mp3 URL...")
        driver.execute_script("window.scrollTo(0,{})".format(randint(10,200)))
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@title='El reCAPTCHA caduca dentro de dos minutos']"))
        sleep(randint(1,2))
        element = driver.find_element_by_xpath("//a[contains(@href,'/api2/payload/audio.mp3')]")
        audioMp3 = element.get_attribute("href")

        # Download mp3 and resolve to text
        print("Resolving mp3 audio to text...")
        response = requests.get(audioMp3)
        with open('./audio.mp3','wb') as f:
            f.write(response.content)
            
        sleep(1.0)

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
        print("Submitting audio challange response...")
        driver.find_element_by_id("audio-response").send_keys(text)
        sleep(randint(1,5))
        driver.find_element_by_id("recaptcha-verify-button").click()
        sleep(randint(1,2))

        return True
    except FileNotFoundError:
        print("Invalid audio challange")
        return False
    except Exception:
        print("Unknown error while resolving to text")
        return False
