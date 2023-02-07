from selenium.webdriver.common.by import By
from seleniumwire import webdriver  
import time
import gzip
import json
import os
import shutil
from pyvirtualdisplay import Display


def remove_dir(region_id):
  if region_id:
    parent_dir = "/home/www/licreg/data/licenses-registry/json"
    directory = str(region_id)
    path = os.path.join(parent_dir, directory)
    shutil.rmtree(path)


def make_dir(region_id):

  if region_id:
    parent_dir = "/home/www/licreg/data/licenses-registry/json"
    directory = str(region_id)
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)


def russian_regions_read_status():

  with open('/home/www/licreg/data/licenses-registry/status/russian_regions_status.json') as file:
    russian_regions = json.load(file)

  for region in russian_regions:
    if region["scraped_status"]:
      print(
        region["id"],
        region["name"],
        region["scraped_status"],
      )
    elif region["id"] <= 99:
      print(region["id"])
      return region["id"]
    else:
      return 100


def russian_regions_write_status(file_exists=True):

  if not file_exists:

    with open('/home/www/licreg/filters/russian-regions.json') as file:
      dataFrame = json.load(file)

    russian_regions = dataFrame['result']['dataFrame']['rows']

    russian_regions_list = []
    count = 0
    for region in russian_regions:
      print(region[0])
      russian_regions_list.append({
        'id': count,
        'name': region[0],
        'scraped_status': False
      })
      count += 1

    with open('/home/www/licreg/data/licenses-registry/status/russian_regions_status.json', 'w') as file:
      json.dump(russian_regions_list, file, indent=4, ensure_ascii=False)

    return 0

  else:

    with open('/home/www/licreg/data/licenses-registry/status/russian_regions_status.json') as file:
      russian_regions = json.load(file)

    region_id = russian_regions_read_status()
    russian_regions[region_id]["scraped_status"] = True
    print(russian_regions[region_id])

    with open('/home/www/licreg/data/licenses-registry/status/russian_regions_status.json', 'w') as file:
      json.dump(russian_regions, file, indent=4, ensure_ascii=False)
    
    return region_id


def click_regions_filter(driver):

  region_id = russian_regions_read_status()

  find_pager_element = driver.find_element(By.CSS_SELECTOR, \
    "#bf074f6f6c994c49b33efd267915a9b3")
  find_pager_element.click()
  time.sleep(1)
  find_pager_element = driver.find_element(By.CSS_SELECTOR, \
    f"#bf074f6f6c994c49b33efd267915a9b3 .rb-filter-body-container.opened .rb-filter-list li:nth-child({region_id + 2})")
  find_pager_element.click()
  time.sleep(1)
  find_pager_element = driver.find_element(By.CSS_SELECTOR, \
    "#bf074f6f6c994c49b33efd267915a9b3 .rb-filter-body-container .rb-filter-apply-button")
  find_pager_element.click()
  time.sleep(20)


def get_pages(driver):
  pages = find_pager_element = driver.find_element(By.CSS_SELECTOR, \
    ".dx-pages .dx-page-indexes .dx-page:last-child").text
  return pages


def click_page_button(driver):
  find_pager_element = driver.find_element(By.CSS_SELECTOR, "div.dx-page.dx-selection + .dx-page")
  find_pager_element.click()
  time.sleep(20)


def get_first_request_number(driver):
  count = 0
  query_after_filter = 0
  for request in driver.requests:
    if request.response:
      print(
        count,
        request.url,
        request.response.status_code,
        request.response.headers['Content-Type']
      )
      request_number = count
      if count > 101 and "query" in request.url:
        query_after_filter += 1
        print(
          "query_after_filter: ",
          query_after_filter
        )
        if query_after_filter == 5:
          first_request_number = count
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


def	get_source_json(url):
    
  region_id = russian_regions_read_status()
  if region_id >= 99:
      return region_id
  display = Display(visible=0, size=(800, 800))  
  display.start()
  driver = webdriver.Chrome()
  driver.maximize_window()

  try:
    driver.get(url)
    driver.switch_to.frame("myframe")
    time.sleep(5)

    click_regions_filter(driver)
    pages = get_pages(driver)
    make_dir(region_id)

    first_request = get_first_request_number(driver)
    print(first_request)
    request_number = first_request
    response_body_decoded = gzip.decompress(driver.requests[request_number].response.body).decode('utf-8')
    page_number = 1
    print(request_number, page_number)
    with open(f"/home/www/licreg/data/licenses-registry/json/{region_id}/page_{page_number}.json", "w") as file:
      file.write(response_body_decoded)

    while True:
      if str(page_number) == pages:
        break
      click_page_button(driver)
      request_number = get_request_number(driver, prev_request_number=request_number)
      response_body_decoded = gzip.decompress(driver.requests[request_number].response.body).decode('utf-8')
      page_number += 1
      print(request_number, page_number)
      with open(f"/home/www/licreg/data/licenses-registry/json/{region_id}/page_{page_number}.json", "w") as file:
        file.write(response_body_decoded)

    region_id = russian_regions_write_status()

    return region_id 

  except Exception as _ex:
    print(_ex)
    region_id = russian_regions_read_status()
    remove_dir(region_id)

  finally:
    driver.close()
    driver.quit()
    display.stop()


def main():
  
  region_id = 0  
  while True:
    if region_id >= 99:
      break
    region_id = get_source_json(url="https://rfgf.ru/ReestrLic/")
    time.sleep(300)

if __name__ == "__main__":
  main()
