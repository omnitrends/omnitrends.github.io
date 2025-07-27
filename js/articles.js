// ===== ARTICLES DATA AND MANAGEMENT =====

// Articles database - loaded from JSON file
let articlesData = [];

/**
 * Load articles data from JSON file
 * @returns {Promise<Array>} Promise that resolves to articles array
 */
async function loadArticlesData() {
    try {
        // Determine the correct path based on current location
        const currentPath = window.location.pathname;
        const isInCategory = currentPath.includes('/category/');
        const isInArticle = currentPath.includes('/articles/');
        const jsonPath = (isInCategory || isInArticle) ? '../json/articles.json' : 'json/articles.json';
        
        const response = await fetch(jsonPath);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        articlesData = data;
        return data;
    } catch (error) {
        console.error('Error loading articles data:', error);
        // Fallback to empty array if loading fails
        articlesData = [];
        return [];
    }
}

// Categories configuration
const categoriesConfig = {
    'technology': { name: 'Technology', slug: 'technology' },
    'lifestyle': { name: 'Lifestyle', slug: 'lifestyle' },
    'business': { name: 'Business', slug: 'business' },
    'innovation': { name: 'Innovation', slug: 'innovation' },
    'news': { name: 'News', slug: 'news' },
    'health': { name: 'Health', slug: 'health' },
    'entertainment': { name: 'Entertainment', slug: 'entertainment' },
    'finance': { name: 'Finance', slug: 'finance' },
    'science': { name: 'Science', slug: 'science' },
    'travel': { name: 'Travel', slug: 'travel' },
    'food': { name: 'Food', slug: 'food' },
    'sports': { name: 'Sports', slug: 'sports' }
};

// ===== UTILITY FUNCTIONS =====

/**
 * Parse formatted date string to Date object
 * @param {string} dateStr - Date string in format "DD Month YYYY"
 * @returns {Date} Date object
 */
function parseFormattedDate(dateStr) {
    const months = {
        'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5,
        'July': 6, 'August': 7, 'September': 8, 'October': 9, 'November': 10, 'December': 11
    };
    
    const parts = dateStr.split(' ');
    if (parts.length !== 3) return new Date(0); // fallback for invalid format
    
    const day = parseInt(parts[0]);
    const month = months[parts[1]];
    const year = parseInt(parts[2]);
    
    return new Date(year, month, day);
}

/**
 * Get articles by category
 * @param {string} category - Category name
 * @returns {Array} Array of articles in the category
 */
function getArticlesByCategory(category) {
    return articlesData.filter(article => 
        article.category.toLowerCase() === category.toLowerCase()
    );
}

/**
 * Get article data by ID
 * @param {string} articleId - Article ID
 * @returns {Object|null} Article object or null if not found
 */
function getArticleById(articleId) {
    return articlesData.find(article => article.id === articleId) || null;
}

/**
 * Initialize article page with dynamic data
 * @param {string} articleId - Article ID
 */
function initializeArticlePage(articleId) {
    const article = getArticleById(articleId);
    if (!article) return;
    
    // Update article date elements
    const dateElements = document.querySelectorAll('.article-date, .article-card__date');
    dateElements.forEach(element => {
        element.textContent = article.date;
        element.setAttribute('datetime', article.date);
    });
    
    // Update structured data if present
    const structuredDataScript = document.querySelector('script[type="application/ld+json"]');
    if (structuredDataScript) {
        try {
            const structuredData = JSON.parse(structuredDataScript.textContent);
            const articleDate = parseFormattedDate(article.date);
            const isoDate = articleDate.toISOString();
            
            structuredData.datePublished = isoDate;
            structuredData.dateModified = isoDate;
            
            structuredDataScript.textContent = JSON.stringify(structuredData, null, 4);
        } catch (error) {
            console.error('Error updating structured data:', error);
        }
    }
    
    // Update meta tags
    const publishedTimeMeta = document.querySelector('meta[property="article:published_time"]');
    if (publishedTimeMeta) {
        const articleDate = parseFormattedDate(article.date);
        publishedTimeMeta.setAttribute('content', articleDate.toISOString());
    }
    
    // Load related articles
    loadRelatedArticles(article);
}

/**
 * Load related articles for the current article
 * @param {Object} currentArticle - Current article object
 */
