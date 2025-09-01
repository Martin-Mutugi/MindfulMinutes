from flask import Blueprint, render_template

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@feedback_bp.route('/')
def index():
    return render_template('support/feedback.html')
