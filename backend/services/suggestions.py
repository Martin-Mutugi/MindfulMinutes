from backend.models import JournalEntry, Meditation
from sqlalchemy import desc
from datetime import datetime, timedelta

# --- Sentiment Extraction ---
def get_latest_sentiment(user):
    entry = JournalEntry.query.filter_by(author=user).order_by(desc(JournalEntry.created_at)).first()
    if entry and entry.sentiment_label:
        return entry.sentiment_label.lower()
    return None

# --- Meditation Suggestions ---
def suggest_meditations(user):
    mood = get_latest_sentiment(user)
    query = Meditation.query

    if mood:
        query = query.filter_by(mood_tag=mood)

    limit = 8 if user.is_premium else 4
    return query.limit(limit).all()

# --- Journaling Streak Calculation ---
def get_journaling_streak(user):
    entries = JournalEntry.query.filter_by(author=user).order_by(desc(JournalEntry.created_at)).all()
    if not entries:
        return 0

    streak = 1
    today = datetime.utcnow().date()
    previous_date = entries[0].created_at.date()

    for entry in entries[1:]:
        current_date = entry.created_at.date()
        if previous_date - current_date == timedelta(days=1):
            streak += 1
            previous_date = current_date
        else:
            break

    return streak

# --- Prompt Suggestions ---
def suggest_journaling_prompt(user):
    streak = get_journaling_streak(user)
    sentiment = get_latest_sentiment(user)

    if streak >= 7:
        return "You've built a powerful habit. What mindset shift helped you most this week?"
    elif streak >= 3:
        return "You're gaining momentum. What’s one thing you’re grateful for today?"
    elif sentiment == "negative":
        return "What’s been weighing on your mind lately? Let it out."
    elif sentiment == "positive":
        return "Capture this moment of joy — what made today feel good?"
    else:
        return "Start fresh: What’s on your mind right now?"

# --- Combined Suggestions ---
def get_suggestions(user):
    return {
        "meditations": suggest_meditations(user),
        "prompt": suggest_journaling_prompt(user)
    }