function loadRelatedArticles(currentArticle) {
    const relatedGrid = document.getElementById('related-articles-grid');
    if (!relatedGrid) return;
    
    // Get articles from the same category, excluding current article
    const relatedArticles = articlesData
        .filter(article => 
            article.category === currentArticle.category && 
            article.id !== currentArticle.id
        )
        .sort((a, b) => parseFormattedDate(b.date) - parseFormattedDate(a.date))
        .slice(0, 2); // Show 2 related articles
    
    // If not enough articles in same category, fill with other featured articles
    if (relatedArticles.length < 2) {
        const otherArticles = articlesData
            .filter(article => 
                article.id !== currentArticle.id &&
                !relatedArticles.some(related => related.id === article.id)
            )
            .sort((a, b) => parseFormattedDate(b.date) - parseFormattedDate(a.date))
            .slice(0, 2 - relatedArticles.length);
        
        relatedArticles.push(...otherArticles);
    }
    
    // Generate HTML for related articles
    const relatedHTML = relatedArticles.map(article => createArticleCard(article, '../')).join('');
    relatedGrid.innerHTML = relatedHTML;
}

/**
 * Get latest articles sorted by date
 * @param {number} limit - Number of articles to return
 * @returns {Array} Array of latest articles
 */
function getLatestArticles(limit = 9) {
    return articlesData
        .sort((a, b) => parseFormattedDate(b.date) - parseFormattedDate(a.date))
        .slice(0, limit);
}

/**
 * Get featured articles sorted by date
 * @param {number} limit - Number of articles to return
 * @returns {Array} Array of featured articles
 */
function getFeaturedArticles(limit = 9) {
    return articlesData
        .filter(article => article.featured === true)
        .sort((a, b) => parseFormattedDate(b.date) - parseFormattedDate(a.date))
        .slice(0, limit);
}

/**
 * Create article card HTML
 * @param {Object} article - Article object
 * @param {string} basePath - Base path for links (e.g., '../' for category pages)
 * @returns {string} HTML string for article card
 */
function createArticleCard(article, basePath = '') {
    const imagePath = basePath ? `${basePath}images/${article.image}` : `images/${article.image}`;
    const articleUrl = basePath ? `${basePath}${article.url}` : article.url;
    
    return `
        <article class="article-card">
            <div class="article-card__image">
                <img src="${imagePath}" alt="${article.title}" loading="lazy">
            </div>
            <div class="article-card__content">
                <div class="article-card__meta">
                    <span class="article-card__category">${article.category}</span>
                    <time class="article-card__date" datetime="${article.date}">${article.date}</time>
                </div>
                <h3 class="article-card__title">
                    <a href="${articleUrl}">${article.title}</a>
                </h3>
                <p class="article-card__excerpt">${article.excerpt}</p>
                <a href="${articleUrl}" class="article-card__link">Read More</a>
            </div>
        </article>
    `;
}

/**
 * Create coming soon card HTML
 * @param {string} category - Category name
 * @param {string} title - Card title
 * @param {string} excerpt - Card excerpt
 * @returns {string} HTML string for coming soon card
 */
function createComingSoonCard(category, title, excerpt) {
    return `
        <article class="article-card" style="opacity: 0.6;">
            <div class="article-card__image">
                <div style="height: 200px; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); display: flex; align-items: center; justify-content: center; border-radius: var(--border-radius);">
                    <span style="color: var(--text-light); font-size: var(--font-size-sm);">Articles coming soon</span>
                </div>
            </div>
            <div class="article-card__content">
                <div class="article-card__meta">
                    <span class="article-card__category">${category}</span>
                    <time class="article-card__date" datetime="2024-12-01">Coming Soon</time>
                </div>
                <h3 class="article-card__title">
                    <a href="#" style="pointer-events: none;">${title}</a>
                </h3>
                <p class="article-card__excerpt">${excerpt}</p>
            </div>
        </article>
    `;
}

// ===== CATEGORY PAGE LOGIC =====

// Global variables for pagination
let currentCategoryArticles = [];
let displayedArticlesCount = 0;
const articlesPerPage = 9; // 3 rows × 3 columns

/**
 * Initialize category page with 1x3 structure and load more functionality
 */
