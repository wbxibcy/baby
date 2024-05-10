import sqlite3

# 设置数据库文件路径
db_file = 'dish.db'

# 连接到数据库
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 查询数据
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

cursor.execute("SELECT * FROM dishs")
dishes = cursor.fetchall()

cursor.execute("SELECT * FROM ingredients")
ingredients = cursor.fetchall()

cursor.execute("SELECT * FROM logs")
logs = cursor.fetchall()

# 打印数据
print("Users:")
for user in users:
    print(user)

print("\nDishes:")
for dish in dishes:
    print(dish)

print("\nIngredients:")
for ingredient in ingredients:
    print(ingredient)

print("\nLogs:")
for log in logs:
    print(log)

# 关闭连接
conn.close()
