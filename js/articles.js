// ===== ARTICLES DATA AND MANAGEMENT =====

// Articles database - This would typically come from a CMS or API
const articlesData = [
    {
        id: 'ai-revolution-2024',
        title: 'The AI Revolution: How Artificial Intelligence is Reshaping Industries in 2024',
        category: 'Technology',
        date: '2025-08-01',
        dateFormatted: '01 August 2025',
        excerpt: 'Explore how AI is transforming healthcare, finance, and education, creating new opportunities and challenges for businesses worldwide.',
        image: 'ai-revolution-2024.jpg',
        url: 'articles/ai-revolution-2024.html',
        featured: true
    },
    {
        id: 'sustainable-living-guide',
        title: 'The Complete Guide to Sustainable Living in 2024',
        category: 'Lifestyle',
        date: '2025-08-01',
        dateFormatted: '01 August 2025',
        excerpt: 'Discover practical tips and strategies for reducing your environmental footprint while maintaining a comfortable lifestyle.',
        image: 'sustainable-living-guide.jpg',
        url: 'articles/sustainable-living-guide.html',
        featured: true
    },
    {
        id: 'remote-work-trends',
        title: 'Remote Work Evolution: Trends Shaping the Future of Employment',
        category: 'Business',
        date: '2025-08-01',
        dateFormatted: '01 August 2025',
        excerpt: 'Analyze the latest remote work trends and their impact on productivity, company culture, and work-life balance.',
        image: 'remote-work-trends.jpg',
        url: 'articles/remote-work-trends.html',
        featured: true
    },
    // Example additional articles to demonstrate multiple articles in a category
    {
        id: 'tech-trends-2025',
        title: 'Top Technology Trends to Watch in 2025',
        category: 'Technology',
        date: '2025-07-28',
        dateFormatted: '28 July 2025',
        excerpt: 'Discover the emerging technology trends that will define 2025, from quantum computing to advanced robotics.',
        image: 'ai-revolution-2024.jpg', // Reusing existing image for demo
        url: '#', // Placeholder URL
        featured: false
    },
    {
        id: 'cybersecurity-guide',
        title: 'Essential Cybersecurity Practices for Modern Businesses',
        category: 'Technology',
        date: '2025-07-25',
        dateFormatted: '25 July 2025',
        excerpt: 'Learn about the latest cybersecurity threats and how to protect your business with proven security strategies.',
        image: 'ai-revolution-2024.jpg', // Reusing existing image for demo
        url: '#', // Placeholder URL
        featured: false
    },
    {
        id: 'digital-transformation',
        title: 'Digital Transformation: A Complete Guide for Enterprises',
        category: 'Technology',
        date: '2025-07-20',
        dateFormatted: '20 July 2025',
        excerpt: 'Navigate the digital transformation journey with expert insights and practical implementation strategies.',
        image: 'ai-revolution-2024.jpg', // Reusing existing image for demo
        url: '#', // Placeholder URL
        featured: false
    },
    {
        id: 'digital-transformation',
        title: 'Digital Transformation: A Complete Guide for Enterprises',
        category: 'Business',
        date: '2025-07-20',
        dateFormatted: '20 July 2025',
        excerpt: 'Navigate the digital transformation journey with expert insights and practical implementation strategies.',
        image: 'ai-revolution-2024.jpg', // Reusing existing image for demo
        url: '#', // Placeholder URL
        featured: false
    },
    {
        id: 'digital-transformation',
        title: 'Digital Transformation: A Complete Guide for Enterprises',
        category: 'Business',
        date: '2025-07-20',
        dateFormatted: '20 July 2025',
        excerpt: 'Navigate the digital transformation journey with expert insights and practical implementation strategies.',
        image: 'ai-revolution-2024.jpg', // Reusing existing image for demo
        url: '#', // Placeholder URL
        featured: false
    },
    {
        id: 'digital-transformation',
        title: 'Digital Transformation: A Complete Guide for Enterprises',
        category: 'Business',
        date: '2025-07-20',
        dateFormatted: '20 July 2025',
        excerpt: 'Navigate the digital transformation journey with expert insights and practical implementation strategies.',
        image: 'ai-revolution-2024.jpg', // Reusing existing image for demo
        url: '#', // Placeholder URL
        featured: false
    },
    {
        id: 'digital-transformation',
        title: 'Digital Transformation: A Complete Guide for Enterprises',
        category: 'Business',
        date: '2025-07-20',
        dateFormatted: '20 July 2025',
        excerpt: 'Navigate the digital transformation journey with expert insights and practical implementation strategies.',
        image: 'ai-revolution-2024.jpg', // Reusing existing image for demo
        url: '#', // Placeholder URL
        featured: false
    }
];

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
 * Get latest articles sorted by date
 * @param {number} limit - Number of articles to return
 * @returns {Array} Array of latest articles
 */
