"""Module that handles the like features"""
from math import ceil
from time import sleep
from re import findall
from selenium.webdriver.common.keys import Keys

def get_links_for_tag(browser, tag, amount):
  """Fetches the number of links specified
  by amount and returns a list of links"""
  browser.get('https://www.instagram.com/explore/tags/'
              + (tag[1:] if tag[:1] == '#' else tag))

  sleep(2)

  # clicking load more till there are 1000 posts
  body_elem = browser.find_element_by_tag_name('body')

  sleep(2)

  load_button = body_elem.find_element_by_xpath \
    ('//a[contains(@class, "_8imhp _glz1g")]')
  body_elem.send_keys(Keys.END)
  sleep(2)

  load_button.click()

  body_elem.send_keys(Keys.HOME)
  sleep(1)

  main_elem = browser.find_element_by_tag_name('main')

  new_needed = int(ceil((amount - 33) / 12))

  for _ in range(new_needed):  # add images x * 12
    body_elem.send_keys(Keys.END)
    sleep(1)
    body_elem.send_keys(Keys.HOME)
    sleep(1)

  link_elems = main_elem.find_elements_by_tag_name('a')
  links = [link_elem.get_attribute('href') for link_elem in link_elems]

  return links[:amount]

def check_link(browser, link, dont_like, ignore_if_contains, username):
  """Gets the description of the link and checks for the dont_like tags"""
  browser.get(link)

  sleep(2)

  user_div = browser.find_element_by_class_name('_nk46a')
  user_name = user_div.find_element_by_tag_name('a').text
  image_text = user_div.find_element_by_tag_name('span').text

  print('Image from: ' + user_name)
  print('Link: ' + link)
  print('Description: ' + image_text)

  for word in ignore_if_contains:
    if word in image_text:
      return False, user_name

  for tag in dont_like:
    if tag in image_text or user_name == username:
      return True, user_name

  return False, user_name

def like_image(browser):
  """Likes the browser opened image"""
  a_elems = browser.find_elements_by_xpath('//a[@role = "button"]')

  #handle videos
  link_elem = a_elems[0] if len(a_elems) < 2 else a_elems[len(a_elems) - 1]

  span_elem_text = link_elem.text

  if span_elem_text == 'Like':
    link_elem.click()
    print('--> Image liked!')
    sleep(2)
    return True
  else:
    print('--> Already Liked!')
    return False


def get_tags(browser, url):
  """Gets all the tags of the given description in the url"""
  browser.get(url)
  sleep(1)

  user_div = browser.find_element_by_class_name('_nk46a')
  image_text = user_div.find_element_by_tag_name('span').text

  tags = findall(r'#\w*', image_text)
  return tags
