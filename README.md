# LTLCalc — Калькулятор стоимости доставки

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![Status](https://img.shields.io/badge/status-production-success)
![License](https://img.shields.io/badge/license-MIT-green)

LTLCalc — веб-приложение для расчёта стоимости доставки грузов по технологии Less Than Truckload (LTL).

Приложение позволяет автоматически рассчитывать объём груза, выбирать подходящий тариф, учитывать коэффициенты перевозки и формировать итоговую стоимость доставки через удобный веб-интерфейс.

---

# Содержание

- [Технологии](#технологии)
- [Возможности](#возможности)
- [Начало работы](#начало-работы)
- [Использование](#использование)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Структура проекта](#структура-проекта)
- [Переменные окружения](#переменные-окружения)
- [Резервное копирование](#резервное-копирование)
- [Безопасность](#безопасность)
- [FAQ](#faq)
- [To Do](#to-do)
- [Команда проекта](#команда-проекта)

---

# Технологии

Проект разработан с использованием следующих технологий:

- Python 3.11+
- Streamlit
- SQLite
- Pandas
- NumPy
- Pillow
- OpenPyXL
- Python-dotenv
- Nginx
- Systemd
- Ubuntu Server 24.04 LTS

---

# Возможности

Основные возможности приложения:

- расчёт стоимости доставки;
- автоматический расчёт объёма;
- работа с тарифами;
- хранение данных в SQLite;
- авторизация пользователей;
- административная панель;
- импорт и экспорт Excel;
- управление коэффициентами;
- работа через браузер;
- адаптивный интерфейс.

---

# Начало работы

## Требования

Для установки необходимы:

- Ubuntu Server 24.04 LTS
- Python 3.11+
- Git
- pip
- venv

Проверка версий:

```bash
python3 --version
pip3 --version
```

---

## Клонирование проекта

```bash
git clone https://github.com/mefyqe/logistics-calculator-1.git

cd logistics-calculator-1
```

---

## Создание виртуального окружения

```bash
python3 -m venv .venv
```

Активация

```bash
source .venv/bin/activate
```

---

## Установка зависимостей

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

# Использование

После установки выполните запуск приложения:

```bash
streamlit run app.py
```

По умолчанию приложение будет доступно по адресу

```
http://localhost:8501
```

Если используется собственный порт:

```bash
streamlit run app.py --server.port 8502
```

---

# Разработка

## Создание файла настроек

Создайте файл

```
.env
```

пример содержимого

```env
APP_NAME=LTLCalc

SECRET_KEY=ChangeThisSecret

DATABASE=database/database.db

UPLOAD_DIR=uploads

ADMIN_LOGIN=admin

ADMIN_PASSWORD=admin

DEBUG=False
```

---

## База данных

При первом запуске приложение автоматически создаст:

```
database/database.db
```

Если используется новая установка, убедитесь, что существует каталог

```
database/
```

---

## Создание администратора

Если база данных пустая, первый пользователь создаётся автоматически согласно параметрам:

```env
ADMIN_LOGIN=admin

ADMIN_PASSWORD=admin
```

После первого входа рекомендуется изменить пароль.

---

# Запуск Development сервера

```bash
source .venv/bin/activate

streamlit run app.py
```

---

# Production запуск

Создать сервис

```
sudo nano /etc/systemd/system/ltlcalc.service
```

Пример:

```ini
[Unit]
Description=LTLCalc

After=network.target

[Service]

User=www-data

WorkingDirectory=/opt/ltlcalc

ExecStart=/opt/ltlcalc/.venv/bin/streamlit run app.py --server.port 8502

Restart=always

Environment=PYTHONUNBUFFERED=1

[Install]

WantedBy=multi-user.target
```

Запуск

```bash
sudo systemctl daemon-reload

sudo systemctl enable ltlcalc

sudo systemctl start ltlcalc
```

Проверка

```bash
sudo systemctl status ltlcalc
```

---

# Nginx

Пример конфигурации

```nginx
server {

    listen 80;

    server_name ltlcalc.ru;

    location / {

        proxy_pass http://127.0.0.1:8502;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    }

}
```

После изменения

```bash
sudo nginx -t

sudo systemctl reload nginx
```

---

# Тестирование

Проверка запуска приложения

```bash
streamlit run app.py
```

Проверка зависимостей

```bash
pip check
```

При наличии unit-тестов:

```bash
pytest
```

---

# Deploy и CI/CD

Для обновления проекта достаточно выполнить:

```bash
cd /opt/ltlcalc

git pull

source .venv/bin/activate

pip install -r requirements.txt

sudo systemctl restart ltlcalc
```

---

# Структура проекта

```
project/

├── app.py

├── pages/

├── modules/

├── database/

│   └── database.db

├── uploads/

├── static/

├── config/

├── requirements.txt

├── .env

├── README.md

└── .venv/
```

---

# Переменные окружения

| Переменная | Назначение |
|------------|------------|
| SECRET_KEY | секретный ключ |
| DATABASE | путь к SQLite |
| ADMIN_LOGIN | логин администратора |
| ADMIN_PASSWORD | пароль администратора |
| DEBUG | режим разработки |
| UPLOAD_DIR | каталог загрузок |

---

# Резервное копирование

Рекомендуется регулярно сохранять:

```
database/

uploads/

.env
```

Пример:

```bash
tar -czf backup.tar.gz database uploads .env
```

---

# Безопасность

Рекомендуется:

- использовать HTTPS;
- изменить пароль администратора;
- не хранить `.env` в Git;
- регулярно обновлять зависимости;
- использовать Firewall;
- выполнять резервное копирование базы данных.

---

# FAQ

### Не открывается сайт

Проверьте:

```
systemctl status ltlcalc
```

---

### Ошибка ModuleNotFoundError

Установите зависимости

```bash
pip install -r requirements.txt
```

---

### Ошибка Permission denied

Проверьте права доступа

```bash
chmod -R 755 .
```

---

### Приложение недоступно извне

Проверьте:

- Firewall
- Nginx
- Port Forwarding
- DNS

---

# To Do

- [x] Реализован калькулятор доставки
- [x] Авторизация пользователей
- [x] Импорт Excel
- [x] Экспорт Excel
- [x] SQLite
- [ ] PostgreSQL
- [ ] Docker
- [ ] CI/CD
- [ ] Автоматическое резервное копирование

---

# Команда проекта

Разработчик

**Никита**

GitHub:

https://github.com/mefyqe

---

# Лицензия

Проект распространяется по лицензии MIT.

---

# Источники

- Python
- Streamlit
- SQLite
- OpenPyXL
- Pandas
- NumPy