function getLatestArticles(limit = 9) {
    return articlesData
        .sort((a, b) => new Date(b.date) - new Date(a.date))
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
                    <time class="article-card__date" datetime="${article.date}">${article.dateFormatted}</time>
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

/**
 * Initialize category page with 2-column structure
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
    const categoryArticles = getArticlesByCategory(categoryName);
    const articleCount = categoryArticles.length;
    
    let cardsHTML = '';
    
    if (articleCount >= 2) {
        // Show ALL real articles (not just 2)
        cardsHTML = categoryArticles.map(article => 
            createArticleCard(article, '../')
        ).join('');
    } else if (articleCount === 1) {
        // Show 1 real article + 1 coming soon
        cardsHTML = createArticleCard(categoryArticles[0], '../');
        cardsHTML += createComingSoonCard(
            categoryName,
            `More ${categoryName} Content`,
            `Discover more insightful articles about ${categoryName.toLowerCase()} trends and insights.`
        );
    } else {
        // Show 2 coming soon cards
        cardsHTML = createComingSoonCard(
            categoryName,
            `${categoryName} Articles Coming Soon`,
            `Stay tuned for exciting content about ${categoryName.toLowerCase()} trends and insights.`
        );
        cardsHTML += createComingSoonCard(
            categoryName,
            `More ${categoryName} Content`,
            `Discover the latest in ${categoryName.toLowerCase()} and stay ahead of the curve.`
        );
    }
    
    articlesGrid.innerHTML = cardsHTML;
}

// ===== INDEX PAGE LOGIC =====

/**
 * Initialize index page with 3x3 grid (9 articles)
 */
function initializeIndexPage() {
    const articlesGrid = document.querySelector('.articles-grid');
    
    if (!articlesGrid) return;
    
    // Check if we're on the index page
    const currentPath = window.location.pathname;
    const isIndexPage = currentPath === '/' || currentPath.endsWith('/index.html') || currentPath === '/index.html';
    
    if (!isIndexPage) return;
    
    const latestArticles = getLatestArticles(9);
    const totalArticles = latestArticles.length;
    
    let cardsHTML = '';
    
    // Add real articles
    cardsHTML = latestArticles.map(article => createArticleCard(article)).join('');
    
    // Add coming soon cards if we have less than 9 articles
    if (totalArticles < 9) {
        const comingSoonCount = 9 - totalArticles;
        
        for (let i = 0; i < comingSoonCount; i++) {
            const comingSoonTitles = [
                'Exciting Content Coming Soon',
                'More Trending Articles',
                'Latest Insights & Trends',
                'Discover New Perspectives',
                'Stay Tuned for Updates',
                'Fresh Content on the Way',
                'New Articles in Development',
                'Coming Soon: Expert Analysis',
                'More Stories to Explore'
            ];
            
            const comingSoonExcerpts = [
                'Stay tuned for more insightful articles covering the latest trends across technology, lifestyle, and innovation.',
                'Discover upcoming content that will keep you informed about the latest developments in various industries.',
                'Get ready for fresh perspectives and expert analysis on topics that matter most to you.',
                'More engaging content is on the way to help you stay ahead of the curve.',
                'We\'re working on exciting new articles that will provide valuable insights and trends.',
                'Coming soon: comprehensive guides and analysis on trending topics.',
                'New content is being developed to bring you the latest industry insights.',
                'Stay connected for upcoming articles featuring expert opinions and trend analysis.',
                'More stories and insights are coming to help you discover the latest trends.'
            ];
            
            cardsHTML += createComingSoonCard(
                'Coming Soon',
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
function initializeArticles() {
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
        categoriesConfig,
        getArticlesByCategory,
        getLatestArticles,
        createArticleCard,
        createComingSoonCard
    };
}