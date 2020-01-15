import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from Screenshot import Screenshot_Clipping
from ensure_selenium_driver import check_for_driver
import time
from lxml import html
from PIL import Image
from PIL import ImageEnhance
import io
from gtts import gTTS


def to_data_folder():
    if not os.path.isdir('data'):
        os.mkdir('data')
    os.chdir('data')


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


def get_element_info(element):
    comment_depth = len(element.find_elements_by_xpath('./div/div/div[1]/div')) - 1
    scan_points = element.find_element_by_xpath('./div/div/div[2]/div[2]/div[1]/span[1]').text.split(' ')[0]
    try:
        if len(scan_points) == 0:
            prep_text = element.find_element_by_xpath('./div/div/div[2]/div[2]/div[2]/div').get_attribute('innerHTML')
            text = html.fromstring(prep_text).text_content()
            print(text)
        if scan_points.__contains__('k'):
            points = str(float(scan_points[:-1]) * 1000)
        elif scan_points.__contains__('ore'):
            points = 'hidden'
        else:
            points = scan_points
    except Exception as err:
        print('error', err)
    prep_text = element.find_element_by_xpath('./div/div/div[2]/div[2]/div[2]/div').get_attribute('innerHTML')
    text = html.fromstring(prep_text).text_content()
    return comment_depth, points, text


def stitch_comments(img_list):
    print('th', img_list)
    img_objs = []
    for a in img_list:
        try:
            img_objs.append(Image.open(io.BytesIO(a)))
        except:
            return False
    new_height, new_width = 0, 0
    for a in img_objs:
        obj_width, obj_height = a.size
        if obj_width > new_width:
            new_width = obj_width
        new_height += obj_height
    result = Image.new('RGB', (new_width, new_height))
    height_offset = 0
    for a in img_objs:
        result.paste(im=ImageEnhance.Sharpness(a).enhance(2), box=(0, height_offset))
        height_offset += a.size[1]
    return result


def use_tts(text, name):
    custom_text = ''
    for a in text.split(' '):
        if a.__contains__('http'):
            a = a[:a.index('http')]
        if a.__contains__('but') or a.__contains__('or') or a.__contains__('and'):
            a = ', ' + a
        custom_text += a
    text = custom_text
    try:
        obj = gTTS(text=text)
        obj.tokenizer_func(text)
        obj.save(name + '.mp3')
        print(name, len(text.split(' ')))
    except:
        return


def grab_images(url):
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    if not os.path.isdir(url_dir := url.split('/')[-2]):
        os.mkdir(url_dir)
    os.chdir(url_dir)
    head = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div[1]')
    cleaned_head = stitch_comments([head.screenshot_as_png])
    head_text = head.find_element_by_xpath('./div/div[3]/div[1]/div/h1').text
    cleaned_head.save('Head.png')
    use_tts(head_text, 'head')
    sleep_time = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[1]/a/span').text.split(' ')[0]
    if sleep_time.__contains__('k'):
        sleep_time = round(float(sleep_time[:-1])) * 1000
    else:
        sleep_time = int(sleep_time)
    sleep_time /= 80
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div[*]/div/button').click()
    time.sleep(sleep_time)
    elements = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div/div/div/div')
    action = ActionChains(driver)
    print(len(elements))
    stitch_queue = []
    last_depth = -1
    first_name = ''
    text_string = ''
    for num_a, a in enumerate(elements):
        print(num_a, a)
        action.move_to_element(a)
        if len(a.find_elements_by_xpath('./div/div/div[2]/div[2]/div[1]/div[1]/a')) == 1:
            depth, points, text = get_element_info(a)
            print(':', depth, text)
            points = '0' * (6 - len(points.replace('.', ''))) + points.replace('.', '')
            file_name = points + '_' + str(num_a)
            if depth == 0:
                if last_depth != -1:
                    finished = stitch_comments(stitch_queue)
                    if type(finished) is bool:
                        continue
                    finished.save(first_name + '.png')
                    print('text', text_string)
                    use_tts(text_string, first_name)
                first_name = file_name
                text_string = ''
                stitch_queue.clear()
            else:
                print(len(stitch_queue))
            try:
                print('s', a.size)
                stitch_queue.append(a.screenshot_as_png)
                text_string += text + '. '
            except Exception as err:
                print('err', err)
                input('error>')
            last_depth = depth
    driver.quit()


def main():
    to_data_folder()
    check_for_driver('firefox')
    test_url = 'https://www.reddit.com/r/AskReddit/comments/emvveb/australian_bushfire_crisis/'
    small_url = 'https://www.reddit.com/r/AskReddit/comments/envpqo/homeless_redditors_what_is_keeping_you_going_rn/'
    fourteen_url = 'https://www.reddit.com/r/AskReddit/comments/eo0naz/a_big_muscular_man_appears_in_front_of_you_and/'
    stress_url = 'https://www.reddit.com/r/AskReddit/comments/enwojq/serious_reddit_what_are_some_free_or_cheap/'
    url_to_use = 'https://www.reddit.com/r/AskReddit/comments/eoss5j/who_here_has_actually_married_their_lets_get/'
    grab_images(url_to_use)


if __name__ == '__main__':
    main()