function initializeCategoryPage() {
    // Get current category from URL
    const currentPath = window.location.pathname;
    const categoryMatch = currentPath.match(/\/category\/([^.]+)\.html/);
    
    if (!categoryMatch) return;
    
    const categorySlug = categoryMatch[1];
    const categoryConfig = categoriesConfig[categorySlug];
    
    if (!categoryConfig) return;
    
    const categoryName = categoryConfig.name;
    const articlesGrid = document.querySelector('.articles-grid');
    
    if (!articlesGrid) return;
    
    // Get articles for this category
    currentCategoryArticles = getArticlesByCategory(categoryName);
    const articleCount = currentCategoryArticles.length;
    
    // Reset displayed count
    displayedArticlesCount = 0;
    
    // Clear existing content
    articlesGrid.innerHTML = '';
    
    // Remove existing load more container if any
    const existingLoadMore = document.querySelector('.load-more-container');
    if (existingLoadMore) {
        existingLoadMore.remove();
    }
    
    // Load initial articles
    loadMoreCategoryArticles(categoryName, articlesGrid);
}

/**
 * Load more articles for category page
 */
function loadMoreCategoryArticles(categoryName, articlesGrid) {
    const articleCount = currentCategoryArticles.length;
    let cardsHTML = '';
    let articlesToShow = Math.min(articlesPerPage, articleCount - displayedArticlesCount);
    
    // Calculate how many coming soon cards we need for the current batch
    let comingSoonNeeded = 0;
    
    if (displayedArticlesCount === 0) {
        // First load - determine layout based on total articles
        if (articleCount === 0) {
            // No articles - show 3 coming soon cards
            comingSoonNeeded = 3;
            articlesToShow = 0;
        } else if (articleCount === 1) {
            // 1 article - show 1 article + 2 coming soon
            comingSoonNeeded = 2;
            articlesToShow = 1;
        } else if (articleCount === 2) {
            // 2 articles - show 2 articles + 1 coming soon
            comingSoonNeeded = 1;
            articlesToShow = 2;
        } else {
            // 3 or more articles - show up to 9 articles in first load
            articlesToShow = Math.min(9, articleCount);
            comingSoonNeeded = 0;
        }
    } else {
        // Subsequent loads - show up to 9 more articles
        articlesToShow = Math.min(9, articleCount - displayedArticlesCount);
        comingSoonNeeded = 0;
    }
    
    // Add real articles
    for (let i = 0; i < articlesToShow; i++) {
        const article = currentCategoryArticles[displayedArticlesCount + i];
        cardsHTML += createArticleCard(article, '../');
    }
    
    // Add coming soon cards if needed
    for (let i = 0; i < comingSoonNeeded; i++) {
        const comingSoonTitles = [
            `${categoryName} Articles Coming Soon`,
            `More ${categoryName} Content`,
            `Discover ${categoryName} Insights`
        ];
        
        const comingSoonExcerpts = [
            `Stay tuned for exciting content about ${categoryName.toLowerCase()} trends and insights.`,
            `Discover more insightful articles about ${categoryName.toLowerCase()} trends and insights.`,
            `Get ready for fresh perspectives on ${categoryName.toLowerCase()} topics.`
        ];
        
        cardsHTML += createComingSoonCard(
            categoryName,
            comingSoonTitles[i % comingSoonTitles.length],
            comingSoonExcerpts[i % comingSoonExcerpts.length]
        );
    }
    
    // Append new cards to grid
    articlesGrid.innerHTML += cardsHTML;
    
    // Update displayed count
    displayedArticlesCount += articlesToShow;
    
    // Add or update load more button
    updateLoadMoreButton(categoryName, articlesGrid);
}

/**
 * Update load more button visibility and functionality
 */
function updateLoadMoreButton(categoryName, articlesGrid) {
    const articleCount = currentCategoryArticles.length;
    const hasMoreArticles = displayedArticlesCount < articleCount;
    
    // Remove existing load more container
    const existingLoadMore = document.querySelector('.load-more-container');
    if (existingLoadMore) {
        existingLoadMore.remove();
    }
    
    // Add load more button if there are more articles and we've shown at least 9
    if (hasMoreArticles && displayedArticlesCount >= 9) {
        const loadMoreContainer = document.createElement('div');
        loadMoreContainer.className = 'load-more-container';
        
        const loadMoreBtn = document.createElement('button');
        loadMoreBtn.className = 'load-more-btn';
        loadMoreBtn.innerHTML = `
            <span class="spinner"></span>
            Load More Articles
        `;
        
        loadMoreBtn.addEventListener('click', function() {
            // Add loading state
            loadMoreBtn.classList.add('loading');
            loadMoreBtn.disabled = true;
            
            // Simulate loading delay for better UX
            setTimeout(() => {
                loadMoreCategoryArticles(categoryName, articlesGrid);
                loadMoreBtn.classList.remove('loading');
                loadMoreBtn.disabled = false;
            }, 500);
        });
        
        loadMoreContainer.appendChild(loadMoreBtn);
        
        // Insert after the articles grid
        articlesGrid.parentNode.insertBefore(loadMoreContainer, articlesGrid.nextSibling);
    }
}

