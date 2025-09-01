from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from backend.services.suggestions import get_suggestions

bp = Blueprint('suggestions', __name__, url_prefix='/api/suggestions')

@bp.route('/', methods=['GET'])
@login_required
def fetch_suggestions():
    data = get_suggestions(current_user)

    # Serialize meditation objects
    meditations = [
        {
            "id": m.id,
            "title": m.title,
            "mood_tag": m.mood_tag,
            "is_premium": m.is_premium,
            "image_url": m.image_url,
            "audio_url": m.audio_url,
            "description": m.description
        }
        for m in data["meditations"]
    ]

    return jsonify({
        "prompt": data["prompt"],
        "meditations": meditations
    })
