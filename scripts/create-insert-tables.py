from sql import db
import config, crawler


def insert_filter_table():

  for filter in config.FILTERS:
    db.insert_filter_table(filter)
    # db.fetchall_filter_table(filter)
  # db.drop()

  return True


def main():
  db.drop()
  db.create()
  insert_filter_table()

  while True:
    type_of_minerals_id = crawler.type_of_minerals_read_status()
    if type_of_minerals_id > 8:
      break

    region_id = crawler.russian_regions_read_status()
    while True:
      if region_id > 99:
        break

      try:
        db.insert_licenses_table(type_of_minerals_id, region_id)
      except Exception as e:
        print(e)
        exit()

      region_id = crawler.russian_regions_write_status()

    type_of_minerals_id = crawler.type_of_minerals_write_status()

  return True


if __name__ == "__main__":
  main()