from flask import Blueprint, render_template
from flask_login import login_required

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def index():
    return render_template('main/profile.html')
