from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# get list of private posts
@router.get("", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user),
            limit: int = 10,
            skip: int = 0,
            search: Optional[str] = ""):

    # query to retreiv all user posts
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.owner_id == current_user.id).filter(
                models.Post.title.contains(search)).order_by(
                models.Post.created_at.desc()).limit(limit).offset(skip).all()
    return posts

# get list of all posts
@router.get("/getallposts", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user),
            limit: int = 10,
            skip: int = 0,
            search: Optional[str] = ""):
    # query to retreive all posts
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).order_by(
                models.Post.created_at.desc()).limit(limit).offset(skip).all()

    return posts

#create a post
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #create a new post do the ** to make it more efficient and unpack all the fields in our Post model
    #new_post = models.Post(title=post.title, content=post.content, published=post.published) ===  new_post = models.Post(**post.model_dump())
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    # add to the db
    db.add(new_post)
    #commit changes
    db.commit()
    # return data of new created post an store it into new_post variable
    db.refresh(new_post)
    return new_post

#get specific post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # always convert & validate the str into an int
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

    post_auth_owner, _ = post
    if post_auth_owner.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to perform requested action")

    return post

#delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query to search for the post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # grab the post
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to perform requested action")

    # if post exist we chain the update method to the query post object passing the post we want to update
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # we send back to the user the post
    return post_query.first()
