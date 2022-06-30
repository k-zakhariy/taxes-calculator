from csv import DictReader
from genericpath import exists
from tabulate import tabulate
from os.path import exists
import sys
import requests
import time

import html2text
text_maker = html2text.HTML2Text()

table = [['Дата', 'Значення', 'Валюта', 'Курс', 'Сумма']]
total_income = 0
total_five_percent = 0
total_ten_percent = 0
if not exists('data.csv'):
    print('File data.csv does not exists')
    sys.exit()

with open('data.csv') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        date = row["date"]
        value = row['value']
        currency = row['currency']

        result = 0
        currencyAmount = 0
        if currency != 'UAH':
            response = requests.get(
                "https://bank.gov.ua/NBU_Exchange/exchange?date="+date+"&json")

            if response.text[0] == '<':
                print("Failed for date - "+date)
                print(text_maker.handle(response.text))
                time.sleep(3)
                continue

            time.sleep(2)
            resJson = response.json()

            for x in resJson:
                if x["CurrencyCodeL"] == currency and currency != 'UAH':
                    currencyAmount = x['Amount']
                    result = round(float(x["Amount"]) * float(value))

        else:
            result = float(value)
            value = ""

        total_income += result

        table.append([date, value, currency, currencyAmount,
                     "{:,.2f} UAH".format(result)])

    total_five_percent = (total_income / 100) * 5
    total_ten_percent = ((total_income - total_five_percent) / 100) * 10

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    print(tabulate([["Total", "5%", "10%"], [total_income, total_five_percent,
          total_ten_percent]], headers='firstrow', tablefmt='fancy_grid'))
