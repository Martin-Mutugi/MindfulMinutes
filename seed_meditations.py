# seed_meditations.py
from backend.app import create_app
from backend.extensions import db
from backend.models import MeditationSession
from datetime import datetime

app = create_app()

def seed_for_user(user_id):
    meditations = [
        MeditationSession(
            title="Calm Breathing",
            description="Slow your breath and settle your thoughts.",
            audio_url="https://example.com/audio/calm.mp3",
            duration=300,
            mood_tag="anxious",
            completed_at=datetime.utcnow(),
            user_id=user_id
        ),
        MeditationSession(
            title="Gratitude Reset",
            description="Shift your focus to what’s good.",
            audio_url="https://example.com/audio/gratitude.mp3",
            duration=420,
            mood_tag="sad",
            completed_at=datetime.utcnow(),
            user_id=user_id
        ),
        MeditationSession(
            title="Joy Activation",
            description="Lean into your light.",
            audio_url="https://example.com/audio/joy.mp3",
            duration=360,
            mood_tag="happy",
            completed_at=datetime.utcnow(),
            user_id=user_id
        ),
        MeditationSession(
            title="Stillness Practice",
            description="Embrace the quiet.",
            audio_url="https://example.com/audio/stillness.mp3",
            duration=480,
            mood_tag="calm",
            completed_at=datetime.utcnow(),
            user_id=user_id
        ),
    ]
    db.session.bulk_save_objects(meditations)
    db.session.commit()
    print("Meditations seeded successfully.")

# ✅ Wrap in app context
with app.app_context():
    seed_for_user(user_id=1)
