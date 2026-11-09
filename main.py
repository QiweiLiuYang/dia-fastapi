from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Literal

app = FastAPI()
API_KEY = "CONTRASENA_SEGURA"

class Alumno(BaseModel):
    nombre: str
    curso: Literal["IA", "Datos", "ML"]


class Persona(BaseModel):
    edad: int
    horas_estudio: float

alumnos = [
        {"id": 1, "nombre": "Ana", "curso": "IA"},
        {"id": 2, "nombre": "Luis", "curso": "Datos"},
        {"id": 3, "nombre": "Carlos", "curso": "IA"}
]


def buscar(id: int):
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if alumno is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno


def verificar_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Acceso no autorizado")


@app.get("/")
def home():
    return {"mensaje": "Hola, API!"}


@app.get("/saludo/{nombre}")
def saludar(nombre: str, idioma: str = "es"):
    if idioma == "en":
        return {"mensaje": f"Hello, {nombre}!"}
    return {"mensaje": f"Hola, {nombre}!"}


@app.get("/cuadrado/{numero}")
def cuadrado(numero: int):
    return {
        "numero": numero,
        "resultado": numero ** 2
    }


@app.get("/alumnos")
def listar_alumnos(curso: str = None):
    if not curso:
        return {"alumnos": alumnos}

    return {"alumnos": [alumno for alumno in alumnos if alumno.get("curso").lower() == curso.lower()]}


@app.get("/alumnos/{id}")
def obtener_alumno(id: int):
    return buscar(id)


@app.post("/alumnos", status_code=201)
def crear(alumno: Alumno, x_api_key: str | None = Header(default=None)):
    verificar_api_key(x_api_key)
    nuevo_id = max([a["id"] for a in alumnos], default=0) + 1
    nuevo = {"id": nuevo_id, "nombre": alumno.nombre, "curso": alumno.curso}
    alumnos.append(nuevo)
    return nuevo


@app.put("/alumnos/{id}")
def actualizar(id: int, alumno: Alumno, x_api_key: str | None = Header(default=None)):
    verificar_api_key(x_api_key)
    a = buscar(id)
    a["nombre"] = alumno.nombre
    a["curso"] = alumno.curso
    return a


@app.delete("/alumnos/{id}")
def eliminar_alumno(id: int):
    alumnos.remove(buscar(id))

    return {"mensaje": "Alumno eliminado"}



@app.post("/predict")
def predecir(p: Persona):
    aprobado = p.horas_estudio >= 5
    return {
        "prediccion": "Aprobado" if aprobado else "Suspendido",
        "confianza": 0.87
    }