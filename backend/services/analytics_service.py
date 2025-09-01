from backend.models import JournalEntry, MeditationSession
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

class AnalyticsService:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_mood_analytics(self, days=30):
        """
        Get comprehensive mood analytics
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        entries = JournalEntry.query.filter(
            JournalEntry.user_id == self.user_id,
            JournalEntry.created_at >= start_date,
            JournalEntry.mood.isnot(None),
            JournalEntry.sentiment_score.isnot(None)
        ).order_by(JournalEntry.created_at).all()
        
        # Mood distribution
        mood_counts = defaultdict(int)
        mood_scores = defaultdict(list)
        
        for entry in entries:
            mood_counts[entry.mood] += 1
            mood_scores[entry.mood].append(entry.sentiment_score)
        
        # Calculate averages
        mood_averages = {}
        for mood, scores in mood_scores.items():
            mood_averages[mood] = statistics.mean(scores) if scores else 0
        
        # Time series data
        daily_moods = defaultdict(list)
        for entry in entries:
            date_str = entry.created_at.strftime('%Y-%m-%d')
            daily_moods[date_str].append({
                'mood': entry.mood,
                'score': entry.sentiment_score
            })
        
        # Calculate daily averages
        daily_averages = {}
        for date, moods in daily_moods.items():
            scores = [m['score'] for m in moods]
            daily_averages[date] = statistics.mean(scores) if scores else 0
        
        return {
            'mood_distribution': dict(mood_counts),
            'mood_averages': mood_averages,
            'daily_averages': daily_averages,
            'total_entries': len(entries),
            'timeframe_days': days
        }
    
    def get_meditation_analytics(self, days=30):
        """
        Get meditation practice analytics
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        sessions = MeditationSession.query.filter(
            MeditationSession.user_id == self.user_id,
            MeditationSession.started_at >= start_date,
            MeditationSession.completed == True
        ).order_by(MeditationSession.started_at).all()
        
        # Daily statistics
        daily_stats = defaultdict(list)
        for session in sessions:
            date_str = session.started_at.strftime('%Y-%m-%d')
            daily_stats[date_str].append(session.duration)
        
        # Calculate daily totals and averages
        daily_totals = {}
        daily_counts = {}
        for date, durations in daily_stats.items():
            daily_totals[date] = sum(durations) // 60  # Convert to minutes
            daily_counts[date] = len(durations)
        
        # Overall statistics
        total_minutes = sum(daily_totals.values())
        total_sessions = len(sessions)
        avg_session_length = total_minutes / total_sessions if total_sessions > 0 else 0
        
        # Consistency metrics
        practice_days = len(daily_totals)
        consistency_rate = (practice_days / days) * 100
        
        return {
            'daily_totals': dict(daily_totals),
            'daily_counts': dict(daily_counts),
            'total_minutes': total_minutes,
            'total_sessions': total_sessions,
            'avg_session_length': round(avg_session_length, 1),
            'practice_days': practice_days,
            'consistency_rate': round(consistency_rate, 1),
            'timeframe_days': days
        }
    
    def get_correlation_analysis(self, days=30):
        """
        Analyze correlation between meditation and mood
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get meditation data
        meditation_sessions = MeditationSession.query.filter(
            MeditationSession.user_id == self.user_id,
            MeditationSession.started_at >= start_date,
            MeditationSession.completed == True
        ).all()
        
        # Get journal data
        journal_entries = JournalEntry.query.filter(
            JournalEntry.user_id == self.user_id,
            JournalEntry.created_at >= start_date,
            JournalEntry.sentiment_score.isnot(None)
        ).all()
        
        # Group by date
        meditation_by_date = defaultdict(list)
        for session in meditation_sessions:
            date_str = session.started_at.strftime('%Y-%m-%d')
            meditation_by_date[date_str].append(session.duration)
        
        mood_by_date = defaultdict(list)
        for entry in journal_entries:
            date_str = entry.created_at.strftime('%Y-%m-%d')
            mood_by_date[date_str].append(entry.sentiment_score)
        
        # Find days with both meditation and journal entries
        correlation_data = []
        for date in set(meditation_by_date.keys()) & set(mood_by_date.keys()):
            avg_meditation = sum(meditation_by_date[date]) / len(meditation_by_date[date]) / 60  # minutes
            avg_mood = statistics.mean(mood_by_date[date])
            correlation_data.append({
                'date': date,
                'meditation_minutes': avg_meditation,
                'mood_score': avg_mood
            })
        
        # Calculate correlation if we have enough data
        correlation = 0
        if len(correlation_data) >= 2:
            try:
                meditation_values = [d['meditation_minutes'] for d in correlation_data]
                mood_values = [d['mood_score'] for d in correlation_data]
                correlation = statistics.correlation(meditation_values, mood_values)
            except:
                correlation = 0
        
        return {
            'correlation_data': correlation_data,
            'correlation_coefficient': round(correlation, 3),
            'days_with_both_data': len(correlation_data),
            'timeframe_days': days
        }
    
    def get_weekly_report(self):
        """
        Generate weekly insights report
        """
        mood_analytics = self.get_mood_analytics(7)
        meditation_analytics = self.get_meditation_analytics(7)
        correlation = self.get_correlation_analysis(7)
        
        # Generate insights
        insights = []
        
        # Mood insights
        if mood_analytics['total_entries'] > 0:
            most_common_mood = max(mood_analytics['mood_distribution'].items(), key=lambda x: x[1])[0]
            avg_mood_score = statistics.mean(mood_analytics['mood_averages'].values()) if mood_analytics['mood_averages'] else 0
            
            insights.append({
                'type': 'mood',
                'message': f'Your most common mood this week was {most_common_mood}',
                'value': most_common_mood
            })
            
            if avg_mood_score > 0.7:
                insights.append({
                    'type': 'positive',
                    'message': 'You had a very positive week overall!',
                    'value': round(avg_mood_score, 2)
                })
        
        # Meditation insights
        if meditation_analytics['total_sessions'] > 0:
            total_minutes = meditation_analytics['total_minutes']
            avg_length = meditation_analytics['avg_session_length']
            
            insights.append({
                'type': 'meditation',
                'message': f'You meditated for {total_minutes} minutes across {meditation_analytics["total_sessions"]} sessions',
                'value': total_minutes
            })
            
            if meditation_analytics['consistency_rate'] > 70:
                insights.append({
                    'type': 'consistency',
                    'message': 'Great consistency in your practice this week!',
                    'value': meditation_analytics['consistency_rate']
                })
        
        # Correlation insights
        if correlation['correlation_coefficient'] > 0.3:
            insights.append({
                'type': 'correlation',
                'message': 'Your meditation practice appears to positively influence your mood',
                'value': correlation['correlation_coefficient']
            })
        
        return {
            'mood_analytics': mood_analytics,
            'meditation_analytics': meditation_analytics,
            'correlation_analysis': correlation,
            'insights': insights,
            'week_start': (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'week_end': datetime.utcnow().strftime('%Y-%m-%d')
        }

# Utility functions
def get_user_analytics(user_id, days=30):
    service = AnalyticsService(user_id)
    return {
        'mood': service.get_mood_analytics(days),
        'meditation': service.get_meditation_analytics(days),
        'correlation': service.get_correlation_analysis(days)
    }

def get_weekly_user_report(user_id):
    service = AnalyticsService(user_id)
    return service.get_weekly_report()