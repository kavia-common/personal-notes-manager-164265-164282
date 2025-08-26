from marshmallow import Schema, fields, validate


class MessageSchema(Schema):
    message = fields.String(required=True, description="Human-friendly message")


class PaginationSchema(Schema):
    total = fields.Integer(required=True)
    page = fields.Integer(required=True)
    per_page = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)


class UserRegisterSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6), description="Password")


class UserLoginSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, load_only=True, description="Password")


class TokenSchema(Schema):
    access_token = fields.String(required=True, description="JWT access token")


class UserSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.Email(required=True)
    created_at = fields.String(required=True)


class NoteCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    content = fields.String(required=False, allow_none=True)


class NoteUpdateSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=255))
    content = fields.String(required=False, allow_none=True)


class NoteSchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    title = fields.String(required=True)
    content = fields.String(required=True, allow_none=True)
    created_at = fields.String(required=True)
    updated_at = fields.String(required=True)


class NotesListSchema(Schema):
    items = fields.List(fields.Nested(NoteSchema), required=True)
    pagination = fields.Nested(PaginationSchema, required=True)
