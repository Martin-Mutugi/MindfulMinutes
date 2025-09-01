const ctx = document.getElementById('moodChart').getContext('2d');
const moodChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: moodData.labels,
    datasets: [{
      label: 'Mood Over Time',
      data: moodData.values,
      borderColor: '#0077cc',
      fill: false
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: { beginAtZero: true }
    }
  }
});
