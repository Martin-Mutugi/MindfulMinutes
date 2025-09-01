document.addEventListener('DOMContentLoaded', function() {
    // Filter functionality
    const filters = {
        category: document.getElementById('categoryFilter'),
        duration: document.getElementById('durationFilter'),
        level: document.getElementById('levelFilter')
    };
    
    const meditationGrid = document.getElementById('meditationGrid');
    const meditationCards = meditationGrid ? meditationGrid.querySelectorAll('.meditation-card') : [];
    
    // Add event listeners to filters
    Object.values(filters).forEach(filter => {
        if (filter) {
            filter.addEventListener('change', filterMeditations);
        }
    });
    
    function filterMeditations() {
        const categoryValue = filters.category.value;
        const durationValue = filters.duration.value;
        const levelValue = filters.level.value;
        
        meditationCards.forEach(card => {
            const category = card.dataset.category;
            const duration = parseInt(card.dataset.duration);
            const level = card.dataset.level;
            
            let show = true;
            
            // Category filter
            if (categoryValue !== 'all' && category !== categoryValue) {
                show = false;
            }
            
            // Duration filter
            if (durationValue !== 'all') {
                const dur = parseInt(durationValue);
                if (dur === 5 && duration > 5) show = false;
                if (dur === 10 && (duration <= 5 || duration > 10)) show = false;
                if (dur === 15 && (duration <= 10 || duration > 15)) show = false;
                if (dur === 20 && duration <= 15) show = false;
            }
            
            // Level filter
            if (levelValue !== 'all' && level !== levelValue) {
                show = false;
            }
            
            card.style.display = show ? 'block' : 'none';
        });
    }
    
    // Audio player functionality
    const audioPlayer = document.getElementById('audioPlayer');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    const currentTimeEl = document.getElementById('currentTime');
    const durationEl = document.getElementById('duration');
    const volumeSlider = document.getElementById('volumeSlider');
    
    if (audioPlayer && playBtn) {
        let isPlaying = false;
        
        // Update progress bar
        audioPlayer.addEventListener('timeupdate', updateProgress);
        
        // Update volume
        if (volumeSlider) {
            volumeSlider.addEventListener('input', function() {
                audioPlayer.volume = this.value;
            });
        }
        
        // Click on progress bar to seek
        if (progressBar) {
            progressBar.addEventListener('click', function(e) {
                const rect = this.getBoundingClientRect();
                const clickX = e.clientX - rect.left;
                const width = rect.width;
                const seekTime = (clickX / width) * audioPlayer.duration;
                audioPlayer.currentTime = seekTime;
            });
        }
        
        // Play button
        playBtn.addEventListener('click', function() {
            audioPlayer.play();
            isPlaying = true;
            updatePlayButton();
        });
        
        // Pause button
        if (pauseBtn) {
            pauseBtn.addEventListener('click', function() {
                audioPlayer.pause();
                isPlaying = false;
                updatePlayButton();
            });
        }
        
        // Update play button state
        function updatePlayButton() {
            if (isPlaying) {
                playBtn.style.display = 'none';
                if (pauseBtn) pauseBtn.style.display = 'block';
            } else {
                playBtn.style.display = 'block';
                if (pauseBtn) pauseBtn.style.display = 'none';
            }
        }
        
        // Update progress bar
        function updateProgress() {
            if (audioPlayer.duration) {
                const percent = (audioPlayer.currentTime / audioPlayer.duration) * 100;
                if (progressFill) {
                    progressFill.style.width = percent + '%';
                }
                
                // Update time display
                if (currentTimeEl) {
                    currentTimeEl.textContent = formatTime(audioPlayer.currentTime);
                }
                
                if (durationEl) {
                    durationEl.textContent = formatTime(audioPlayer.duration);
                }
            }
        }
        
        // Format time (seconds to MM:SS)
        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs.toString().padStart(2, '0')}`;
        }
        
        // Initialize time display
        audioPlayer.addEventListener('loadedmetadata', function() {
            if (durationEl) {
                durationEl.textContent = formatTime(audioPlayer.duration);
            }
        });
    }
    
    // Meditation session tracking
    const startSessionBtn = document.getElementById('startSessionBtn');
    if (startSessionBtn) {
        startSessionBtn.addEventListener('click', function() {
            const meditationId = this.dataset.meditationId;
            const duration = this.dataset.duration * 60; // Convert to seconds
            
            fetch('/meditation/start_session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    meditation_id: meditationId,
                    duration: duration
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Session started:', data);
            })
            .catch(error => {
                console.error('Error starting session:', error);
            });
        });
    }
    
    // End session when audio completes
    if (audioPlayer) {
        audioPlayer.addEventListener('ended', function() {
            const sessionId = this.dataset.sessionId;
            if (sessionId) {
                fetch(`/meditation/end_session/${sessionId}`, {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Session ended:', data);
                    // Show completion message
                    showCompletionMessage();
                })
                .catch(error => {
                    console.error('Error ending session:', error);
                });
            }
        });
    }
    
    function showCompletionMessage() {
        const message = document.createElement('div');
        message.className = 'completion-message';
        message.innerHTML = `
            <div class="message-content">
                <i class="fas fa-check-circle"></i>
                <h3>Session Completed!</h3>
                <p>Great job taking time for mindfulness.</p>
                <button class="btn btn-primary" onclick="this.parentElement.parentElement.remove()">Okay</button>
            </div>
        `;
        
        message.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        `;
        
        document.body.appendChild(message);
    }
});