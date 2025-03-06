from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from sqlalchemy import create_engine, Column, Integer, String
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

app = FastAPI()

# 🔹 Configuração para permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Isso permite acesso de qualquer origem (para testes)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do banco de dados PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/nasa_db")
print(f"Conectando ao banco de dados: {DATABASE_URL}")
time.sleep(10)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo de tabela para favoritos
class FavoriteImage(Base):
    __tablename__ = "favorite_images"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, index=True)

Base.metadata.create_all(bind=engine)

NASA_API_URL = "https://api.nasa.gov/planetary/apod"
# NASA_API_KEY = "DEMO_KEY"  # Substituir pela sua API Key
NASA_API_KEY = os.getenv("NASA_API_KEY")

@app.get("/image")
def get_nasa_image():
    response = requests.get(f"{NASA_API_URL}?api_key={NASA_API_KEY}")
    return response.json()

@app.post("/favorite")
def add_favorite(title: str, url: str):
    db = SessionLocal()
    favorite = FavoriteImage(title=title, url=url)
    db.add(favorite)
    db.commit()
    db.close()
    return {"message": "Imagem favoritada com sucesso"}

@app.get("/favorites")
def get_favorites():
    db = SessionLocal()
    favorites = db.query(FavoriteImage).all()
    db.close()
    return favorites

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
