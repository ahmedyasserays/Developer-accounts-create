from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# get the new phone number
countryCode = input('please input the key of the country: ')
phone = input('Please enter the number that you want to activate the developing account for: ')


# saving auth key for the number
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
opt.add_argument(r'user-data-dir=C:\Users\HP\AppData\Local\Google\Chrome\User Data\\' + phone)
opt.add_argument(f"profile-directory=Profile {phone}")
driver = webdriver.Chrome(options=opt)
driver.get('https://web.telegram.org/#/login')
sleep(2)
try:
    countryBox = driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div/div[2]/div[2]/form/div[2]/div[1]/input')
    sleep(1.5)
    countryBox.clear()

    countryBox.send_keys(countryCode)

    numberBox = driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/input')
    numberBox.clear()
    inputPhone = phone[len(countryCode)-1:]
    print(inputPhone)
    numberBox.send_keys(input())
    numberBox.send_keys(Keys.RETURN)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[5]/div[2]/div/div/div[2]/button[2]').click()

    codeBox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ng-app"]/body/div[1]/div/div[2]/div[2]/form/div[4]/input')))
    codeBox.send_keys(input('please enter the code you received: '))
    codeBox.send_keys(Keys.RETURN)
    sleep(2)
except NoSuchElementException:
    print('user has logged in before')

# proceed to the core telegram in new tab
driver.execute_script("window.open('');")
sleep(1.5)
driver.switch_to.window(driver.window_handles[1])
driver.get('https://my.telegram.org/auth')
phoneBox = driver.find_element_by_xpath('//*[@id="my_login_phone"]')
phoneBox.send_keys(phone)
phoneBox.send_keys(Keys.RETURN)
sleep(2)

# get the log in code from the first tab
driver.switch_to.window(driver.window_handles[0])
chatsDiv = driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul')
telegramChat = chatsDiv.find_element_by_partial_link_text("Telegram")
telegramChat.click()
sleep(1)

messages = driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div[2]/div'
                                        '/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]')

codeMessage: str = messages.find_element_by_css_selector('.im_history_message_wrap:last-of-type').text
code = codeMessage[codeMessage.index(':', codeMessage.index('.'))+1:codeMessage.index(':', codeMessage.index('.'))+13]
driver.switch_to.window(driver.window_handles[1])
codeBox = driver.find_element_by_xpath('//*[@id="my_password"]')
codeBox.send_keys(code)
codeBox.send_keys(Keys.RETURN)
sleep(3)

# fill the required info
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'API development tools'))).click()

sleep(3)
try:
    titleBox = driver.find_element_by_xpath('//*[@id="app_title"]')
    shortNameBox = driver.find_element_by_xpath('//*[@id="app_shortname"]')
    platform = driver.find_element_by_xpath('//*[@id="app_create_form"]/div[4]/div/div[5]/label/input')

    titleBox.send_keys('botcreator')
    shortNameBox.send_keys('botcreator')
    platform.click()
    driver.find_element_by_xpath('//*[@id="app_save_btn"]').click()
    sleep(2)
except NoSuchElementException:
    print('user is already a developer')
# save the info of the account in a file
api_id = driver.find_element_by_xpath('//*[@id="app_edit_form"]/div[1]/div[1]/span').text
api_hash = driver.find_element_by_xpath('//*[@id="app_edit_form"]/div[2]/div[1]/span').text
with open('adders.txt', 'a') as f:
    f.write(f"{phone},{api_id},{api_hash}\n")


# change the name of the account
driver.switch_to.window(driver.window_handles[0])
driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div[1]/div/div/div[1]/div/a').click()
sleep(0.5)
driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div[1]/div/div/div[1]/div/ul/li[3]/a').click()
sleep(0.5)
driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[6]/div[2]/div/div/div[1]/div[1]/div[1]/a[2]').click()
sleep(0.5)
driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[7]/div[2]/div/div/div[1]/form/div[1]/input').clear()
sleep(0.5)
driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[7]/div[2]/div/div/div[1]/form/div[1]/input').send_keys('ahmed')
sleep(0.5)
driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[7]/div[2]/div/div/div[1]/form/div[2]/input').clear()
sleep(0.5)
driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[7]/div[2]/div/div/div[1]/form/div[2]/input').send_keys('yasser')
sleep(0.5)
driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[7]/div[2]/div/div/div[2]/button[2]').click()
sleep(0.5)
driver.quit()
