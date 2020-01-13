import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from Screenshot import Screenshot_Clipping
from ensure_selenium_driver import check_for_driver


def to_data_folder():
    if not os.path.isdir('data'):
        os.mkdir('data')
    os.chdir('data')


def grab_prompt(url):
    pass


def grab_full_page(url):
    ob = Screenshot_Clipping.Screenshot()
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div[*]/div/button').click()
    img_url = ob.full_Screenshot(driver, save_path='.')
    print(img_url)
    driver.close()
    driver.quit()


def grab_images(url):
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div[*]/div/button').click()
    elements = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div[4]/div/div/div/div[*]')
    action = ActionChains(driver)
    ob = Screenshot_Clipping.Screenshot()
    print(len(elements))
    for num_a, a in enumerate(elements):
        print(num_a, a)
        action.move_to_element(a)
        try:
            print(a.find_element_by_xpath('./div/div/div[2]/div[2]/div[1]/div[1]/a/text()'))
        except Exception as err:
            print('error', err)
            if str(err).__contains__('TypeError'):
                print('has name')
                a.screenshot('hold.png')
            pass

        continue
        '/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div[4]/div/div/div/div[6]/div/div/div[2]/div[2]/div[1]/div[1]/a'
        '/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div[4]/div/div/div/div[8]/div/div/div[2]/div[2]/div[1]/div[1]/a'
        img_url = ob.get_element(driver, a, '.')
        print('img url', img_url)
    driver.quit()


def main():
    to_data_folder()
    check_for_driver('firefox')
    test_url = 'https://www.reddit.com/r/AskReddit/comments/emvveb/australian_bushfire_crisis/'
    small_url = 'https://www.reddit.com/r/AskReddit/comments/envpqo/homeless_redditors_what_is_keeping_you_going_rn/'
    fourteen_url = 'https://www.reddit.com/r/AskReddit/comments/eo0naz/a_big_muscular_man_appears_in_front_of_you_and/'
    grab_images(fourteen_url)


if __name__ == '__main__':
    main()