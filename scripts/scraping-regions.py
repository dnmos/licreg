import requests
import json
from bs4 import BeautifulSoup


def get_source_html():

	# Коды субъектов РФ
	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"
	}
	url = "https://www.buxprofi.ru/spravochnik/kody-regionov-ili-subektov-rf-dlja-nalogovoj" 

	try:
		request = requests.get(url, headers=headers)
		content = request.text
		soup = BeautifulSoup(content, "lxml")
		table = soup.find_all("table")[1]
		trs = table.find_all("tr")
		regions = []
		for tr in trs[1:]:
			print(tr.find_all("td")[0].find("span").contents[0] + " " + tr.find_all("td")[1].find("span").contents[0])
			regions.append({
				'Код субъекта РФ': tr.find_all("td")[0].find("span").contents[0],
				'Наименование субъекта РФ': tr.find_all("td")[1].find("span").contents[0]
			})

		with open('/home/dm/app/python/bonalogru/data/regions.json', 'w') as file:
			json.dump(regions, file, indent=4, ensure_ascii=False)

	except Exception as ex:
		print(ex)


def main():
	get_source_html(url="https://rfgf.ru/ReestrLic/")


if __name__ == "__main__":
	main()