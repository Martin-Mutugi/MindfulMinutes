<template>
  <div class="dashboard">
    <h1>Welcome back, {{ userName }} 👋</h1>

    <section class="prompt-section">
      <h2>🧠 Journaling Prompt</h2>
      <p class="prompt">{{ prompt }}</p>
    </section>

    <section class="recommendations">
      <h2>🧘 Recommended Meditations</h2>
      <MeditationList />
    </section>
  </div>
</template>

<script>
import MeditationList from '../components/MeditationList.vue'

export default {
  name: 'Dashboard',
  components: { MeditationList },
  data() {
    return {
      userName: 'Mindful Explorer', // Replace with actual user name if available
      prompt: ''
    }
  },
  async mounted() {
    try {
      const res = await fetch('/api/suggestions')
      const data = await res.json()
      this.prompt = data.prompt
    } catch (err) {
      console.error('Failed to fetch journaling prompt:', err)
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 800px;
  margin: auto;
}
.prompt-section {
  background-color: #f0f8ff;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
.prompt {
  font-size: 1.2rem;
  color: #333;
}
.recommendations {
  margin-top: 2rem;
}
</style>
