import sqlite3
import os

# 设置数据库文件路径
db_file = 'dish.db'

# 清空数据库文件中的所有数据
if os.path.exists(db_file):
    os.remove(db_file)

# 读取SQL文件
with open('init.sql', 'r') as sql_file:
    sql_script = sql_file.read()

# 连接到数据库
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 执行SQL语句
cursor.executescript(sql_script)

# 提交更改并关闭连接
conn.commit()
conn.close()

print("Init Done!!!")