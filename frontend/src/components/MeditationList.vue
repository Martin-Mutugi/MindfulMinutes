<template>
  <div>
    <h2>🧘 Recommended for You</h2>
    <p class="prompt">{{ prompt }}</p>

    <div v-if="meditations.length">
      <MeditationCard v-for="m in meditations" :key="m.id" :meditation="m" />
    </div>
    <div v-else>
      <p>No meditations found for your current mood. Try journaling again or explore all sessions.</p>
    </div>
  </div>
</template>

<script>
import MeditationCard from './MeditationCard.vue'

export default {
  name: 'MeditationList',
  components: { MeditationCard },
  data() {
    return {
      meditations: [],
      prompt: ''
    }
  },
  async mounted() {
    try {
      const res = await fetch('/api/suggestions')
      const data = await res.json()
      this.meditations = data.meditations
      this.prompt = data.prompt
    } catch (err) {
      console.error('Failed to fetch suggestions:', err)
    }
  }
}
</script>

<style scoped>
.prompt {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #333;
}
</style>
