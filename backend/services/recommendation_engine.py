from backend.models import JournalEntry, MeditationSession, Meditation
from datetime import datetime, timedelta
from collections import Counter
import random

class RecommendationEngine:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_recommendations(self, limit=5):
        """
        Get personalized meditation recommendations
        """
        # Get user's recent mood from journal entries
        recent_mood = self._get_recent_mood()
        
        # Get meditation preferences from session history
        preferences = self._get_user_preferences()
        
        # Base query
        query = Meditation.query.filter_by(is_premium=False)
        
        # Filter by mood if available
        if recent_mood:
            mood_categories = self._get_mood_categories(recent_mood)
            if mood_categories:
                query = query.filter(Meditation.category.in_(mood_categories))
        
        # Filter by preferences
        if preferences:
            preferred_categories = [cat for cat, count in preferences.most_common(3)]
            query = query.filter(Meditation.category.in_(preferred_categories))
        
        # Get recommendations
        recommendations = query.order_by(Meditation.duration.asc()).limit(limit).all()
        
        # If not enough recommendations, add some popular ones
        if len(recommendations) < limit:
            popular = self._get_popular_meditations(limit - len(recommendations))
            recommendations.extend(popular)
        
        return recommendations
    
    def _get_recent_mood(self):
        """
        Get user's most recent mood from journal entries
        """
        recent_entry = JournalEntry.query.filter_by(
            user_id=self.user_id
        ).order_by(JournalEntry.created_at.desc()).first()
        
        return recent_entry.mood if recent_entry else None
    
    def _get_user_preferences(self):
        """
        Get user's meditation preferences from session history
        """
        # Get sessions from last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        sessions = MeditationSession.query.filter(
            MeditationSession.user_id == self.user_id,
            MeditationSession.started_at >= thirty_days_ago,
            MeditationSession.meditation_id.isnot(None)
        ).join(Meditation).all()
        
        # Count categories
        categories = [session.meditation.category for session in sessions if session.meditation]
        return Counter(categories)
    
    def _get_mood_categories(self, mood):
        """
        Map moods to meditation categories
        """
        mood_mapping = {
            'happy': ['gratitude', 'joy', 'energy'],
            'calm': ['relaxation', 'breathing', 'mindfulness'],
            'sad': ['compassion', 'self-love', 'healing'],
            'anxious': ['anxiety', 'stress-relief', 'grounding'],
            'tired': ['energy', 'focus', 'morning'],
            'stressed': ['stress-relief', 'relaxation', 'sleep']
        }
        
        return mood_mapping.get(mood.lower(), [])
    
    def _get_popular_meditations(self, limit=3):
        """
        Get generally popular meditations
        """
        return Meditation.query.filter_by(is_premium=False)\
            .order_by(Meditation.duration.asc())\
            .limit(limit)\
            .all()
    
    def get_daily_recommendation(self):
        """
        Get a single daily recommendation
        """
        recommendations = self.get_recommendations(limit=3)
        return random.choice(recommendations) if recommendations else None

# Utility function to get recommendations for a user
def get_user_recommendations(user_id, limit=5):
    engine = RecommendationEngine(user_id)
    return engine.get_recommendations(limit)

def get_daily_recommendation(user_id):
    engine = RecommendationEngine(user_id)
    return engine.get_daily_recommendation()