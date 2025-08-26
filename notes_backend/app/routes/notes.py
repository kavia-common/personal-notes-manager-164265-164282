from flask_smorest import Blueprint
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from ..auth import get_current_user_id_from_request
from ..schemas import NoteCreateSchema, NoteUpdateSchema, NoteSchema, NotesListSchema, MessageSchema
from ..services import NoteService

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="CRUD endpoints for notes",
)


@blp.route("/")
class NotesCollection(MethodView):
    @blp.response(200, NotesListSchema)
    def get(self):
        """List notes for the current user with pagination. Query params: page, per_page"""
        user_id = get_current_user_id_from_request()
        from flask import request

        try:
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))
        except ValueError:
            raise BadRequest("Invalid pagination parameters")

        items, total, total_pages = NoteService.list_notes(user_id=user_id, page=page, per_page=per_page)
        return {
            "items": [n.to_dict() for n in items],
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
            },
        }

    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema)
    def post(self, json_data):
        """Create a note for the current user."""
        user_id = get_current_user_id_from_request()
        note = NoteService.create_note(user_id=user_id, title=json_data["title"], content=json_data.get("content"))
        return note.to_dict()


@blp.route("/<int:note_id>")
class NoteItem(MethodView):
    @blp.response(200, NoteSchema)
    def get(self, note_id: int):
        """Get a single note by id."""
        user_id = get_current_user_id_from_request()
        note = NoteService.get_note(user_id=user_id, note_id=note_id)
        return note.to_dict()

    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema)
    def put(self, json_data, note_id: int):
        """Update title and/or content of a note."""
        user_id = get_current_user_id_from_request()
        note = NoteService.update_note(
            user_id=user_id,
            note_id=note_id,
            title=json_data.get("title"),
            content=json_data.get("content"),
        )
        return note.to_dict()

    @blp.response(200, MessageSchema)
    def delete(self, note_id: int):
        """Delete a note by id."""
        user_id = get_current_user_id_from_request()
        NoteService.delete_note(user_id=user_id, note_id=note_id)
        return {"message": "Note deleted"}
