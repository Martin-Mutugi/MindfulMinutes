document.addEventListener('DOMContentLoaded', function() {
    // Mood selection
    const moodButtons = document.querySelectorAll('.mood-btn');
    const moodInput = document.getElementById('mood');
    
    moodButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            moodButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Set hidden input value
            moodInput.value = this.dataset.mood;
        });
    });
    
    // Initialize mood if already selected
    if (moodInput.value) {
        const selectedButton = document.querySelector(`.mood-btn[data-mood="${moodInput.value}"]`);
        if (selectedButton) {
            selectedButton.classList.add('active');
        }
    }
    
    // Auto-resize textarea
    const textarea = document.querySelector('.journal-textarea');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Trigger initial resize
        setTimeout(() => {
            textarea.dispatchEvent(new Event('input'));
        }, 100);
    }
    
    // Word count display
    const wordCountDisplay = document.createElement('div');
    wordCountDisplay.className = 'word-count';
    wordCountDisplay.style.cssText = `
        position: absolute;
        bottom: 10px;
        right: 10px;
        color: var(--text-secondary);
        font-size: 0.8rem;
        background: var(--bg-white);
        padding: 0.25rem 0.5rem;
        border-radius: 10px;
    `;
    
    if (textarea) {
        textarea.parentElement.style.position = 'relative';
        textarea.parentElement.appendChild(wordCountDisplay);
        
        textarea.addEventListener('input', updateWordCount);
        updateWordCount();
    }
    
    function updateWordCount() {
        const text = textarea.value.trim();
        const wordCount = text ? text.split(/\s+/).length : 0;
        wordCountDisplay.textContent = `${wordCount} words`;
        
        // Change color based on length
        if (wordCount < 50) {
            wordCountDisplay.style.color = '#f44336';
        } else if (wordCount < 100) {
            wordCountDisplay.style.color = '#ff9800';
        } else {
            wordCountDisplay.style.color = '#4caf50';
        }
    }
    
    // Save draft functionality
    let draftTimer;
    const DRAFT_KEY = 'journal_draft';
    
    if (textarea) {
        textarea.addEventListener('input', function() {
            clearTimeout(draftTimer);
            draftTimer = setTimeout(saveDraft, 1000);
        });
        
        // Load draft on page load
        loadDraft();
    }
    
    function saveDraft() {
        const draft = {
            title: document.getElementById('title').value,
            content: textarea.value,
            tags: document.getElementById('tags').value,
            mood: moodInput.value,
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem(DRAFT_KEY, JSON.stringify(draft));
        showToast('Draft saved automatically');
    }
    
    function loadDraft() {
        const draft = localStorage.getItem(DRAFT_KEY);
        if (draft) {
            try {
                const data = JSON.parse(draft);
                if (data.content && !textarea.value) {
                    if (confirm('You have a saved draft. Would you like to load it?')) {
                        document.getElementById('title').value = data.title || '';
                        textarea.value = data.content || '';
                        document.getElementById('tags').value = data.tags || '';
                        moodInput.value = data.mood || '';
                        
                        // Update mood button
                        if (data.mood) {
                            moodButtons.forEach(btn => btn.classList.remove('active'));
                            const selectedBtn = document.querySelector(`.mood-btn[data-mood="${data.mood}"]`);
                            if (selectedBtn) selectedBtn.classList.add('active');
                        }
                        
                        // Trigger resize and word count
                        textarea.dispatchEvent(new Event('input'));
                        showToast('Draft loaded successfully');
                    }
                }
            } catch (e) {
                console.error('Error loading draft:', e);
            }
        }
    }
    
    // Clear draft on successful submission
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            localStorage.removeItem(DRAFT_KEY);
        });
    }
    
    // Toast notification
    function showToast(message) {
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--text-primary);
            color: white;
            padding: 12px 20px;
            border-radius: var(--radius);
            z-index: 1000;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    // Entry view page functionality
    const entryContent = document.querySelector('.entry-content');
    if (entryContent && entryContent.textContent.length > 500) {
        const readMoreBtn = document.createElement('button');
        readMoreBtn.textContent = 'Read more';
        readMoreBtn.className = 'btn btn-outline btn-sm';
        readMoreBtn.style.marginTop = '1rem';
        
        const fullContent = entryContent.innerHTML;
        const truncatedContent = fullContent.substring(0, 500) + '...';
        
        entryContent.innerHTML = truncatedContent;
        entryContent.parentElement.appendChild(readMoreBtn);
        
        let isExpanded = false;
        readMoreBtn.addEventListener('click', function() {
            isExpanded = !isExpanded;
            entryContent.innerHTML = isExpanded ? fullContent : truncatedContent;
            readMoreBtn.textContent = isExpanded ? 'Read less' : 'Read more';
        });
    }
});