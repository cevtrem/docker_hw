# Инструкция по запуску Django Stocks API в Docker

**1. Сначала создайте файл db.sqlite3 локально:**

```bash
touch db.sqlite3
chmod 666 db.sqlite3
```

**2. Запустите контейнер без монтирования для первого запуска:**
```bash
docker run -p 8000:8000 stocks-api
```

**3. После этого остановите контейнер и выполните:**
Скопируйте файл БД из контейнера:
```bash
docker cp <container_id>:/app/db.sqlite3 .
```

**4. Теперь можно запускать с монтированием:**
```bash
docker run -p 8000:8000 -v ./db.sqlite3:/app/db.sqlite3 stocks-api
```

**5. Войдите в контейнер чтобы создать записи в БД:**
```bash
docker exec -it <container_id> python manage.py shell
```

В shell:
```bash
from logistic.models import Product, Stock, StockProduct
p1 = Product.objects.create(title="Ноутбук", description="Мощный ноутбук")
p2 = Product.objects.create(title="Телефон", description="Смартфон")
s1 = Stock.objects.create(address="Склад 1")
StockProduct.objects.create(stock=s1, product=p1, quantity=5, price=999.99)
StockProduct.objects.create(stock=s1, product=p2, quantity=10, price=499.99)
```

**6. Проверьте endpoints:**
```bash
curl http://localhost:8000/api/v1/products/
```

или:
GET http://localhost:8000/api/v1/products/
GET http://localhost:8000/api/v1/stocks/



