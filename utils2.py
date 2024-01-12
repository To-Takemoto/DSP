import utils, settings
import sqlite3
db_path = utils.db_path

#####

schema = settings.screen_time_table_schema

#####

def create_table(schema, table_name = None, db_path = None):
    """
    与えられたカラムとテーブル名に従ってDBに新たにテーブルを作るための関数
    """
    if db_path == None:
        db_path = settings.db_path

    if table_name == None:
        table_name = schema["table_name"]
    columns = schema["columns"]

    columns_sql = ", ".join([f"{col['name']} {col['type']}" for col in columns])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(create_table_sql)

    conn.commit()
    conn.close()

create_table(schema)