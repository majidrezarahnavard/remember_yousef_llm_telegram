# Remember Yousef llm telegram
telegram bot for serve a large language model

این پروژه به یاد یوسف قبادی ساخته شده است.

برای اجرا کردن این پروژه اول باید پروژه زیر را اجرا کنید:

```
https://github.com/majidrezarahnavard/remember_yousef_llm_serve
```

روی پورت ۸۰۸۰ سرویس اولاما اجرا شده است.

# Bot Father

با استفاده از بات زیر یک کد اجرا باید بگیرید:

```
https://t.me/BotFather
```

## .env

یک فایل .env بسازید و مثل .env.default مقدار توکن رو قرار دهید.


# docker-compose

داکر باید روی سیستم نصب داشته باشید و دستور زیر را اجرا کنید:

```
docker build -t llm-telegram-app .
sudo docker-compose up
```

# Database

این سرویس دارای دیتابیس هست و باید جداول ایجاد شوند:

مقادیر زیر را حتما تغییر دهید

```
POSTGRES_USER: user
POSTGRES_PASSWORD: pass
POSTGRES_DB: telegram
```

# Initial database

```
sudo docker-compose -f docker-compose.yml exec liquibase /bin/sh 

liquibase update --url=jdbc:postgresql://postgres-telegram:5432/telegram?currentSchema=public --changelog-file=changelog.xml --username=user --password=pass

```

# Adminer

برای دسترسی راحت به دیتابیس از آدرس زیر استفاده کنید

```
http://127.0.0.1:10000/?pgsql=postgres-telegram&username=user&db=telegram&ns=public&select=faqs
```