// ===== INDEX PAGE LOGIC =====

/**
 * Initialize index page with featured articles
 */
function initializeIndexPage() {
    const articlesGrid = document.querySelector('.articles-grid');
    
    if (!articlesGrid) return;
    
    // Check if we're on the index page
    const currentPath = window.location.pathname;
    const isIndexPage = currentPath === '/' || currentPath.endsWith('/index.html') || currentPath === '/index.html';
    
    if (!isIndexPage) return;
    
    const featuredArticles = getFeaturedArticles(9);
    const totalArticles = featuredArticles.length;
    
    let cardsHTML = '';
    
    // Add featured articles
    cardsHTML = featuredArticles.map(article => createArticleCard(article)).join('');
    
    // Add coming soon cards if we have less than 9 featured articles
    if (totalArticles < 9) {
        const comingSoonCount = 9 - totalArticles;
        
        for (let i = 0; i < comingSoonCount; i++) {
            const comingSoonTitles = [
                'More Featured Content Coming Soon',
                'Exciting Featured Articles',
                'Featured Insights & Trends',
                'Discover Featured Perspectives',
                'Stay Tuned for Featured Updates',
                'Fresh Featured Content on the Way',
                'New Featured Articles in Development',
                'Coming Soon: Featured Expert Analysis',
                'More Featured Stories to Explore'
            ];
            
            const comingSoonExcerpts = [
                'Stay tuned for more featured articles covering the latest trends across technology, lifestyle, and innovation.',
                'Discover upcoming featured content that will keep you informed about the latest developments in various industries.',
                'Get ready for fresh featured perspectives and expert analysis on topics that matter most to you.',
                'More engaging featured content is on the way to help you stay ahead of the curve.',
                'We\'re working on exciting new featured articles that will provide valuable insights and trends.',
                'Coming soon: comprehensive featured guides and analysis on trending topics.',
                'New featured content is being developed to bring you the latest industry insights.',
                'Stay connected for upcoming featured articles featuring expert opinions and trend analysis.',
                'More featured stories and insights are coming to help you discover the latest trends.'
            ];
            
            cardsHTML += createComingSoonCard(
                'Featured',
                comingSoonTitles[i % comingSoonTitles.length],
                comingSoonExcerpts[i % comingSoonExcerpts.length]
            );
        }
    }
    
    articlesGrid.innerHTML = cardsHTML;
}

// ===== SEARCH FUNCTIONALITY UPDATE =====

/**
 * Update search functionality to use articles data
 */
function updateSearchFunctionality() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (!searchInput || !searchResults) return;
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }
        
        const filteredArticles = articlesData.filter(article => 
            article.title.toLowerCase().includes(query) ||
            article.excerpt.toLowerCase().includes(query) ||
            article.category.toLowerCase().includes(query)
        );
        
        if (filteredArticles.length > 0) {
            searchResults.innerHTML = filteredArticles.map(article => `
                <div class="search-result">
                    <h4><a href="${article.url}">${article.title}</a></h4>
                    <p>${article.excerpt}</p>
                    <span class="search-category">${article.category}</span>
                </div>
            `).join('');
            searchResults.style.display = 'block';
        } else {
            searchResults.innerHTML = '<div class="search-result">No articles found.</div>';
            searchResults.style.display = 'block';
        }
    });
    
    // Close search results when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}

// ===== INITIALIZATION =====

/**
 * Initialize articles functionality based on current page
 */
async function initializeArticles() {
    // Load articles data first
    await loadArticlesData();
    
    // Initialize based on current page
    initializeCategoryPage();
    initializeIndexPage();
    updateSearchFunctionality();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeArticles);

// Also initialize immediately if DOM is already loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeArticles);
} else {
    initializeArticles();
}

// ===== EXPORT FOR TESTING =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        articlesData,
        loadArticlesData,
        categoriesConfig,
        getArticlesByCategory,
        getLatestArticles,
        getFeaturedArticles,
        createArticleCard,
        createComingSoonCard
    };
}