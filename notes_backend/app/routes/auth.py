from flask_smorest import Blueprint
from flask.views import MethodView

from ..auth import create_access_token
from ..schemas import UserRegisterSchema, UserLoginSchema, TokenSchema, UserSchema, MessageSchema
from ..services import UserService

blp = Blueprint(
    "Auth",
    "auth",
    url_prefix="/auth",
    description="Authentication endpoints for user registration and login",
)


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserSchema)
    @blp.alt_response(400, schema=MessageSchema, description="Invalid input or email already registered")
    def post(self, json_data):
        """Register a new user."""
        user = UserService.register(email=json_data["email"], password=json_data["password"])
        return user.to_dict()


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserLoginSchema)
    @blp.response(200, TokenSchema)
    @blp.alt_response(400, schema=MessageSchema, description="Invalid credentials")
    def post(self, json_data):
        """Authenticate user and return JWT token."""
        user = UserService.authenticate(email=json_data["email"], password=json_data["password"])
        token = create_access_token({"id": user.id, "email": user.email})
        return {"access_token": token}
