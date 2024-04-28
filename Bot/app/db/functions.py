import sqlite3
import datetime
db_name = 'mos_trans_proekt_bot_db.sql'
name_max_length = 255
# TODO REVIEW 20.04.2024
def create_tables_if_not_exists():
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(
            f'''
            CREATE TABLE IF NOT EXISTS giga_chad_match (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version integer NOT NULL,
            id_vacancy INTEGER NOT NULL,
            id_course INTEGER NOT NULL,
            score timestamp NOT NULL);
            --FOREIGN KEY (chat_conditional_branch_id)  REFERENCES ChatConditionalBranches (id) ON DELETE SET NULL);
            '''
        )
        cur.execute(
            f'''
            CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_tg_id varchar({name_max_length}) NOT NULL,
	        dt timestamp NOT NULL,
	        msg_bot text NOT NULL,
	        msg_user text NOT NULL);
	        -- FOREIGN KEY (psychological_state_id)  REFERENCES PsychologicalStates (id) ON DELETE SET NULL);
            ''')

        cur.execute(
            f'''
                    CREATE TABLE IF NOT EXISTS cosine_similarity(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                   id_vacancy INTEGER NOT NULL,
                    id_course INTEGER NOT NULL,
                    cosine_similarity FlOAT NOT NULL);
        	        -- FOREIGN KEY (psychological_state_id)  REFERENCES PsychologicalStates (id) ON DELETE SET NULL);
                    ''')

        cur.execute(
            f'''
                    CREATE TABLE IF NOT EXISTS levenshtein_distance(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                   id_vacancy INTEGER NOT NULL,
                    id_course INTEGER NOT NULL,
                    levenshtein_distance INTEGER NOT NULL);
        	        -- FOREIGN KEY (psychological_state_id)  REFERENCES PsychologicalStates (id) ON DELETE SET NULL);
                    ''')

        cur.execute(
            f'''
                    CREATE TABLE IF NOT EXISTS jaccard_coefficient(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                   id_vacancy INTEGER NOT NULL,
                    id_course INTEGER NOT NULL,
                    jaccard_coefficient FlOAT NOT NULL);
        	        -- FOREIGN KEY (psychological_state_id)  REFERENCES PsychologicalStates (id) ON DELETE SET NULL);
                    ''')

        cur.execute(
            f'''
                            CREATE TABLE IF NOT EXISTS euclidean_distance(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_vacancy INTEGER NOT NULL,
                            id_course INTEGER NOT NULL,
                            euclidean_distance FlOAT NOT NULL);
                	        -- FOREIGN KEY (psychological_state_id)  REFERENCES PsychologicalStates (id) ON DELETE SET NULL);
                            ''')
        # cur.execute(
        #     f'''
        #     CREATE TABLE IF NOT EXISTS PsychologicalStates (
        #     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     name varchar({name_max_length}) NOT NULL,
	    #     typeOfState varchar({name_max_length}) NOT NULL,
	    #     description text NOT NULL);
        #     ''')
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print('Ошибка при работе с SQLite', error)
    finally:
        if conn:
            conn.close()
            print('Соединение с SQLite закрыто')

# TODO: регистрации нет, пока что не нужно

# def user_exists_in_db(user_id):
#     try:
#         conn = sqlite3.connect(db_name)
#         cur = conn.cursor()
#         res = cur.execute(
#             f'''
#             SELECT id, tg_id FROM user
#             WHERE tg_id == {user_id}
#             ORDER BY id DESC
#             '''
#         )
#         result = res.fetchall()
#         conn.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print('Ошибка при работе с SQLite', error)
#     finally:
#         if conn:
#             conn.close()
#             print('Соединение с SQLite закрыто')
#
#     if len(result) == 0:
#         return False
#     return True

def if_none(val):
    if val is None:
        return 'NULL'
    return val


async def save_message_to_db(user_tg_id,
                             msg_bot,
                             msg_user):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(
            f'''
            INSERT INTO chat_history (user_tg_id, dt, msg_bot, msg_user)
            VALUES ('{user_tg_id}', '{datetime.datetime.now()}', '{msg_bot}', '{msg_user}');
            '''
        )
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print('Ошибка при работе с SQLite', error)
    finally:
        if conn:
            conn.close()
            print('Соединение с SQLite закрыто')

async def get_scores_from_db(id_vacancy):
    print(f'get_passenger_flow_from_db. id_vacancy: {id_vacancy}')
    result = None
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        res = cur.execute(
            f'''
            SELECT id_course, score FROM giga_chad_match
            WHERE 1=1
                AND id_vacancy='{id_vacancy}'
            
            CREATE TABLE IF NOT EXISTS giga_chad_match (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version integer NOT NULL,
            id_vacancy INTEGER NOT NULL,
            id_course INTEGER NOT NULL,
            score timestamp NOT NULL);
            '''
        )
        print(dt)
        result = res.fetchall()
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print('Ошибка при работе с SQLite', error)
    finally:
        if conn:
            conn.close()
            # print('Соединение с SQLite закрыто')
    if result is not None and len(result) > 0:
        # print(result[0])
        return result#[0][0]
    else:
        return None

async def get_agg_passenger_flow_from_db(agg, station, dt1, dt2):
    result = None
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        res = cur.execute(
            f'''
            SELECT line_name, {agg}(passenger_cnt) FROM passenger_flow
            WHERE LOWER(station)=LOWER('{station}') 
            AND DATE(dt)>='{dt1}' AND DATE(dt)<='{dt2}'
            GROUP BY line_name
            '''
        )
        result = res.fetchall()
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print('Ошибка при работе с SQLite', error)
    finally:
        if conn:
            conn.close()
            print('Соединение с SQLite закрыто')
    if result is not None and len(result) > 0:
        return result
    else:
        return None

