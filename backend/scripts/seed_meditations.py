from backend.extensions import db
from backend.models import Meditation

def seed_meditations():
    meditations = [
        # 🎵 Free Meditations
        Meditation(
            title="Morning Clarity",
            mood_tag="focused",
            is_premium=False,
            image_url="/static/images/morning.jpg",
            audio_url="/static/audio/morning_clarity.mp3",
            description="Start your day with clarity and calm."
        ),
        Meditation(
            title="Gratitude Flow",
            mood_tag="grateful",
            is_premium=False,
            image_url="/static/images/gratitude.jpg",
            audio_url="/static/audio/gratitude_flow.mp3",
            description="Reflect on what you're thankful for."
        ),
        Meditation(
            title="Breathe Through It",
            mood_tag="anxious",
            is_premium=False,
            image_url="/static/images/breathe.jpg",
            audio_url="/static/audio/breathe_through_it.mp3",
            description="A short breathing session to ease tension."
        ),
        Meditation(
            title="Evening Reset",
            mood_tag="neutral",
            is_premium=False,
            image_url="/static/images/evening.jpg",
            audio_url="/static/audio/evening_reset.mp3",
            description="Wind down and reset your mind."
        ),

        # 🔒 Premium Meditations
        Meditation(
            title="Inner Strength",
            mood_tag="hopeful",
            is_premium=True,
            image_url="/static/images/strength.jpg",
            audio_url="/static/audio/inner_strength.mp3",
            description="Tap into your resilience and power."
        ),
        Meditation(
            title="Let It Go",
            mood_tag="sad",
            is_premium=True,
            image_url="/static/images/letgo.jpg",
            audio_url="/static/audio/let_it_go.mp3",
            description="Release emotional weight and find peace."
        ),
        Meditation(
            title="Joyful Energy",
            mood_tag="positive",
            is_premium=True,
            image_url="/static/images/joy.jpg",
            audio_url="/static/audio/joyful_energy.mp3",
            description="Boost your mood with uplifting vibes."
        ),
        Meditation(
            title="Grounding Roots",
            mood_tag="anxious",
            is_premium=True,
            image_url="/static/images/grounding.jpg",
            audio_url="/static/audio/grounding_roots.mp3",
            description="Feel anchored and safe in the present moment."
        ),
        Meditation(
            title="Vision Forward",
            mood_tag="focused",
            is_premium=True,
            image_url="/static/images/vision.jpg",
            audio_url="/static/audio/vision_forward.mp3",
            description="Visualize your goals with clarity."
        ),
        Meditation(
            title="Compassion Pulse",
            mood_tag="grateful",
            is_premium=True,
            image_url="/static/images/compassion.jpg",
            audio_url="/static/audio/compassion_pulse.mp3",
            description="Cultivate kindness toward yourself and others."
        ),
        Meditation(
            title="Emotional Release",
            mood_tag="sad",
            is_premium=True,
            image_url="/static/images/release.jpg",
            audio_url="/static/audio/emotional_release.mp3",
            description="Let go of lingering emotions with guided support."
        ),
        Meditation(
            title="Peaceful Horizon",
            mood_tag="neutral",
            is_premium=True,
            image_url="/static/images/horizon.jpg",
            audio_url="/static/audio/peaceful_horizon.mp3",
            description="Find stillness and space to breathe."
        ),
    ]

    db.session.bulk_save_objects(meditations)
    db.session.commit()
    print("✅ Seeded 12 meditations successfully.")
