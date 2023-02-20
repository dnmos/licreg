from selenium.webdriver.common.by import By
from seleniumwire import webdriver  
import time
import gzip
import json
import os
import shutil
from pyvirtualdisplay import Display
import config


def remove_dir(region_id):
  if region_id:
    parent_dir = config.JSON_RESULT_PATH
    directory = str(region_id)
    path = os.path.join(parent_dir, directory)
    shutil.rmtree(path)


def make_dir(type_of_minerals_id: int, region_id: int):

  parent_dir = config.JSON_RESULT_PATH

  directory = str(type_of_minerals_id)
  path = os.path.join(parent_dir, directory)
  if not os.path.isdir(path):
    os.mkdir(path)
    print("Directory", path, "is created")

  directory = str(type_of_minerals_id) + "/" + str(region_id)
  path = os.path.join(parent_dir, directory)
  if not os.path.isdir(path):
    os.mkdir(path)
    print("Directory", path, "is created")


def create_type_of_minerals_status() -> int:

  with open(config.FILTERS_PATH + "type-of-minerals.json") as file:
    dataFrame = json.load(file)

  type_of_minerals = dataFrame["result"]["dataFrame"]["rows"]

  type_of_minerals_list = []
  count = 0
  for type in type_of_minerals:
    type_of_minerals_list.append({
      "id": count,
      "name": type[0],
      "scraped_status": False
    })
    count += 1

  with open(config.STATUS_PATH + "type_of_minerals_status.json", "w") as file:
    json.dump(type_of_minerals_list, file, indent=4, ensure_ascii=False)

  return 0


def create_russian_regions_status() -> int:

  with open(config.FILTERS_PATH + "russian-regions.json") as file:
    dataFrame = json.load(file)

  russian_regions = dataFrame["result"]["dataFrame"]["rows"]

  russian_regions_list = []
  count = 0
  for region in russian_regions:
    russian_regions_list.append({
      "id": count,
      "name": region[0],
      "scraped_status": False
    })
    count += 1

  with open(config.STATUS_PATH + "russian_regions_status.json", "w") as file:
    json.dump(russian_regions_list, file, indent=4, ensure_ascii=False)

  return 0


def type_of_minerals_read_status() -> int:

  try:
    with open(config.STATUS_PATH + "type_of_minerals_status.json") as file:
      type_of_minerals = json.load(file)
  except OSError as e:
    if e.args[0] in (2,):
      return create_type_of_minerals_status()

  for type in type_of_minerals:
    if type["scraped_status"]:
      pass
    elif type["id"] <= 8:
      return type["id"]

  return 9


def russian_regions_read_status() -> int:

  try:
    with open(config.STATUS_PATH + "russian_regions_status.json") as file:
      russian_regions = json.load(file)
  except OSError as e:
    if e.args[0] in (2,):
      return create_russian_regions_status()

  for region in russian_regions:
    if region["scraped_status"]:
      pass
    elif region["id"] <= 99:
      return region["id"]

  create_russian_regions_status()
  return 0


def type_of_minerals_write_status() -> int:

  with open(config.STATUS_PATH + "type_of_minerals_status.json") as file:
    type_of_minerals = json.load(file)

  type_of_minerals_id = type_of_minerals_read_status()
  type_of_minerals[type_of_minerals_id]["scraped_status"] = True
  print(type_of_minerals[type_of_minerals_id])

  with open(config.STATUS_PATH + "type_of_minerals_status.json", "w") as file:
    json.dump(type_of_minerals, file, indent=4, ensure_ascii=False)
  
  return type_of_minerals_id + 1


def russian_regions_write_status() -> int:

  with open(config.STATUS_PATH + "russian_regions_status.json") as file:
    russian_regions = json.load(file)

  region_id = russian_regions_read_status()
  if region_id <= 99:
    russian_regions[region_id]["scraped_status"] = True
    print(russian_regions[region_id])
    with open(config.STATUS_PATH + "russian_regions_status.json", "w") as file:
      json.dump(russian_regions, file, indent=4, ensure_ascii=False)
    return region_id + 1


def click_type_of_minerals_filter(driver):

  type_of_minerals_id = type_of_minerals_read_status()

  find_pager_element = driver.find_element(By.CSS_SELECTOR, config.TYPE_OF_MINERALS_WIDGET)
  find_pager_element.click()
  time.sleep(1)
  find_pager_element = driver.find_element(By.CSS_SELECTOR, f"{config.TYPE_OF_MINERALS_WIDGET_ROW}({type_of_minerals_id + 1})")
  find_pager_element.click()
  time.sleep(1)
  find_pager_element = driver.find_element(By.CSS_SELECTOR, config.TYPE_OF_MINERALS_WIDGET_BUTTON)
  find_pager_element.click()
  time.sleep(3)


