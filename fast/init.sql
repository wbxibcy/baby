CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    nickname TEXT,
    gender TEXT,
    account TEXT,
    phone TEXT,
    password TEXT,
    avatar BLOB
);

CREATE TABLE IF NOT EXISTS dishs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    image BLOB,
    favourite BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    dish_id INTEGER REFERENCES dishs(id),
    ingredient_id INTEGER REFERENCES ingredients(id),
    quantity REAL,
    unit TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(dish_id) REFERENCES dishs(id),
    FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
);


-- 插入用户数据
INSERT INTO users (name, nickname, gender, account, phone, password, avatar)
VALUES ('张三', '三儿', '男', 'zhangsan', '13888888888', '123456', NULL),
       ('李四', '四哥', '男', 'lisi', '13999999999', 'abcdef', NULL),
       ('王五', '五弟', '男', 'wangwu', '13666666666', '888888', NULL);

-- 插入菜品数据
INSERT INTO dishs (name, image, favourite)
VALUES ('宫保鸡丁', NULL, 0),
       ('鱼香肉丝', NULL, 1),
       ('糖醋排骨', NULL, 0);

-- 插入食材数据
INSERT INTO ingredients (name)
VALUES ('鸡肉'),
       ('辣椒'),
       ('鱼肉'),
       ('猪肉'),
       ('排骨'),
       ('醋'),
       ('糖');

-- 插入日志数据
INSERT INTO logs (user_id, dish_id, ingredient_id, quantity, unit)
VALUES (1, 1, 1, 200, '克'),
       (2, 2, 3, 300, '克'),
       (3, 3, 5, 400, '克');
