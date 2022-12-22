from . import db
from .models import Website, Data, User
from sqlalchemy import or_, and_
from app import app
from flask_login import login_required, current_user

def get_regular_websites():
    with app.app_context():
        return db.session.query(
            Website
        ).filter(
            and_(
                Website.user_id == current_user.user_id,
                Website.regularly is not None
            )
        ).all()
