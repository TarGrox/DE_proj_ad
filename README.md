## Hello!
### This is Data Engineer project

Switch from weather.gov to lamoda.ru

### Задача:
Спарсить информацию по продуктам, категориям с сайта [Lamoda.ru](Lamoda.ru);
Спроектировать и создать БД на MySQL;
Отображение через сайт? (ajax, фильтры, bootstrap и тд)

1. #### Парсинг:
    1. Создать черновой вариант Парсера:
        * [х] Записать (иметь возможность) все ссылки на продукты с выбранной категории;
        * [ ] Записать (иметь возможность) всю информацию со страницы продукта:
            * [x] Name;
            * [x] Price;
            * [x] Size;
            * [ ] Comments:
                * [ ] Тело отзыва;
                * [ ] Оценка.
            * [x] Состав:
                от категории к категории имеет сложный состав => какие-то общие правила хранения?
            * [x] Img_link(s?).
    2. [ ] Отрефакторить код:
        note: получение html_response сделать через async/await;
2. #### БД, MySQL:
    1. Спроектировать БД;
        Примерный эскиз  от 10.03.2022
        ![DB_10.03.2022](/utils/DB_10.03.2022.png)
    2. Залить инфу в созданную БД;

