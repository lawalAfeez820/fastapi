from fastapi import APIRouter, Depends, status,HTTPException
from .. import models, auth2, database
from sqlmodel import Session, select
import sqlalchemy
from typing import Dict

router = APIRouter(
    tags= ["Votes"],
    prefix = "/vote"
)

@router.post("/", response_model = Dict, status_code= status.HTTP_201_CREATED)
async def vote(post: models.Voters, current_user: models.Users =  Depends(auth2.get_current_user), 
db: Session = Depends(database.get_session)):
    vote: models.Vote = models.Vote(post_id = post.post_id, user_id = current_user.id)
    if post.vote_dir == 1:
        try:
            check = await db.exec(select(models.Posts).where(models.Posts.id ==post.post_id))
            if not check.first():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                detail= f"Trying to vote on a post that does not exist")
            db.add(vote)
            await db.commit()
            await db.refresh(vote)
            return {"detail": f"Vote successful"}
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                detail= f"Voting on a post you have already voted on")

    elif post.vote_dir == 0:
        check = await db.exec(select(models.Vote).where(models.Vote.post_id == post.post_id))
        check = await db.exec(select(models.Vote).where(models.Vote.user_id == current_user.id))
        check = check.first()
        if not check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail= f"Trying to remove vote that does not exist")
        
        await db.delete(check) 
        await db.commit()
        return {"detail": f"Vote removed"}

    

