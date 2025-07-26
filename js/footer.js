// ===== DYNAMIC FOOTER GENERATOR =====
class DynamicFooter {
    constructor() {
        this.isSubdirectory = this.detectDirectory();
        this.basePath = this.isSubdirectory ? '../' : '';
        this.init();
    }

    detectDirectory() {
        // Check if we're in a subdirectory by looking at the current path
        const path = window.location.pathname;
        const pathSegments = path.split('/').filter(segment => segment.length > 0);
        
        // If we have more than 1 segment (excluding the domain), we're likely in a subdirectory
        // Or if the path contains common subdirectory names
        return pathSegments.length > 1 || 
               path.includes('/pages/') || 
               path.includes('/category/') || 
               path.includes('/articles/');
    }

    generateFooterHTML() {
        return `
            <footer class="footer">
                <div class="container">
                    <div class="footer__content">
                        <div class="footer__section">
                            <h3 class="footer__title">OmniTrends</h3>
                            <p class="footer__description">Your source for the latest trends, insights, and discoveries across technology, lifestyle, and innovation.</p>
                        </div>
                        
                        <div class="footer__section">
                            <h4 class="footer__subtitle">Quick Links</h4>
                            <ul class="footer__links">
                                <li><a href="${this.basePath}index.html">Home</a></li>
                                <li><a href="${this.basePath}pages/about.html">About</a></li>
                                <li><a href="${this.basePath}pages/contact.html">Contact</a></li>
                                <li><a href="${this.basePath}pages/privacy.html">Privacy Policy</a></li>
                                <li><a href="${this.basePath}pages/terms.html">Terms & Conditions</a></li>
                                <li><a href="${this.basePath}pages/disclaimer.html">Disclaimer</a></li>
                            </ul>
                        </div>
                        
                        <div class="footer__section">
                            <h4 class="footer__subtitle">Categories</h4>
                            <ul class="footer__links">
                                <li><a href="${this.basePath}category/technology.html">Technology</a></li>
                                <li><a href="${this.basePath}category/lifestyle.html">Lifestyle</a></li>
                                <li><a href="${this.basePath}category/business.html">Business</a></li>
                                <li><a href="${this.basePath}category/innovation.html">Innovation</a></li>
                                <li><a href="${this.basePath}category/news.html">News</a></li>
                                <li><a href="${this.basePath}category/health.html">Health</a></li>
                                <li><a href="${this.basePath}category/entertainment.html">Entertainment</a></li>
                                <li><a href="${this.basePath}category/finance.html">Finance</a></li>
                                <li><a href="${this.basePath}category/science.html">Science</a></li>
                                <li><a href="${this.basePath}category/travel.html">Travel</a></li>
                                <li><a href="${this.basePath}category/food.html">Food</a></li>
                                <li><a href="${this.basePath}category/sports.html">Sports</a></li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="footer__bottom">
                        <p>&copy; 2025 OmniTrends. All rights reserved.</p>
                    </div>
                </div>
            </footer>
        `;
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.injectFooter());
        } else {
            this.injectFooter();
        }
    }

    injectFooter() {
        // Look for existing footer to replace, or append to body
        const existingFooter = document.querySelector('.footer');
        const footerHTML = this.generateFooterHTML();
        
        if (existingFooter) {
            // Replace existing footer
            existingFooter.outerHTML = footerHTML;
        } else {
            // Create footer element and append to body
            const footerElement = document.createElement('div');
            footerElement.innerHTML = footerHTML;
            document.body.appendChild(footerElement.firstElementChild);
        }
    }
}

// Auto-initialize footer when script loads
new DynamicFooter();