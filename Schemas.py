from typing import List
from pydantic import BaseModel


class PhysicalBook(BaseModel):
    titulo:     str
    volume:     int
    valor:      float


class PhysicalBooksResponse(BaseModel):
    allBooks:   List[dict] = []


class VirtualBook(BaseModel):
    titulo:     str
    status:     str
    capsLidos:  int


class VirtualBooksResponse(BaseModel):
    allBooks:   List[dict] = []