def click_regions_filter(driver):

  region_id = russian_regions_read_status()

  find_pager_element = driver.find_element(By.CSS_SELECTOR, config.REGIONS_WIDGET)
  find_pager_element.click()
  time.sleep(1)
  try:
    find_pager_element = driver.find_element(By.CSS_SELECTOR, config.REGIONS_WIDGET_UNSELECT)
    find_pager_element.click()
    time.sleep(1)
  except Exception as e:
    print(e)
  find_pager_element = driver.find_element(By.CSS_SELECTOR, f"{config.REGIONS_WIDGET_ROW}({region_id + 2})")
  find_pager_element.click()
  time.sleep(1)
  find_pager_element = driver.find_element(By.CSS_SELECTOR, config.REGIONS_WIDGET_BUTTON)
  find_pager_element.click()
  time.sleep(20)


def get_licenses_selected(driver):
  try:
    licenses_selected = driver.find_element(By.CSS_SELECTOR, config.LICENSES_SELECTED).text
    print("Выбрано:", licenses_selected)
    return licenses_selected
  except Exception as e:
    print(e)
    return False


def get_pages(driver):
  try:
    pages = driver.find_element(By.CSS_SELECTOR, config.LAST_PAGE).text
    return pages
  except Exception as e:
    print(e)
    return False


def click_page_button(driver) -> bool:
  try:
    find_pager_element = driver.find_element(By.CSS_SELECTOR, config.NEXT_PAGE)
    find_pager_element.click()
    time.sleep(20)
    return True
  except Exception as e:
    print(e)
    return False


def get_first_request_number(driver):
  count = 0
  query_utf_8 = 110
  for request in driver.requests:
    if request.response and "query" in request.url and "image" not in request.url:
      print(
        count,
        request.url,
        request.response.status_code,
        request.response.headers["Content-Type"]
      )
      request_number = count
      if count > query_utf_8 and "query" in request.url and "utf-8" in request.response.headers["Content-Type"]:
        query_utf_8 = count
      if count > query_utf_8 and "query" in request.url:
        first_request_number = count
        print("first_request_number:", first_request_number)

    count += 1
  request_number = first_request_number
  return request_number


def get_request_number(driver, prev_request_number):
  count = 0
  for request in driver.requests:
    if request.response and count > prev_request_number and "query" in request.url:
      request_number = count
    count += 1
  return request_number


def result_write_json(
  request_number: int, 
  driver: object, 
  page_number: int, 
  type_of_minerals_id: int, 
  region_id: int):

  try:
    response_body_decoded = gzip.decompress(driver.requests[request_number].response.body).decode("utf-8")
    print(request_number, page_number)
    json_file_name = f"{type_of_minerals_id}_{region_id}_{page_number}.json"
    with open(f"{config.JSON_RESULT_PATH}{type_of_minerals_id}/{region_id}/{json_file_name}", "w") as file:
      file.write(response_body_decoded)
    return True
  except Exception as e:
    print(e)
    return False


def	get_source_json(url, type_of_minerals_id, region_id):
    
  display = Display(visible=0, size=(800, 800))  
  display.start()

  driver = webdriver.Chrome()
  driver.maximize_window()

  try:
    driver.get(url)
    time.sleep(5)
    driver.switch_to.frame("myframe")
    time.sleep(5)

    click_type_of_minerals_filter(driver)
    click_regions_filter(driver)
    if not get_licenses_selected(driver):
      return False

    page_number = 1
    pages = get_pages(driver)
    print("type_of_minerals_id:", type_of_minerals_id, "region_id:", region_id, "make directory...")
    make_dir(type_of_minerals_id, region_id)

    first_request = get_first_request_number(driver)
    print(first_request)
    request_number = first_request
    result_write_json(request_number, driver, page_number, type_of_minerals_id, region_id)

    if pages:
      while True:
        if str(page_number) == pages:
          break
        next_button_exists = click_page_button(driver)
        if next_button_exists:
          page_number += 1
          request_number = get_request_number(driver, prev_request_number=request_number)
          result_write_json(request_number, driver, page_number, type_of_minerals_id, region_id)

    elif not pages:
      pages = range(11)
      for page in pages:
        next_button_exists = click_page_button(driver)
        if next_button_exists:
          page_number += 1
          request_number = get_request_number(driver, prev_request_number=request_number)
          result_write_json(request_number, driver, page_number, type_of_minerals_id, region_id)

  except Exception as _ex:
    print(_ex)
    region_id = russian_regions_read_status()
    remove_dir(region_id)

  finally:
    driver.close()
    driver.quit()
    display.stop()


def main():

  while True:
    type_of_minerals_id = type_of_minerals_read_status()
    if type_of_minerals_id > 8:
      break

    region_id = russian_regions_read_status()
    while True:
      if region_id > 99:
        break

      try:
        get_source_json("https://rfgf.ru/ReestrLic/", type_of_minerals_id, region_id)
      except Exception as e:
        print(e)
        exit()

      region_id = russian_regions_write_status()
      time.sleep(10)

    type_of_minerals_id = type_of_minerals_write_status()


if __name__ == "__main__":
  main()