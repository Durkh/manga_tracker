import DB
import Schemas

from fastapi import FastAPI, HTTPException
from psycopg2 import DatabaseError


conn, cursor = DB.connect_db()
app = FastAPI()


@app.get("/")
async def hello():
    return {"Hello": "World"}

# physical mangas section


@app.get("/manga/fisico", response_model=Schemas.PhysicalBooksResponse)
async def all_physical_copies():

    response: Schemas.PhysicalBooksResponse = Schemas.PhysicalBooksResponse()
    result = []

    query = """SELECT * FROM fisicos"""
    cursor.execute(query)

    rows = cursor.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="No entries")
    else:
        for row in rows:
            valor: str = row[2]
            book = Schemas.PhysicalBook(titulo=row[0], volume=row[1], valor=float(valor.lstrip("R$ ").replace(",", ".")))
            result.append(book.dict())

    response.allBooks = result
    return response


@app.get("/manga/fisico/{item_name}")
async def get_single_physical(item_name: str):
    query = """SELECT titulo, volume, valor FROM fisicos WHERE titulo = %s"""
    cursor.execute(query, (item_name,))

    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="Title not found")

    return result


@app.put("/manga/fisico")
async def add_physical_copy(book: Schemas.PhysicalBook):
    query = """INSERT INTO fisicos(titulo, volume, valor) VALUES(%s, %s, %s)"""

    try:
        cursor.execute(query, (book.titulo, book.volume, book.valor))
        conn.commit()
    except (Exception, DatabaseError) as errorDB:
        print("Database Put error: " + errorDB)
    finally:
        return


@app.delete("/manga/fisico/{item_name}")
async def delete_physical(item_name: str):
    query = """DELETE FROM fisicos WHERE titulo = %s"""
    try:
        cursor.execute(query, (item_name,))
        conn.commit()
    except (Exception, DatabaseError) as errorDB:
        print("Database Delete error: " + errorDB)
    finally:
        return


# virtual mangas section


@app.get("/manga/virtual", response_model=Schemas.PhysicalBooksResponse)
async def all_physical_copies():

    response: Schemas.VirtualBooksResponse = Schemas.VirtualBooksResponse()
    result = []

    query = """SELECT * FROM virtuais"""
    cursor.execute(query)

    rows = cursor.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="No entries")
    else:
        for row in rows:
            book = Schemas.VirtualBook(titulo=row[0], status=row[1], capsLidos=row[2])
            result.append(book.dict())

    response.allBooks = result
    return response


@app.get("/manga/virtual/{item_name}")
async def get_single_physical(item_name: str):
    query = """SELECT titulo, status, caps_lidos FROM virtuais WHERE titulo = %s"""
    cursor.execute(query, (item_name,))

    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="Title not found")

    return result


@app.put("/manga/virtual")
async def add_physical_copy(book: Schemas.VirtualBook):
    query = """INSERT INTO virtuais(titulo, status, caps_lidos) VALUES(%s, %s, %s)"""

    try:
        cursor.execute(query, (book.titulo, book.status, book.capsLidos))
        conn.commit()
    except (Exception, DatabaseError) as errorDB:
        print("Database Put error: " + errorDB)
    finally:
        return


@app.delete("/manga/virtual/{item_name}")
async def delete_physical(item_name: str):
    query = """DELETE FROM virtuais WHERE titulo = %s"""
    try:
        cursor.execute(query, (item_name,))
        conn.commit()
    except (Exception, DatabaseError) as errorDB:
        print("Database Delete error: " + errorDB)
    finally:
        return
