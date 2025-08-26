from typing import Optional, Tuple, List

from werkzeug.exceptions import BadRequest, NotFound, Forbidden

from .models import db, User, Note


class UserService:
    """Service layer for user-related operations."""

    @staticmethod
    def register(email: str, password: str) -> User:
        existing = User.query.filter_by(email=email).first()
        if existing:
            raise BadRequest("Email already registered")
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(email: str, password: str) -> User:
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise BadRequest("Invalid email or password")
        return user


class NoteService:
    """Service layer for note CRUD with authorization checks."""

    @staticmethod
    def create_note(user_id: int, title: str, content: Optional[str]) -> Note:
        note = Note(user_id=user_id, title=title, content=content or "")
        db.session.add(note)
        db.session.commit()
        return note

    @staticmethod
    def get_note(user_id: int, note_id: int) -> Note:
        note = Note.query.get(note_id)
        if not note:
            raise NotFound("Note not found")
        if note.user_id != user_id:
            raise Forbidden("You do not have access to this note")
        return note

    @staticmethod
    def update_note(user_id: int, note_id: int, title: Optional[str], content: Optional[str]) -> Note:
        note = NoteService.get_note(user_id, note_id)
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        db.session.commit()
        return note

    @staticmethod
    def delete_note(user_id: int, note_id: int) -> None:
        note = NoteService.get_note(user_id, note_id)
        db.session.delete(note)
        db.session.commit()

    @staticmethod
    def list_notes(user_id: int, page: int, per_page: int) -> Tuple[List[Note], int, int]:
        query = Note.query.filter_by(user_id=user_id).order_by(Note.updated_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages or 0
