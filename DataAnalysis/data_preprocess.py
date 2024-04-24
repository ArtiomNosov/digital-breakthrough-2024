import pandas as pd

path = "dataset.xlsx"

data = pd.read_excel(path)
data = data.rename(columns={'Дата': 'Название линии'})

# Исправление данных
replacement_dict = {
    "АРБАТСК-ПОКРОВСК": "Арбатско-Покровская",
    "БКЛ": "Большая кольцевая линия",
    "СЕРПУХОВ-ТИМИРЯЗ": "Серпуховско-Тимирязевская",
    "МЦК": "Московское центральное кольцо",
    "СОЛНЦЕВСКАЯ ЛИН.": "Солнцевская",
    "ТАГАНСК-КРАСНОПР": "Таганско-краснопресненская"
}

# Замена значений
data['Название линии'] = data['Название линии'].replace(replacement_dict)
data.to_excel('dataset_fixed.xlsx', index=False)
data.head()

data = pd.read_excel(path)
data = data.rename(columns={'Дата': 'Название линии'})

data.insert(loc=3, column='Дата', value=0)
data.insert(loc=4, column='Пассажиропоток', value=0)
data.insert(loc=5, column='Станция 2.0', value=0)

# Внутри цикла преобразование датафрейма к виду таблицы БД -- Станция - номер линии - название линии - дата
for i in range(len(data.columns[6:])):
  for j in range(311):
    data.loc[j + 311 * i, 'Дата'] = data.columns[i+6]
    data.loc[j + 311 * i, 'Пассажиропоток'] = data.iloc[j, i + 6]
    data.loc[j + 311 * i, 'Станция 2.0'] = data.loc[j, 'Станция']
    data.loc[j + 311 * i, 'Номер линии'] = data.loc[j, 'Номер линии']
    data.loc[j + 311 * i, 'Название линии'] = data.loc[j, 'Название линии']

# Избавление от лишнего столбца грядет
data['Станция'] = data['Станция 2.0']
# Лишняя, создана исключительно для цикла
columns_to_drop = ['Станция 2.0']
data = data.drop(columns=columns_to_drop)
data = data.iloc[:, :5]

# Для БД
data = data.rename(columns={'Станция': 'station', 'Пассажиропоток': 'passenger_cnt',
                            'Номер линии': 'line_number', 'Название линии': 'line_name', 'Дата': 'dt'})

# Исправление данных
replacement_dict = {
    "АРБАТСК-ПОКРОВСК": "Арбатско-Покровская",
    "БКЛ": "Большая кольцевая линия",
    "СЕРПУХОВ-ТИМИРЯЗ": "Серпуховско-Тимирязевская",
    "МЦК": "Московское центральное кольцо",
    "СОЛНЦЕВСКАЯ ЛИН.": "Солнцевская",
    "ТАГАНСК-КРАСНОПР": "Таганско-краснопресненская"
}

# Замена значений
data['line_name'] = data['line_name'].replace(replacement_dict)

# Эскпорт
data.to_csv('Пассажиропоток.csv', index_label='id')
