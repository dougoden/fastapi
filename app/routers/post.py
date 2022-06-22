from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List, Optional

from .. import models, schemas, oauth2, database

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get("/", response_model=List[schemas.PostOut])
@router.get("/")
def get_posts(
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = ""):
    # sql = """SELECT * FROM posts"""
    # cursor.execute(sql)
    # posts = cursor.fetchall()

    stmt = (
        select(models.Posts, func.count(models.Votes.post_id).label("likes"))
        .outerjoin(models.Votes, models.Posts.id == models.Votes.post_id)
        .filter(models.Posts.title.contains(search))
        .group_by(models.Posts.id)
        .order_by(models.Posts.id)
        .offset(skip)
        .limit(limit)
    )
    query = db.execute(stmt)
    result = query.all()
    # query = db.query(models.Posts)
    # print(query)
    # result = query.all()
    # result = query.filter(models.Posts.title.contains(
    #     search)).limit(limit).offset(skip).all()

    # query = db.query(
    #     models.Posts, func.count(models.Votes.post_id).label("likes")).join(
    #         models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).group_by(
    #             models.Posts.id).order_by(models.Posts.id)
    # result = query.all()
    return result


# @router.get("/{id}", response_model=schemas.PostOut)
@router.get("/{id}")
def get_post(
        id: int,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    # sql = """SELECT * FROM posts WHERE id = %s"""
    # cursor.execute(sql, (str(id)))
    # post = cursor.fetchone()
    # query = db.query(models.Posts).filter(models.Posts.id == id)
    # result = query.first()

    stmt = (
        select(models.Posts, func.count(models.Votes.post_id).label("likes"))
        .outerjoin(models.Votes, models.Posts.id == models.Votes.post_id)
        .filter(models.Posts.id == id)
        .group_by(models.Posts.id)
    )
    query = db.execute(stmt)
    result = query.first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Post Id: [ {id} ]")
    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
        post: schemas.PostCreate,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    # sql = """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"""
    # cursor.execute(sql, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    data = models.Posts(owner_id=current_user.id, **post.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@router.put("/{id}", response_model=schemas.Post)
def update_post(
        id: int,
        post: schemas.PostCreate,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    # sql = """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"""
    # cursor.execute(sql, (post.title, post.content, post.published, str(id)))
    # upd_post = cursor.fetchone()
    query = db.query(models.Posts).filter(models.Posts.id == id)
    result = query.first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid id: [{id}]")
    if result.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action")
    query.update(post.dict())
    db.commit()
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        id: int,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    # sql = """DELETE FROM posts WHERE id = %s RETURNING *"""
    # cursor.execute(sql, (str(id)))
    # del_post = cursor.fetchone()
    query = db.query(models.Posts).filter(models.Posts.id == id)
    result = query.first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Post Id: [ {id} ]")
    if result.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action")
    query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
