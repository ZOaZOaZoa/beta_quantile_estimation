import pandas as pd
import numpy as np
import os
from datetime import datetime
from scipy.special import betaincinv
from tqdm import tqdm

def get_col_no_blank(df, col_name):
    '''Убирает из серии NaN и нулевые значения'''
    k = pd.Series(df[df[col_name].apply(lambda x: type(x) in [int, np.int64, float, np.float64])][col_name]).values.astype(np.float64)
    k = k[~np.isnan(k)]
    k = k[k!=0]

    return k

def main():
    #Открытыие Excel файла
    while True:
        print('Введите название (или путь) файла Excel с данными: ', end='')
        file = input()
        if os.path.isfile(file):
            print(f'\nОткрываем файл {file}')
            break

        print(f'Файла {file} не существует')


    xl = pd.ExcelFile(file)
    sheets = xl.sheet_names

    if len(sheets) == 0:
        print('Не найдено листов в файле')
        exit()

    #Выбор листа
    while True:
        print('Найдены следующие листы: ', end='')
        print(*sheets, sep='; ')
        if len(sheets) == 1:
            print(f'Выбран лист {sheets[0]}\n')
            sheet = sheets[0]
            break

        print('Введите название листа, откуда брать данные: ', end='')
        sheet = input()
        if sheet in sheets:
            print(f'Выбран лист {sheets[0]}\n')
            break

        print(f'Листа {sheet} среди найденных листов нет')

    print('Парсим данные')
    df = xl.parse(sheet)
    print('Найдены следующие столбцы:', *df.columns)
    print('Первые три считаем следующими столбцами: название, значение альфа, значение бета')
    column = df.columns[0]
    alpha_col = df.columns[1]
    beta_col = df.columns[2]
    data_df = df[[column, alpha_col, beta_col]]

    #Выбор квантиля
    while True:
        user_input = input('Введите уровень вероятности для расчёта квантиля (0.95 по умолчанию): ')
        if user_input == '':
            probability = 0.95
            break
        
        try:
            probability = int(user_input)
            if probability >= 0 and probability <= 1:
                break

            print('Неправильное значение вероятности! Введите число от 0 до 1.')
        except ValueError:
            print(f'Получено не число! Введите число от 0 до 1. Получено {user_input}.')

    protocol_columns = ['Название', 'Альфа', 'Бета', f'Квантиль{probability}']
    protocol_rows = []

    for i in tqdm(range(len(data_df)), leave=False):
        row = data_df.loc[i]
        alpha = row[alpha_col]
        beta = row[beta_col]
        quantile = betaincinv(alpha, beta, probability)
        protocol_rows += [row.tolist() + [quantile,]]
    
    cur_datetime = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
    protocol = pd.DataFrame(protocol_rows, columns=protocol_columns)
    if not os.path.isdir('protocol'):
        os.mkdir('protocol')
    protocol.to_excel(f'protocol\\{cur_datetime}.xlsx')
    
    print(f'Протокол сохранен в: {os.getcwd()}\\protocol')


if __name__ == '__main__':
    main()