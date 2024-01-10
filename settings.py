db_path = "/Users/takemoto.t/1st_q4/DSP/DSP_FT.db"

climate_table_schema = {
    "table_name":"climate_table",
    "columns" : [
        {"name":"id","type":"INTEGER PRIMARY KEY AUTOINCREMENT"},
        {"name":"date","type":"TEXT"},
        {"name":"tenki","type":"TEXT"},
        {"name":"saikoukionn","type":"INTEGER"},
        {"name":"saiteikionn","type":"INTEGER"},
        {"name":"kousuiryou","type":"INTEGER"}
        ]
}

screen_time_table_schema = {
    "table_name":"screen_time_table",
    "columns" : [
        {"name":"id","type":"INTEGER PRIMARY KEY AUTOINCREMENT"},
        {"name":"date","type":"TEXT"},
        {"name":"SNS","type":"INTEGER"},
        {"name":"Entame","type":"INTEGER"},
        {"name":"Zyouhou","type":"INTEGER"},
        {"name":"Sonohoka","type":"INTEGER"},
        {"name":"Creatibity","type":"INTEGER"},
        {"name":"Sigoto","type":"INTEGER"},
        {"name":"Shopping","type":"INTEGER"},
        {"name":"Util","type":"INTEGER"},
        {"name":"Game","type":"INTEGER"}
        ]
}