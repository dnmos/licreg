# licreg

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Initial server setup](#initial-server-setup)

## General info
Python scraping sites, data normalization, saving data to a mysql database, sql queries
	
## Technologies
Project is created with:
* ubuntu 22.04
* python 3.11.1
* selenium 4.8.0
* selenium_wire 5.1.0
* beautifulsoup4 4.11.2
	
## Initial server setup
Обновляем систему

```
$ sudo apt update && sudo apt upgrade 
```
Устанавливаем Python 3.11 сборкой из исходников
```
$ sudo apt install wget build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
$ wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz
$ tar -xzvf Python-3.11.1.tgz
$ cd Python-3.11.1
$ ./configure --enable-optimizations --prefix=/home/www/.python3.11
$ make -j4 && sudo make altinstall
```

Добавляем Python3.11 в PATH
```
nano ~/.bashrc
export PATH=$PATH:/home/www/.python3.11/bin
source ~/.bashrc
```
Клонируем репозиторий
```
$ git clone https://github.com/dnmos/licreg.git
$ cd licreg
```
Создаем виртуальное окружение
```
$ python3.11 -m venv env
$ . ./env/bin/activate
```
Устанавливает selenium и bs4
```
$ pip install selenium
$ pip install selenium-wire
$ pip install beautifulsoup4
$ pip install lxml
$ pip install PyVirtualDisplay
```
Устанавливаем Google Chrome
```
$ sudo apt-get install xvfb
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo apt install ./google-chrome-stable_current_amd64.deb
``` 
