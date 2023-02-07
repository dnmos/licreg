import json

# Реестр недропользователей 
with open('/home/dm/app/python/bonalogru/data/licenses-registry/licenses-registry.json') as file:
  licenses_registry = json.load(file)

rows = licenses_registry['result']['data']['rows']
cols = licenses_registry['result']['data']['cols']
registry = []
for row in rows:
  registry.append({
    "Ссылка на карточку лицензии":\
      licenses_registry['result']['data']['values'][0][int(row[0])],
    "Государственный регистрационный номер":\
      licenses_registry['result']['data']['values'][1][int(row[0])],
    "Дата присвоения регистрационного номера лицензии":\
      licenses_registry['result']['data']['values'][3][int(row[0])],
    "Целевое назначение лицензии":\
      licenses_registry['result']['data']['values'][4][int(row[0])],
    "Вид полезного ископаемого":\
      licenses_registry['result']['data']['values'][5][int(row[0])],
    "Наименование участка недр":\
      licenses_registry['result']['data']['values'][6][int(row[0])],
    "Наименование субъекта РФ":\
      licenses_registry['result']['data']['values'][7][int(row[0])],
    "Статус участка недр":\
      licenses_registry['result']['data']['values'][9][int(row[0])],
    "Сведения о пользователе недр":\
      licenses_registry['result']['data']['values'][10][int(row[0])],
    "Наименование органа, выдавшего лицензию":\
      licenses_registry['result']['data']['values'][11][int(row[0])],
    "Дата окончания срока действия лицензии":\
      licenses_registry['result']['data']['values'][18][int(row[0])],
  })
with open('/home/dm/app/python/bonalogru/data-result/licenses-registry.json', 'w') as file:
  json.dump(registry, file, indent=4, ensure_ascii=False)
