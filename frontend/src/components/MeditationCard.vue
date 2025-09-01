<template>
  <div class="meditation-card">
    <img :src="meditation.image_url" alt="Meditation image" class="meditation-image" />
    <h3>{{ meditation.title }}</h3>
    <p class="mood-tag">🧘 Mood: {{ meditation.mood_tag }}</p>
    <audio :src="meditation.audio_url" controls></audio>
    <span v-if="meditation.is_premium" class="premium-badge">Premium 🔒</span>
    <p class="description">{{ meditation.description }}</p>
  </div>
</template>

<script>
export default {
  name: 'MeditationCard',
  props: {
    meditation: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.meditation-card {
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  background-color: #f9f9f9;
}
.meditation-image {
  width: 100%;
  border-radius: 6px;
}
.premium-badge {
  color: #e91e63;
  font-weight: bold;
}
.mood-tag {
  font-style: italic;
  color: #555;
}
</style>
