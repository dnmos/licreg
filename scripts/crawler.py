import json
import os
import shutil
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
      "status": False
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
      "status": False
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
    if type["status"]:
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
    if region["status"]:
      pass
    elif region["id"] <= 99:
      return region["id"]

  create_russian_regions_status()
  return 0


def type_of_minerals_write_status() -> int:

  with open(config.STATUS_PATH + "type_of_minerals_status.json") as file:
    type_of_minerals = json.load(file)

  type_of_minerals_id = type_of_minerals_read_status()
  type_of_minerals[type_of_minerals_id]["status"] = True
  print(type_of_minerals[type_of_minerals_id])

  with open(config.STATUS_PATH + "type_of_minerals_status.json", "w") as file:
    json.dump(type_of_minerals, file, indent=4, ensure_ascii=False)
  
  return type_of_minerals_id + 1


def russian_regions_write_status() -> int:

  with open(config.STATUS_PATH + "russian_regions_status.json") as file:
    russian_regions = json.load(file)

  region_id = russian_regions_read_status()
  if region_id <= 99:
    russian_regions[region_id]["status"] = True
    print(russian_regions[region_id])
    with open(config.STATUS_PATH + "russian_regions_status.json", "w") as file:
      json.dump(russian_regions, file, indent=4, ensure_ascii=False)
    return region_id + 1
