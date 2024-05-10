from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Dish, Log, Ingredient
from schemas import LoginRequest, MeRequest, DishResponse, IngredientRequest
from models import Base
from typing import List
from Levenshtein import distance as levenshtein_distance
from fastapi import HTTPException, status
import uvicorn
import base64
from fastapi import Form, File, UploadFile

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return "Hello World"


@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录，接收 LoginRequest 模型的请求体，验证用户账号密码是否正确
    """
    user = db.query(User).filter(User.account == request.account, User.password == request.password).first()
    if user:
        return {"user_id": user.id}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/me", response_model=MeRequest)
def get_me(uid: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    """
    获取用户信息，根据用户 ID 查询用户信息并返回 MeRequest 模型
    """
    user = db.query(User).filter(User.id == uid).first()
    if user:
        return MeRequest(
            user_id=user.id,
            name=user.name,
            nickname=user.nickname,
            gender=user.gender,
            account=user.account,
            phone=user.phone,
            avatar=user.avatar
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/dishes", response_model=List[DishResponse])
def get_dishes_by_user(uid: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    """
    获取用户的菜品列表，根据用户 ID 查询用户的菜品并返回 DishResponse 模型列表
    """
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    logs = db.query(Log).filter(Log.user_id == uid).all()
    dish_ids = [log.dish_id for log in logs]
    dishes = db.query(Dish).filter(Dish.id.in_(dish_ids)).all()
    
    return [DishResponse(id=dish.id, name=dish.name, image=dish.image) for dish in dishes]


@app.get("/dishes/favourite", response_model=List[DishResponse])
def get_favourite_dishes_by_user(uid: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    """
    获取用户收藏的菜品列表，根据用户 ID 查询用户收藏的菜品并返回 DishResponse 模型列表
    """
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    favourite_dishes = db.query(Dish).join(Log, Log.dish_id == Dish.id).filter(Log.user_id == uid, Dish.favourite == True).all()
    return [DishResponse(id=dish.id, name=dish.name, image=dish.image) for dish in favourite_dishes]


@app.post("/dishes/add", response_model=None, status_code=status.HTTP_201_CREATED)
def add_dish(name: str = Form(...), image: UploadFile = File(...), favourite: bool = Form(...), uid: int = Form(...), db: Session = Depends(get_db)):
    """
    添加菜品，接收菜品名字、图像文件、是否收藏、用户 ID, 将菜品信息保存到数据库
    """
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    image_data = base64.b64encode(image.file.read())
    
    new_dish = Dish(name=name, image=image_data, favourite=favourite)
    db.add(new_dish)
    db.commit()

    new_log = Log(user_id=user.id, dish_id=new_dish.id)
    db.add(new_log)
    db.commit()

    return status.HTTP_201_CREATED


@app.delete("/dishes/delete", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(did: int = Query(..., description="Dish ID"), db: Session = Depends(get_db)):
    """
    删除菜品，根据菜品 ID 删除数据库中的菜品信息
    """
    dish = db.query(Dish).filter(Dish.id == did).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    db.delete(dish)
    db.commit()

    return status.HTTP_204_NO_CONTENT

def get_dish_id_by_user_id_and_name(user_id: int, dish_name: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    log_entry = db.query(Log).join(Dish).filter(User.id == user_id, Dish.name == dish_name).first()
    if not log_entry:
        raise HTTPException(status_code=404, detail="Dish not found")

    return log_entry.dish_id


@app.get("/dishes/select")
def get_dish_id(uid: int = Query(..., description="User ID"), dishname: str = Query(..., description="Dish Name"), db: Session = Depends(get_db)):
    """
    根据用户 ID 和菜品名称获取菜品 ID
    """
    dish_id = get_dish_id_by_user_id_and_name(uid, dishname, db)
    return {"dish_id": dish_id}


def get_similar_dishes(user_id: int, search_query: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    logs = db.query(Log).filter(Log.user_id == user_id).all()
    dish_ids = [log.dish_id for log in logs]

    dishes = db.query(Dish).filter(Dish.id.in_(dish_ids)).all()

    threshold = 3
    similar_dishes = []
    for dish in dishes:
        distance = levenshtein_distance(search_query, dish.name)
        if distance <= threshold:
            similar_dishes.append(dish)

    return similar_dishes


@app.get("/dishes/search")
def search_dishes(uid: int = Query(..., description="User ID"), query: str = Query(..., description="Search Query"), db: Session = Depends(get_db)):
    """
    根据用户 ID 和搜索内容获取相似的菜品列表
    """
    similar_dishes = get_similar_dishes(uid, query, db)
    return [DishResponse(id=dish.id, name=dish.name, image=dish.image) for dish in similar_dishes]


@app.put("/dishes/update", status_code=status.HTTP_200_OK)
def update_dish(did: int = Form(...), name: str = Form(...), image: UploadFile = File(None), db: Session = Depends(get_db)):
    """
    根据菜品 ID 更新菜品名字和图片
    """
    dish = db.query(Dish).filter(Dish.id == did).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    dish.name = name

    if image:
        image_data = base64.b64encode(image.file.read())
        dish.image = image_data

    db.commit()

    return {"message": "Update successful"}


@app.post("/ingredients/add", status_code=status.HTTP_201_CREATED)
def add_ingredient(request: IngredientRequest, db: Session = Depends(get_db)):
    """
    根据用户 ID 和菜品 ID 添加食材
    """
    user = db.query(User).filter(User.id == request.uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dish = db.query(Dish).filter(Dish.id == request.did).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    for ingredient_data in request.ingredients:

        ingredient = db.query(Ingredient).filter(Ingredient.name == ingredient_data.name).first()
        if not ingredient:
            ingredient = Ingredient(name=ingredient_data.name)
            db.add(ingredient)
            db.commit()


        new_log = Log(user_id=request.uid, dish_id=request.did, ingredient_id=ingredient.id, quantity=ingredient_data.quantity, unit=ingredient_data.unit)
        db.add(new_log)
        db.commit()

    return status.HTTP_201_CREATED


@app.get("/ingredients/select", response_model=None)
def get_ingredients(uid: int = Query(..., description="User ID"), did: int = Query(..., description="Dish ID"), db: Session = Depends(get_db)):
    """
    根据用户 ID 和菜品 ID 查找食材
    """
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dish = db.query(Dish).filter(Dish.id == did).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    logs = db.query(Log).filter(Log.user_id == uid, Log.dish_id == did).all()
    ingredients = []
    for log in logs:
        ingredient = db.query(Ingredient).filter(Ingredient.id == log.ingredient_id).first()
        if ingredient:
            ingredient_data = {
                "name": ingredient.name,
                "quantity": log.quantity,
                "unit": log.unit
            }
            ingredients.append(ingredient_data)

    return ingredients


@app.delete("/ingredients/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredients(uid: int = Query(..., description="User ID"), did: int = Query(..., description="Dish ID"), db: Session = Depends(get_db)):
    """
    根据用户 ID 和菜品 ID 删除食材
    """
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dish = db.query(Dish).filter(Dish.id == did).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    log = db.query(Log).filter(Log.user_id == uid, Log.dish_id == did).first()
    if not log:
        raise HTTPException(status_code=404, detail="Ingredients not found")

    db.delete(log)
    db.commit()

    return None

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)