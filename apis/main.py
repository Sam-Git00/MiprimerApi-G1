from fastapi import FastAPI

app = FastAPI()

#Ruta raiz
@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}

@app.get("/saludo/{nombre}")

def saludo(nombre: str):
    return {"message": f"Hola {nombre}"}
    