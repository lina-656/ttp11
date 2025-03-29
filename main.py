from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import datetime
import random
app = FastAPI()

# Секретный ключ для JWT. Его следует хранить в защищенном месте.
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена в минутах
def authenticate_user(username: str, password: str) -> bool:
    # В реальном приложении вы будете проверять чувства пользователя в БД
    return random.choice([True, False])
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Генерация JWT токена
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": username,
        "exp": expiration
    }
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token}
@app.get("/protected_resource")
async def protected_resource(token: str):
    # Проверка токена
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    return {"message": "Access granted", "user": username}
