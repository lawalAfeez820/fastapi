from typing import List, Dict,Optional, Tuple, Union
from .. import database, models, auth2, schemas
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status, Response, APIRouter

router = APIRouter(
    prefix="/posts",
    tags= ["POSTS"]
)

# , response_model=Union[Dict , List[models.ResponseType]]
# response_model= List[models.ResponseType]
@router.get("/")
async def get_post(db: Session = Depends(database.get_session), limit:int = 2, skip:int = 0,
search: Optional[str]= "" ,current_user: models.Users =  Depends(auth2.get_current_user)): 

    query = await db.exec(select(models.Posts).where(models.Posts.title.contains(search)).limit(limit).offset(skip))
   
    
    query = query.all()
    if not query:
        raise HTTPException(status_code= 204)
    return query


@router.post("/", response_model=schemas.ResponseType, status_code= 201)
async def create_post(post: schemas.CreatePost, db: Session = Depends(database.get_session),
current_user: models.Users =  Depends(auth2.get_current_user)):

    full_data= models.Posts.from_orm(post)
    full_data.user_id = current_user.id
    full_data.creator_email = current_user.email

    db.add(full_data)
    await db.commit()
    await db.refresh(full_data)
    
    return full_data

# , response_model=models.ResponseType

@router.get("/getone/{id}")
async def get_post(id: int, db: Session = Depends(database.get_session),
current_user: models.Users =  Depends(auth2.get_current_user)):
    post = await db.get(models.Posts, id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist")
    return post
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(database.get_session),
current_user: models.Users =  Depends(auth2.get_current_user)):

    post = await db.get(models.Posts, id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
        detail= f"post with id {id} not found")
    if current_user.id != post.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail= f"You did not create this post")
    await db.delete(post)
    await db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.ResponseType)
async def update(new_post: schemas.UpdatePost, id: int, db: Session = Depends(database.get_session),
current_user: models.Users =  Depends(auth2.get_current_user)):
    post= await db.get(models.Posts, id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
        detail= f"post with id {id} not found")
    if current_user.id != post.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail= f"You did not create this post")
    post_tmp= new_post.dict(exclude_unset= True)
    for key,value in post_tmp.items():
        setattr(post,key,value)
    #full_post = models.Posts.from_orm(post)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post