from app.db.functions import add_passenger_flow_information, get_passenger_flow_from_db
import pandas as pd
from datetime import datetime

if __name__ == '__main__':
    # res = get_passenger_flow_from_db('Румянцево', 'Солнцевская', '2024-03-25')
    # print(res)

    tmp = pd.read_csv('Пассажиропоток.csv')
    print(tmp)
    for row in tmp.iterrows():
        date_row = row[1]
        # print(date_row)
        day = date_row['dt'][0:2]
        month = date_row['dt'][3:5]
        year = date_row['dt'][6:10]
        # print(date_row['station'], int(date_row['line_number']), date_row['line_name'], date_row['dt'], date_row['passenger_cnt'])
        # print(date_row['station'], int(date_row['line_number']), date_row['line_name'], datetime.fromisoformat(f'{year}-{month}-{day}'), int(date_row['passenger_cnt']))
        # break
        add_passenger_flow_information(date_row['station'], int(date_row['line_number']), date_row['line_name'], datetime.fromisoformat(f'{year}-{month}-{day}'), int(date_row['passenger_cnt']))