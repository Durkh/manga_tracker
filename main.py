from typing import Optional

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
        raise HTTPException(status_code=404, detail="No entries found")
    else:
        for row in rows:
            valor: str = row[2]
            book = Schemas.PhysicalBook(titulo=row[0], volume=row[1],
                                        valor=float(valor.lstrip("R$ ").replace(",", ".")))
            result.append(book.dict())

    response.allBooks = result
    return response


@app.get("/manga/fisico/{item_name}", response_model=Schemas.PhysicalBooksResponse)
async def get_single_physical(item_name: str, volume: Optional[int] = None):
    response: Schemas.PhysicalBooksResponse = Schemas.PhysicalBooksResponse()
    result = []

    if volume is None:
        query = """SELECT titulo, volume, valor FROM fisicos WHERE titulo = %s"""
        cursor.execute(query, (item_name,))
    else:
        query = """SELECT titulo, volume, valor FROM fisicos WHERE titulo = %s AND volume = %s"""
        cursor.execute(query, (item_name, volume))

    rows = cursor.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="No entries found")
    else:
        for row in rows:
            valor: str = row[2]
            book = Schemas.PhysicalBook(titulo=row[0], volume=row[1],
                                        valor=float(valor.lstrip("R$ ").replace(",", ".")))
            result.append(book.dict())

    response.allBooks = result
    return response


@app.post("/manga/fisico")
async def add_physical_copy(book: Schemas.PhysicalBook):
    query = """INSERT INTO fisicos(titulo, volume, valor) VALUES(%s, %s, %s)"""

    try:
        cursor.execute(query, (book.titulo, book.volume, book.valor))
        conn.commit()
    except (Exception, DatabaseError) as errorDB:
        print("Database Put error: " + errorDB)
    finally:
        return


@app.put("/manga/fisico/{item_name}")
async def update_physical_book(item_name: str, volume: int, valor: float):
    query = """SELECT titulo, volume, valor FROM fisicos WHERE titulo = %s AND volume = %s AND valor = %s"""
    cursor.execute(query, (item_name, volume, valor))

    rows = cursor.fetcone()
    if rows is None:
        book = Schemas.PhysicalBook(titulo=item_name, volume=volume, valor=valor)
        await add_physical_copy(book)
    else:
        query = """UPDATE fisicos SET volume = %s, valor = %s WHERE titulo = %s"""
        cursor.execute(query, (volume, valor, item_name))
        conn.commit()

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
async def all_virtual_copies(status: str = "a"):

    status.casefold()
    if status is not "d" or status is not "o" or status is not "r" or status is not "p":
        # Dropped, On Hold, Reading, Plan to (read)
        raise HTTPException(status_code=400, detail="Invalid status")

    response: Schemas.VirtualBooksResponse = Schemas.VirtualBooksResponse()
    result = []

    if status == "a":
        query = """SELECT * FROM virtuais"""
        cursor.execute(query)
    else:
        query = """SELECT * FROM virtuais WHERE status = %s"""
        cursor.execute(query, (status,))

    rows = cursor.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="No entries found")
    else:
        for row in rows:
            book = Schemas.VirtualBook(titulo=row[0], status=row[1], capsLidos=row[2])
            result.append(book.dict())

    response.allBooks = result
    return response


@app.get("/manga/virtual/{item_name}")
async def get_single_virtual(item_name: str):
    query = """SELECT titulo, status, caps_lidos FROM virtuais WHERE titulo = %s"""
    cursor.execute(query, (item_name,))

    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="Title not found")

    return result


@app.post("/manga/virtual")
async def add_virtual_copy(book: Schemas.VirtualBook):
    query = """INSERT INTO virtuais(titulo, status, caps_lidos) VALUES(%s, %s, %s)"""

    book.status = book.status.casefold()
    if book.status != "d" and book.status != "o" and book.status != "r" and book.status != "p":
        # Dropped, On Hold, Reading, Plan to (read)
        raise HTTPException(status_code=400, detail="Invalid status")

    try:
        cursor.execute(query, (book.titulo, book.status, book.capsLidos))
        conn.commit()
    except (Exception, DatabaseError) as errorDB:
        print("Database Put error: " + errorDB)
    finally:
        return


@app.put("/manga/virtual/{item_name}")
async def update_virtual_book(item_name: str, status: str, caps_lidos: int):
    query = """SELECT titulo, status, caps_lidos FROM virtuais WHERE titulo = %s"""
    cursor.execute(query, (item_name,))

    rows = cursor.fetchone()
    if rows is None:
        book = Schemas.VirtualBook(titulo=item_name, status=status, capsLidos=caps_lidos)
        await add_virtual_copy(book)
    else:
        query = """UPDATE virtuais SET status = %s, caps_lidos = %s WHERE titulo = %s"""
        cursor.execute(query, (status.casefold(), caps_lidos, item_name))
        conn.commit()

    return


@app.delete("/manga/virtual/{item_name}")
async def delete_virtual(item_name: str):
    query = """DELETE FROM virtuais WHERE titulo = %s"""
    try:
        cursor.execute(query, (item_name,))
        conn.commit()
    except (Exception, DatabaseError) as errorDB:
        print("Database Delete error: " + errorDB)
    finally:
        return
