import config.conn as db
import pandas as pd
from sqlalchemy import create_engine
import crawler
import pymysql

# DB에 연결
engine = create_engine(db.conn_pd)
conn = engine.connect()
cursor = db.conn_py.cursor(pymysql.cursors.DictCursor)

def insert(df, player):
    player_ = player.replace(" ", "_").lower()
    table_df = pd.read_sql_query("show tables", engine)

    if player_ in table_df['Tables_in_lol'].values.tolist():
        data = pd.read_sql_query(f"select id from {player_}", engine)
        df = pd.concat([data, df])
        df = df.drop_duplicates(['id'], keep='first')
        df = df.dropna(axis=0)

        if df.empty == False:
            df.to_sql(name=player_, con=engine, if_exists='append', index=True)
    else:
        print('no table')
        df.to_sql(name=player_, con=engine, if_exists='append', index=True)

def select_record(player):
    player_ = player.replace(" ", "_").lower()
    data = pd.read_sql_query(f"select * from {player_} where record=0 and failed=0", engine)
    return data

def select_upload(player):
    player_ = player.replace(" ", "_").lower()
    data = pd.read_sql_query(f"select * from {player_} where upload=0 and failed=0", engine)
    return data
    
def recorded(player, id):
    player_ = player.replace(" ", "_").lower()
    sql = f"update {player_} set record=1 where id={id}"
    cursor.execute(sql)
    db.conn_py.commit()

def uploaded(player, id):
    player_ = player.replace(" ", "_").lower()
    sql = f"update {player_} set upload=1 where id={id}"
    cursor.execute(sql)
    db.conn_py.commit()

def failed(player, id):
    player_ = player.replace(" ", "_").lower()
    sql = f"update {player_} set failed=1 where id={id}"
    cursor.execute(sql)
    db.conn_py.commit()
