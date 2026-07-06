document.addEventListener('DOMContentLoaded', () => {
    // App State
    let currentFeedUrl = '';
    let articlesList = [];
    
    // UI Elements
    const articlesContainer = document.getElementById('articles-container');
    const skeletonContainer = document.getElementById('skeleton-container');
    const emptyState = document.getElementById('empty-state');
    
    const refreshBtn = document.getElementById('refresh-btn');
    const refreshIcon = document.getElementById('refresh-icon');
    
    const feedTitle = document.getElementById('current-feed-title');
    const feedDesc = document.getElementById('current-feed-desc');
    
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search-btn');
    
    const customFeedForm = document.getElementById('custom-feed-form');
    const customUrlInput = document.getElementById('custom-url-input');
    
    const presetButtons = document.querySelectorAll('.preset-btn');
    
    const errorBanner = document.getElementById('error-banner');
    const errorMessage = document.getElementById('error-message');
    const closeErrorBtn = document.getElementById('close-error-btn');

    // Initialize Lucide Icons
    if (window.lucide) {
        window.lucide.createIcons();
    }

    // Load initial feed (TechCrunch)
    const initialPreset = document.querySelector('.preset-btn[data-name="techcrunch"]');
    if (initialPreset) {
        setActivePreset(initialPreset);
        fetchArticles(initialPreset.dataset.url);
    } else if (presetButtons.length > 0) {
        setActivePreset(presetButtons[0]);
        fetchArticles(presetButtons[0].dataset.url);
    }

    // Bind Presets
    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            setActivePreset(btn);
            fetchArticles(btn.dataset.url);
        });
    });

    // Custom Feed Form Submit
    customFeedForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const url = customUrlInput.value.trim();
        if (url) {
            clearPresetActives();
            fetchArticles(url);
        }
    });

    // Refresh Button Click
    refreshBtn.addEventListener('click', () => {
        if (currentFeedUrl) {
            fetchArticles(currentFeedUrl);
        }
    });

    // Search Input Filtering
    searchInput.addEventListener('input', () => {
        filterAndRenderArticles();
    });

    // Clear Search Buttons
    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        filterAndRenderArticles();
    });

    // Close Error Banner
    closeErrorBtn.addEventListener('click', () => {
        errorBanner.classList.add('hidden');
    });

    // Helper functions
    function setActivePreset(selectedBtn) {
        clearPresetActives();
        selectedBtn.classList.add('active');
        // Pre-fill custom input to show current URL
        customUrlInput.value = selectedBtn.dataset.url;
    }

    function clearPresetActives() {
        presetButtons.forEach(btn => btn.classList.remove('active'));
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorBanner.classList.remove('hidden');
        // Auto scroll to error banner if on mobile
        errorBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideError() {
        errorBanner.classList.add('hidden');
    }

    // API Call to fetch RSS Articles
    async function fetchArticles(feedUrl) {
        currentFeedUrl = feedUrl;
        
        // UI states: Loading
        showLoadingState(true);
        hideError();
        emptyState.classList.add('hidden');

        try {
            const apiUrl = `/api/articles?url=${encodeURIComponent(feedUrl)}`;
            const response = await fetch(apiUrl);
            const data = await response.json();

            if (data.success) {
                articlesList = data.articles;
                
                // Update Feed metadata headers
                feedTitle.textContent = data.title || 'RSS Feed';
                feedDesc.textContent = data.description || 'Custom RSS News Stream';
                
                // Render
                renderArticles(articlesList);
            } else {
                showError(data.error || 'Failed to parse RSS feed.');
                articlesContainer.innerHTML = '';
            }
        } catch (err) {
            console.error('Fetch error:', err);
            showError('Network error: Could not reach the server.');
            articlesContainer.innerHTML = '';
        } finally {
            showLoadingState(false);
        }
    }

    // Toggle Skeleton loader and button animations
    function showLoadingState(isLoading) {
        if (isLoading) {
            skeletonContainer.classList.remove('hidden');
            articlesContainer.classList.add('hidden');
            
            // Spin the refresh button icon
            refreshBtn.classList.add('spinning');
            refreshBtn.disabled = true;
        } else {
            skeletonContainer.classList.add('hidden');
            articlesContainer.classList.remove('hidden');
            
            // Stop spin
            refreshBtn.classList.remove('spinning');
            refreshBtn.disabled = false;
        }
    }

    // Render articles with custom animations and fallback image layouts
    function renderArticles(articles) {
        articlesContainer.innerHTML = '';

        if (articles.length === 0) {
            emptyState.classList.remove('hidden');
            return;
        }

        emptyState.classList.add('hidden');

        articles.forEach((article, index) => {
            const card = document.createElement('article');
            card.className = 'article-card';
            // Stagger animation delays for sleek item cascade effect
            card.style.animationDelay = `${index * 0.05}s`;

            // Setup Image Area (check if article has image_url)
            let imageHtml = '';
            if (article.image_url) {
                imageHtml = `
                    <div class="card-image-wrapper">
                        <img src="${article.image_url}" class="card-image" alt="Article visual" onerror="this.parentElement.innerHTML = getFallbackImageHtml();">
                    </div>
                `;
            } else {
                imageHtml = `
                    <div class="card-image-wrapper">
                        ${getFallbackImageHtml()}
                    </div>
                `;
            }

            card.innerHTML = `
                ${imageHtml}
                <div class="card-body">
                    <div class="card-meta">
                        <span class="card-meta-item">
                            <i data-lucide="calendar"></i>
                            <span>${article.published}</span>
                        </span>
                    </div>
                    
                    <a href="${article.link}" target="_blank" rel="noopener noreferrer" class="card-title">
                        ${article.title}
                    </a>
                    
                    <p class="card-summary">${article.summary}</p>
                    
                    <div class="card-footer">
                        <span class="author-tag" title="${article.author}">By ${article.author}</span>
                        <a href="${article.link}" target="_blank" rel="noopener noreferrer" class="read-more-link">
                            <span>Read Article</span>
                            <i data-lucide="arrow-up-right"></i>
                        </a>
                    </div>
                </div>
            `;

            articlesContainer.appendChild(card);
        });

        // Re-render injected lucide SVGs
        if (window.lucide) {
            window.lucide.createIcons();
        }
    }

    // Local Search Filter
    function filterAndRenderArticles() {
        const query = searchInput.value.toLowerCase().trim();
        
        if (!query) {
            renderArticles(articlesList);
            return;
        }

        const filtered = articlesList.filter(article => {
            const titleMatch = article.title.toLowerCase().includes(query);
            const summaryMatch = article.summary.toLowerCase().includes(query);
            const authorMatch = article.author.toLowerCase().includes(query);
            return titleMatch || summaryMatch || authorMatch;
        });

        renderArticles(filtered);
    }

    // HTML template for default fallback card images
    function getFallbackImageHtml() {
        return `
            <div class="card-image-fallback">
                <svg class="fallback-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 11a9 9 0 0 1 9 9"></path>
                    <path d="M4 4a16 16 0 0 1 16 16"></path>
                    <circle cx="5" cy="19" r="1"></circle>
                </svg>
            </div>
        `;
    }
});
