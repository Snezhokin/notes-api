# endpoints for notes

from fastapi import APIRouter , Depends , HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import database, models , schemas , auth

router = APIRouter(prefix="/notes" , tags = ["notes"])

@router.get("/", response_model=List[schemas.NoteOut])
def get_notes(
    db:Session = Depends(database.get_db),
    current_user:models.User=Depends(auth.get_current_user)
):
    notes = db.query(models.Note).filter(models.Note.user_id == current_user.id).all()
    return notes

@router.post("/" , response_model = schemas.NoteOut)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_note = models.Note(
        title = note.title,
        content = note.content,
        user_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(
    note_id: int ,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.id == current_user.user
    ).first()
    if not note:
        raise HTTPException(status_code = 404 , detail = "Note not found")
    return note

@router.put("/{note_id}" , response_model = schemas.NoteOut)
def update_note(
    note_id : int,
    note_update: schemas.NoteUpdate,
    db:  Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    note = db.query(models.Note).filter(
        models.Note.id== note_id,
        models.Note.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code = 404 , detail = "Note not found")
    
    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content

    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db:Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    note=db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException( status_code = 404 , detail = "Note not found")
    
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}