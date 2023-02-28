import pymysql.cursors
import json
import config
import os


def parse_sql(filename):
  data = open(filename, "r").readlines()
  queries = []
  DELIMITER = ";"
  query = ""

  for line in data:

    if not line.strip():
      continue

    if line.startswith("--"):
      continue

    if (DELIMITER not in line):
      query += line.replace(DELIMITER, ";")
      continue

    if query:
      query += line
      queries.append(query.strip())
      query = ""
    else:
      queries.append(line.strip())
  return queries


def connect(): 
  connection = pymysql.connect(host = config.DB_HOST,
                               user = config.DB_USER,
                               database = config.DB_NAME,
                               password = config.DB_PASSWORD,
                               cursorclass = pymysql.cursors.DictCursor)
  return connection


def get_list_from_filter(filter: str):

  with open(config.FILTERS_PATH + filter + ".json") as file:
    data_frame = json.load(file)

  rows = data_frame['result']['dataFrame']['rows']
  list = []
  for row in rows:
    list.append((
      row[0],
    ))

  return list


def get_list_from_json(json_file_path, type_of_minerals_id, region_id):

  with open(json_file_path) as file:
    data = json.load(file)

  rows = data['result']['data']['rows']
  cols = data['result']['data']['cols']
  values = data['result']['data']['values']
  list = []
  for row_number, row in enumerate(rows):
    list_of_values_in_row = []
    for col_number, col in enumerate(cols):
      # Наличие полного электронного образа
      if col_number == 2:
        if values[col_number][row_number] and "Есть" in values[col_number][row_number]:
          list_of_values_in_row.append(True)
        else: 
          list_of_values_in_row.append(False)
      # Вид полезного ископаемого
      elif col_number == 5:
        if values[col_number][row_number]:
          list_of_values_in_row.append(type_of_minerals_id + 1)
      # Регион
      elif col_number == 7:
        if values[col_number][row_number]:
          list_of_values_in_row.append(region_id + 1)
        else:
          list_of_values_in_row.append("")
      # Гео
      elif col_number == 4 or col_number == 6 or col_number == 8:
        if values[col_number][row_number]:
          list_of_values_in_row.append(values[col_number][row_number])
        else:
          list_of_values_in_row.append("")
      # Статус участка
      elif col_number == 9:
        if values[col_number][row_number] and "Участок недр местного значения" in values[col_number][row_number]:
          list_of_values_in_row.append(1)
        elif values[col_number][row_number] and "Участок недр федерального значения" in values[col_number][row_number]:
          list_of_values_in_row.append(2)
        elif values[col_number][row_number]:
          list_of_values_in_row.append(3)
      # Пользователь недр
      elif col_number == 10:
        if values[col_number][row_number] and "ИНН" in values[col_number][row_number]:
          # list_of_values_in_row.append(values[col_number][row_number].split("ИНН")[0].strip(" ("))
          list_of_values_in_row.append(values[col_number][row_number].split("ИНН")[1].strip(": ").strip(")"))
        elif not values[col_number][row_number]:
          list_of_values_in_row.append("нет данных")
        else:
          list_of_values_in_row.append(values[col_number][row_number])
      # Ссылка на вход в систему АСЛН
      elif col_number == 20:
        pass
      else:
        if values[col_number][row_number]:
          list_of_values_in_row.append(values[col_number][row_number])
        else:
          list_of_values_in_row.append("")

    tuple_of_values_in_row = tuple(list_of_values_in_row)
    list.append(tuple_of_values_in_row)

  return list


def create():
  try:  
    connection = connect()
    queries = parse_sql(config.CREATE_TABLES_QUERY_PATH)
    with connection.cursor() as cursor:
      for query in queries:
        cursor.execute(query)
        print("Query is executed")
      connection.commit()
  finally:
    connection.close()
    print("Сonnection is disconnected")


def drop():
  try:  
    connection = connect()
    queries = parse_sql(config.DROP_TABLES_QUERY_PATH)
    with connection.cursor() as cursor:
      for query in queries:
        cursor.execute(query)
        print("Query is executed")
      connection.commit()
  finally:
    connection.close()
    print("Сonnection is disconnected")


def insert_filter_table(filter):

  list = get_list_from_filter(filter)
  table_name = "_".join(filter.split("-"))

  try:  
    connection = connect()
    print("Connect successful")
    cursor = connection.cursor()
    query = f"INSERT INTO `{table_name}` (`name`) VALUES " + ",".join("(%s)" for _ in list)
    values = [item for sublist in list for item in sublist]
    cursor.execute(query, values)
    print("Query is executed")
    connection.commit()
  except pymysql.err.IntegrityError as e:
    if e.args[0] in (1062,):
      print('Невозможно выполнить запрос:', e.args)
      return None
    else:
      raise
  finally:
    connection.close()
    print("Сonnection is disconnected")


def insert_licenses_table(type_of_minerals_id, region_id):

  dir = config.JSON_RESULT_PATH + f"{type_of_minerals_id}/{region_id}/"
  try:
    pages = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
    page = 1
    while page <= pages:
      json_file_name = f"{type_of_minerals_id}_{region_id}_{page}.json"
      json_file_path = dir + json_file_name
      print(json_file_path)
      list = get_list_from_json(json_file_path, type_of_minerals_id, region_id)
      table_name = "`licenses_registry`"
      columns = "`link_to_card`, `reg_number`, `el_image`, `reg_date`, `license_purpose`, "
      columns += "`type_of_minerals`, `plot_name`, `russian_region`, `geo`, `plot_status`, "
      columns += "`inn`, `gov_agency`, `base_doc`, `license_changes`, `license_renewal`, "
      columns += "`order_details`, `termination_date`, `restriction`, `end_date`, `previous_licenses`"

      try:  
        connection = connect()
        print("Connect successful")
        cursor = connection.cursor()
        values = ', '.join(map(str, list))
        query = f"INSERT INTO {table_name} ({columns}) VALUES {values}"
        # print(query)
        cursor.execute(query)
        print("Query is executed")
        connection.commit()
        print(page)
      except Exception as e:
        print(e)
      finally:
        connection.close()
        print("Сonnection is disconnected")
        page += 1
  except Exception as e:
    print(e)


def fetchall_filter_table(filter):
  table_name = "_".join(filter.split("-"))
  try:
    connection = connect()
    print("Connect successful")
    cursor = connection.cursor()
    sql = f"SELECT * FROM `{table_name}`"
    cursor.execute(sql)
    print("Query is executed")
    result = cursor.fetchall()
    print(result)
  except pymysql.err.ProgrammingError as e:
    if e.args[0] in (1146,):
      print('Невозможно выполнить запрос:', e.args)
      return None
    else:
      raise
  finally:
    connection.close()
    print("Сonnection is disconnected")
