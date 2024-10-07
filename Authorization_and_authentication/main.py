""" Learn to use OAuth2 and JWT for authorization and authentication
"""

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from typing import Annotated
from jose import jwt


app = FastAPI()

oaut2_schema = OAuth2PasswordBearer(tokenUrl="token")


users = {
    "pablo": {"username": "pablo", "email": "pablo@gmail.com", "password": "fakepass"},
    "user2": {"username": "user2", "email": "user2@gmail.com", "password": "user2"},
}

def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, "my-secret", algorithm="HS256")
    return token

def decode_token(token: Annotated[str, Depends(oaut2_schema)]) -> dict:
    data = jwt.decode(token, "my-secret", algorithms=["HS256"])
    user = users.get(data["username"])
    return user

@app.post('/token')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return {"access_token": token}

@app.get('/users/profile')
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user