# manga_tracker
program to track the mangas I own, am reading or have read

 ---
 
 This program awas created to test the [FastApi](https://fastapi.tiangolo.com/) and use [PostgreSQL](https://www.postgresql.org/) on Python
 
 although it's was created as a test project it was implemented for future use for an easy and customizable way of tracking the mangas I own physically or virtually

## frameworks used in this project

* [FastApi](https://fastapi.tiangolo.com/)
* [Pydantic](https://pydantic-docs.helpmanual.io/)
* [Psycopg2](https://pypi.org/project/psycopg2/)
* [Uvicorn](https://www.uvicorn.org/)

## Database

* [PostgreSQL](https://www.postgresql.org/)

---

## Backend features:
* Physical books:
  * store with title, volume and cost;
  * store, update and delete individual books;
  * list all volumes or individual volumes.
 
* Virtual books:
  * store with title, status and chapters read;
  * store, update and delete individual books;
  * list all volumes or individual volumes.
