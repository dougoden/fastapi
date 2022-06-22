from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='ado99rdo',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("SUCCESS: Connect to PostgreSQL")
        break
    except Exception as error:
        print("FAILED: Connect to PostgreSQL\n", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello API"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    sql = """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"""
    cursor.execute(sql, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    if not new_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid id: [{id}]")
    conn.commit()
    return {
        "status": "Success",
        "data": new_post
    }


@app.get("/posts")
def get_posts():
    sql = """SELECT * FROM posts"""
    cursor.execute(sql)
    posts = cursor.fetchall()
    return {
        "status": "Success",
        "data": posts
    }


@app.get("/posts/{id}")
def get_post(id: int):
    sql = """SELECT * FROM posts WHERE id = %s"""
    cursor.execute(sql, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid id: [{id}]")
    return {
        "status": "Success",
        "data": post
    }


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    sql = """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"""
    cursor.execute(sql, (post.title, post.content, post.published, str(id)))
    upd_post = cursor.fetchone()
    if not upd_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid id: [{id}]")
    conn.commit()
    return {
        "status": "Success",
        "data": upd_post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    sql = """DELETE FROM posts WHERE id = %s RETURNING *"""
    cursor.execute(sql, (str(id)))
    del_post = cursor.fetchone()
    if not del_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid id: [{id}]")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
