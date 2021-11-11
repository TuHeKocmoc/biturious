# biturious
## GUI Python 3 Bitcoin miner

### ENG:

#### Authorization:
- Authorization windows, registration, restoring password using saves to database SQLite
- Linking email using code in the letter
- Hashing passwords Double SHA-512 using global and local salt
- Session saving in settings.txt

#### Main window:
- Mining Bitcoin using nightminer
- Showing Bitcoin exchange rate

#### Menu:
- Bitcoin exchange rate graphic and exchange in both sides using Binance and Bitcoin API
- Speedtest
- Settings (changing login, password and some useful stuff e.g. api-key and secret-key for Binance API, saving to the settings.txt)
- Help

#### Speedtest:
- Shows download speed, upload speed and ping
- ProgressBar to know how much time spent and how much time remaining
- Using multithreading for achieving targets

#### Utils:
- PyQT5 for GUI
- requirements.txt
- pyinstaller
- speedtest-cli for speedtest
- urllib3 and requests for http requests (GET)


### RUS:

#### Авторизация:
- Окна авторизации, регистрации и восстановления пароля с сохранением в базу данных SQLite
- Привязка почты, используя код из письма
- Хэширование паролей Double SHA-512, используя глобальный и локальный ключ
- Сохранение сессии в settings.txt

#### Основное окно:
- Майнинг Bitcoin используя nightminer
- Показ курса Bitcoin

#### Меню:
- График курса Bitcoin и обмен в обе стороны используя API Binance и Bitcoin
- Speedtest
- Настройки (смена логина, пароля, указание api-key и secret-key, сохранение в settings.txt)
- Помощь

#### Speedtest:
- Показывает скорость загрузки, отдачи и пинг
- ProgressBar для понимания, сколько времени прошло и сколько осталось ждать
- Использование мультипоточности для достижения двух целей выше

#### Другое:
- PyQT5 для GUI
- requirements.txt
- pyinstaller
- speedtest-cli для speedtest
- urllib3 и requests для http запросов (GET)

