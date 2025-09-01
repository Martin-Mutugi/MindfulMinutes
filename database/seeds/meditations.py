from backend.models import Meditation
from backend.extensions import db

def seed_meditations():
    """Seed database with sample meditations"""
    meditations = [
        # Beginner meditations
        {
            'title': 'Breathing Awareness',
            'description': 'A simple meditation focusing on your breath. Perfect for beginners.',
            'duration': 5,
            'audio_url': '/audio/breathing-awareness.mp3',
            'image_url': '/images/meditation/breathing.jpg',
            'category': 'beginner',
            'level': 'beginner',
            'is_premium': False
        },
        {
            'title': 'Body Scan Relaxation',
            'description': 'Progressive relaxation through body awareness.',
            'duration': 10,
            'audio_url': '/audio/body-scan.mp3',
            'image_url': '/images/meditation/body-scan.jpg',
            'category': 'relaxation',
            'level': 'beginner',
            'is_premium': False
        },
        
        # Stress relief
        {
            'title': 'Stress Relief',
            'description': 'Release tension and find calm in stressful moments.',
            'duration': 15,
            'audio_url': '/audio/stress-relief.mp3',
            'image_url': '/images/meditation/stress-relief.jpg',
            'category': 'stress-relief',
            'level': 'intermediate',
            'is_premium': False
        },
        {
            'title': 'Anxiety Relief',
            'description': 'Calm your nervous system and reduce anxiety.',
            'duration': 20,
            'audio_url': '/audio/anxiety-relief.mp3',
            'image_url': '/images/meditation/anxiety.jpg',
            'category': 'anxiety',
            'level': 'intermediate',
            'is_premium': True
        },
        
        # Sleep
        {
            'title': 'Deep Sleep',
            'description': 'Fall asleep faster with this guided sleep meditation.',
            'duration': 30,
            'audio_url': '/audio/deep-sleep.mp3',
            'image_url': '/images/meditation/sleep.jpg',
            'category': 'sleep',
            'level': 'beginner',
            'is_premium': False
        },
        {
            'title': 'Lucid Dreaming',
            'description': 'Explore consciousness through lucid dreaming techniques.',
            'duration': 45,
            'audio_url': '/audio/lucid-dreaming.mp3',
            'image_url': '/images/meditation/dream.jpg',
            'category': 'sleep',
            'level': 'advanced',
            'is_premium': True
        },
        
        # Focus
        {
            'title': 'Focus & Concentration',
            'description': 'Improve your focus and mental clarity.',
            'duration': 15,
            'audio_url': '/audio/focus.mp3',
            'image_url': '/images/meditation/focus.jpg',
            'category': 'focus',
            'level': 'intermediate',
            'is_premium': False
        },
        {
            'title': 'Creative Flow',
            'description': 'Unlock your creative potential through meditation.',
            'duration': 25,
            'audio_url': '/audio/creative-flow.mp3',
            'image_url': '/images/meditation/creative.jpg',
            'category': 'creativity',
            'level': 'advanced',
            'is_premium': True
        },
        
        # Mindfulness
        {
            'title': 'Mindful Walking',
            'description': 'Practice mindfulness while walking.',
            'duration': 20,
            'audio_url': '/audio/mindful-walking.mp3',
            'image_url': '/images/meditation/walking.jpg',
            'category': 'mindfulness',
            'level': 'beginner',
            'is_premium': False
        },
        {
            'title': 'Loving Kindness',
            'description': 'Cultivate compassion for yourself and others.',
            'duration': 15,
            'audio_url': '/audio/loving-kindness.mp3',
            'image_url': '/images/meditation/loving-kindness.jpg',
            'category': 'compassion',
            'level': 'intermediate',
            'is_premium': True
        }
    ]
    
    for data in meditations:
        meditation = Meditation(**data)
        db.session.add(meditation)
    
    db.session.commit()
    print(f"✅ Seeded {len(meditations)} meditation sessions")