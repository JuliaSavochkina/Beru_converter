import csv
import xmltodict

"""
Для работы с задачей нужно:
1. В проекте re:revisor в файле 20924_beru.yml изменить даты в uri для AR части.
Заменить часть EP конфига, начиная с 26 строки на

        action_code:
          constant_value: 1
        tariff_code:
          constant_value: 1
        datetime_action:
          path: dateUpdated
        price: cart
        reward: payment
        tracking: clid
        status: status
      orders_filter_rules:
        status:
          allowed_values:
            - 'APPROVED'
          remove_field: True
          
[ничего не комитьте!]          
2. Запустить проект и локально запросить AR для программы 20924. Полученный файл можно перенести в текущий проект.
3. В текущем проекте добавить путь к полученному файлу в качестве первого аргумента функции main, название файла для
менеджера в качестве второго аргумента функции main.
4. Запустить текущий проект (62 строка). Полученный csv файл приложите в задачу. Наслаждайтесь - вы великолепны!
"""


def xml_to_dict(file_name):
    """
    Парсит файл формата xml в словарь и возвращает генератор из дейсвтий, удаляет поля tariff_code и action_code
    :param file_name: название файла с FTP после локального прогона
    :return: генератор
    """
    with open(file_name) as fd:
        doc = xmltodict.parse(fd.read())['payment_list']['payment']
        for action in doc:
            action.pop('tariff_code')
            action.pop('action_code')
            yield action


def main(name_file_from, name_file_to):
    """
    Создает файл csv формата с заданным именем [Beru_AR_month-year.csv] добавляет в него строку заголовков и данные
    по дейсвтиям построчно.
    :param name_file_from: Название файла из которого нужно забирать данные
    :param name_file_to: Название файла в который нужно сложить данные
    """
    with open(name_file_to, "a", newline="") as f:
        columns = ["uid", "order_id", "datetime_action", "price", "payment", "tracking"]
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for item in xml_to_dict(name_file_from):
            writer.writerow(item)


if __name__ == '__main__':
    main('имя_файла_с_актуальной выгрузкой.xml', 'Beru_AR_test_orders.csv')
