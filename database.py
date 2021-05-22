import config.conn as db
import pandas as pd
from sqlalchemy import create_engine

# DB에 연결
engine = create_engine(db.conn)
conn = engine.connect()

def insert(df, player):
    player_ = player.replace(" ", "_").lower()
    df.to_sql(name=player_, con=engine, if_exists='append', index=True)

def select(player):
    player_ = player.replace(" ", "_").lower()
    data = pd.read_sql_query(f"select * from {player_} where record=0", engine)
    return data
    
def recorded(player, id):
    player_ = player.replace(" ", "_").lower()
    data = pd.read_sql_query(f"update {player_} set record=1 where id={id}", engine)
    return data