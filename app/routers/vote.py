from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2, database

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
        vote: schemas.Vote,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    # sql = """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"""
    # cursor.execute(sql, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    query = db.query(models.Posts).filter(models.Posts.id == vote.post_id)
    result = query.first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist")

    query = db.query(models.Votes).filter(models.Votes.post_id ==
                                          vote.post_id, models.Votes.user_id == current_user.id)
    result = query.first()
    if (vote.dir):
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        data = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(data)
        db.commit()
        return {"message": "Success - Vote added"}
    else:
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist")
        query.delete()
        db.commit()
        return {"message": "Success - Vote deleted"}
