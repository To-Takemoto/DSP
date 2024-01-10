'''
目次
show_data               :データをプリント
data_exists             :特定のデータが存在しているかを先にverify
insert_data             :上と連携して、データinsert時に重複があった場合はスキップできる関数
insert_data_hard        :重複データの有無関係なくinsertする関数
select_data             :データを戻り値としてselectする関数。該当するのは全て出てくる
select_one_data         :上に対して、一つのみselectしてくれるモノ
count_data              :対象テーブルにどれだけデータが格納されてるかをintで返す
get_columns             :対象テーブルのカラムを返す
'''


import sqlite3
import settings


######
#以下がデフォルトの接続先DB
db_path = settings.db_path
######

class DBHandler:

    def __init__(self, db_path):
        self.db_path = db_path
        print(f"connecting to {self.db_path}")

    def show_data(self, table_name):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        sql_select = f'SELECT * FROM {table_name};'
        cur.execute(sql_select)

        #print(get_columns(table_name))
        for r in cur:
            print(r)

        conn.close()

    def data_exists(self, table, data, check_columns=None):
        """
        Check if the data with specific columns already exists in the table.
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Determine which columns to check
        if check_columns is None:
            check_columns = data.keys()

        # Create the query to check for existing data
        query = f"SELECT * FROM {table} WHERE " + " AND ".join([f"{k} = ?" for k in check_columns])

        # Prepare the values for the columns to be checked
        check_values = [data[k] for k in check_columns]

        cur.execute(query, tuple(check_values))
        exists = cur.fetchone() is not None

        conn.close()
        return exists

    def insert_data(self, table, data, check_columns=None):
        """
        Insert data into the table if it does not already exist, based on specific columns.
        table: Name of the table to insert data into.
        data: Dictionary of data to insert.
        check_columns: List of columns to check for existing data. If None, all columns are checked.
        """
        # Check if the data already exists based on specific columns
        if self.data_exists(table, data, check_columns):
            print("Data already exists with specified columns, skipping insert.")
            return

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Create the column names for the INSERT
        columns = ",".join(data.keys())

        # Create the placeholders for VALUES
        values = ",".join(["?"] * len(data))

        query = f"INSERT INTO {table} ({columns}) VALUES ({values});"

        cur.execute(query, tuple(data.values()))

        conn.commit()
        conn.close()

    def insert_data_hard(self, table, data):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Create the column names for the INSERT
        columns = ",".join(data.keys())

        # Create the placeholders for VALUES
        values = ",".join(["?"] * len(data))

        query = f"INSERT INTO {table} ({columns}) VALUES ({values});"

        cur.execute(query, tuple(data.values()))

        conn.commit()
        conn.close()

    def select_data(self, table_name, conditions=None, fields=None):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        query = f"SELECT {fields or '*'} FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
            
        cur.execute(query)
        records = cur.fetchall()
        
        conn.close()
        
        return records

    def select_one_data(self, table_name, conditions=None, fields=None):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        query = f"SELECT {fields or '*'} FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        query += f" LIMIT 1"
            
        cur.execute(query)
        record = cur.fetchone()  # fetchone を使用して1つのレコードのみを取得
        
        conn.close()
        
        if record:
            if len(record) == 1:  # 結果が1つのフィールドのみの場合
                return record[0]  # 最初のフィールドの値を返す
            else:
                return record
        else:
            return None  # 結果がない場合は None を返す
    
    def count_data(self, table_name):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        sql_select = f'SELECT COUNT(*) FROM {table_name};'
        cur.execute(sql_select)

        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return 0
    
    def get_columns(self, table_name):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(f"PRAGMA table_info({table_name});")
        columns = [tup[1] for tup in c.fetchall()]
        conn.close()
        return columns