def add_passenger_flow_information(station, line_number, line_name, dt, passenger_cnt):
    result = None
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        res = cur.execute(
            f'''
            INSERT INTO passenger_flow (station, line_number, line_name, dt, passenger_cnt)
            VALUES ('{station}', '{line_number}', '{line_name}', '{dt}', '{passenger_cnt}');
            '''
        )
        result = res.fetchall()
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print('Ошибка при работе с SQLite', error)
    finally:
        if conn:
            conn.close()
            # print('Соединение с SQLite закрыто')
    if result is not None:
        return result
    else:
        return None

# async def save_psychological_state_to_db(name, typeOfState, description):
#     try:
#         conn = sqlite3.connect(db_name)
#         cur = conn.cursor()
#         cur.execute(
#             f'''
#             INSERT INTO PsychologicalStates (name, typeOfState, description)
#             VALUES ('{name}', '{typeOfState}', '{description}');
#             '''
#         )
#         conn.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print('Ошибка при работе с SQLite', error)
#     finally:
#         if conn:
#             conn.close()
#             print('Соединение с SQLite закрыто')

# async def save_conditional_branch_to_db(psychological_state_id, name, condition, branch):
#     psychological_state_id = if_none(psychological_state_id)
#     try:
#         conn = sqlite3.connect(db_name)
#         cur = conn.cursor()
#         cur.execute(
#             f'''
#             INSERT INTO ChatConditionalBranches (psychological_state_id, name, condition, branch)
#             VALUES ({psychological_state_id}, '{name}', '{condition}', '{branch}');
#             '''
#         )
#         conn.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print('Ошибка при работе с SQLite', error)
#     finally:
#         if conn:
#             conn.close()
#             print('Соединение с SQLite закрыто')

# example of insert

# async def save_form_to_db(user_id, name, photo_name, photo_path, description):
#     if name == None:
#         name_str = "NULL"
#     else:
#         name_str = f'''"{name}"'''
#     if photo_name == None:
#         photo_name_str = "NULL"
#     else:
#         photo_name_str = f'''"{photo_name}"'''
#     if photo_path == None:
#         photo_path_str = "NULL"
#     else:
#         photo_path_str = f'''"{photo_path}"'''
#     if description == None:
#         description_str = "NULL"
#     else:
#         description_str = f'''"{description}"'''
#
#     try:
#         conn = sqlite3.connect(db_name)
#         cur = conn.cursor()
#         cur.execute(
#             f'''
#             INSERT INTO user (tg_id, name, photo_name, photo_path, description, type)
#             VALUES ({user_id}, {name_str}, {photo_name_str}, {photo_path_str}, {description_str}, "user");
#             '''
#         )
#         conn.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print('Ошибка при работе с SQLite', error)
#     finally:
#         if conn:
#             conn.close()
#             print('Соединение с SQLite закрыто')

# example of select

# async def get_name_from_db(user_id):
#     result = None
#     try:
#         conn = sqlite3.connect(db_name)
#         cur = conn.cursor()
#         res = cur.execute(
#             f'''
#             SELECT name, tg_id FROM user
#             WHERE tg_id == {user_id}
#             ORDER BY id DESC
#             LIMIT 1
#             '''
#         )
#         result = res.fetchall()
#         conn.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print('Ошибка при работе с SQLite', error)
#     finally:
#         if conn:
#             conn.close()
#             print('Соединение с SQLite закрыто')
#
#     if result is not None:
#         return result[0][0]
#     else:
#         return None

# async def get_psychological_state_id(psychological_state):
#     result = None
#     try:
#         conn = sqlite3.connect(db_name)
#         cur = conn.cursor()
#         res = cur.execute(
#             f'''
#             SELECT id FROM PsychologicalStates
#             WHERE name == '{psychological_state}'
#             '''
#         )
#         result = res.fetchall()
#         conn.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print('Ошибка при работе с SQLite', error)
#     finally:
#         if conn:
#             conn.close()
#             print('Соединение с SQLite закрыто')
#
#     if result is not None:
#         return result[0][0]
#     else:
#         return None

# async def get_chat_conditional_branches_from_db(psychological_state):
#     result = None
#     psychological_state_id = await get_psychological_state_id(psychological_state)
#     try:
#         conn = sqlite3.connect(db_name)
#         cur = conn.cursor()
#         res = cur.execute(
#             f'''
#             SELECT condition, branch FROM ChatConditionalBranches
#             WHERE psychological_state_id == '{psychological_state_id}'
#             '''
#         )
#         result = res.fetchall()
#         conn.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print('Ошибка при работе с SQLite', error)
#     finally:
#         if conn:
#             conn.close()
#             print('Соединение с SQLite закрыто')
#
#     if result is not None:
#         return result
#     else:
#         return None

# time example
# async def add_match_to_db(user_id, match_id):
#     print("test1")
#     try:
#         sqliteConnection = sqlite3.connect(db_name,
#                                            detect_types=sqlite3.PARSE_DECLTYPES |
#                                                         sqlite3.PARSE_COLNAMES)
#         cur = sqliteConnection.cursor()
#         print("Connected to SQLite")
#         sqlite_insert_with_param = """
#                                     INSERT INTO match ('first_tg_id', 'second_tg_id', 'time')
#                                     VALUES (?, ?, ?);
#                                     """
#
#         data_tuple = (user_id, match_id, datetime.datetime.now())
#         cur.execute(sqlite_insert_with_param, data_tuple)
#         sqliteConnection.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print('Ошибка при работе с SQLite', error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print('Соединение с SQLite закрыто')


