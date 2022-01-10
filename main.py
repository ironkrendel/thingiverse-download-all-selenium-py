import time
import os
try:
    from re import split
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    import validators
    from validators.domain import domain
    import configparser
except:
    print("Libraries missing, run dependencies.bat")
    time.sleep(2)
    a = input("Press enter to end")
    quit()

config = configparser.ConfigParser()
config.read("cfg.ini")

try:
    donwload_folder = config["Main"]["download_folder"]
    donwload_speed = float(config["Main"]["ethernet_speed"])
except:
    print("Something wrong with cfg.ini file, try running dependencies.bat")
    a = input()
    quit()

while True:
    URL = str(input("Enter target URL: "))
    URL.replace(" ", "")
    domain = URL.split("/")
    if domain[2].startswith("www"):
        domain = domain[2].split("www")[1][1::]
    else:
        domain = domain[2]
        
    URL_copy = URL.split("/")[0:4]
    URL = "/".join(URL_copy)

    if validators.url(URL) and domain == "thingiverse.com":
        break
    else:
        print("Enter valid URL")

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : donwload_folder, "directory_upgrade": True}
chromeOptions.add_experimental_option("prefs", prefs)
chromedriver = "./chromedriver.exe"
try:
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
except:
    print("Webdriver file is missing, donwload it from chromedriver.chromium.org")
    time.sleep(2)
    a = input("Press enter to end")
    quit()
driver.get(URL + "/files")
while True:
    try:
        btns = driver.find_elements_by_class_name("ThingFile__download--2SUQd")
        if btns == []:
            pass
        else:
            break
    except:
        pass
while True:
    try:
        weights_elems = driver.find_elements_by_class_name("ThingFile__fileDescription--2ct10")
        if weights_elems == []:
            pass
        else:
            break
    except:
        pass
weigths = []
for i in weights_elems:
    weigths.append(i.text.split(" ")[0] + " " + i.text.split(" ")[1])
n = 0
for i in btns:
    while True:
        try:
            i.click()
            break
        except:
            pass
    print(f"queued files: {n + 1}")
    if (weigths[n].split(" ")[1] == "mb"):
        time.sleep(int(weigths[n].split(" ")[0]) / donwload_speed)
    elif (weigths[n].split(" ")[1] == "kb"):
        time.sleep(0.1)
    n+=1
print("\n"*10)
while True:
    a = input("Confirm ending by typing y (it will stop downloadings): ")
    if (a.lower() == "y"):
        driver.quit()
        break
    else:
        print("Error on confirmation")
        time.sleep(2)