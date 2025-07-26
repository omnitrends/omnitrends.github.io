# OmniTrends - Static Blogging Website

A beautiful, mobile-responsive static blogging website optimized for GitHub Pages, Google Discover, and AdSense approval.

## 🌟 Features

- **Mobile-First Design**: Fully responsive across all devices
- **SEO Optimized**: Meta tags, structured data, and semantic HTML
- **Google Discover Ready**: Optimized for Google's content discovery
- **AdSense Compatible**: Clean, fast-loading pages perfect for ads
- **Static Site**: No backend required, perfect for GitHub Pages
- **Modern Design**: Clean, professional aesthetic with smooth animations
- **Accessibility**: WCAG compliant with keyboard navigation support
- **Performance**: Optimized images, lazy loading, and minimal JavaScript

## 📁 Project Structure

```
omnitrends/
├── index.html              # Homepage
├── about.html              # About page
├── contact.html            # Contact page
├── privacy.html            # Privacy policy
├── robots.txt              # Search engine directives
├── sitemap.xml             # Site structure for search engines
├── css/
│   └── style.css           # Main stylesheet
├── js/
│   └── main.js             # JavaScript functionality
├── articles/
│   ├── *.html              # Article HTML files
│   └── *.md                # Article Markdown sources
└── images/
    └── *.jpg               # Article images (1200x630px)
```

## 🚀 Getting Started

### 1. Clone or Download
Download this repository to your local machine.

### 2. Add Images
Add your article images to the `images/` folder:
- Format: JPG
- Dimensions: 1200 x 630 pixels
- Naming: Use descriptive, SEO-friendly names

Required images:
- `ai-revolution-2024.jpg`
- `sustainable-living-guide.jpg`
- `remote-work-trends.jpg`
- `og-image.jpg` (default social sharing image)

### 3. Customize Content
- Update the site title, description, and branding
- Replace placeholder URLs with your actual GitHub Pages URL
- Add your Google AdSense code (when approved)
- Customize colors and fonts in `css/style.css`

### 4. Deploy to GitHub Pages
1. Create a new repository on GitHub
2. Upload all files to the repository
3. Go to Settings > Pages
4. Select "Deploy from a branch" and choose "main"
5. Your site will be available at `https://yourusername.github.io/repositoryname/`

## 📝 Adding New Articles

### Method 1: HTML Files
1. Create a new HTML file in the `articles/` folder
2. Use existing articles as templates
3. Update the sitemap.xml with the new article URL

### Method 2: Markdown Files
1. Create a new `.md` file in the `articles/` folder
2. Use the existing markdown files as templates
3. Convert to HTML when ready to publish

## 🎨 Customization

### Colors
Update CSS variables in `style.css`:
```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #64748b;
    --accent-color: #f59e0b;
    /* ... */
}
```

### Fonts
The site uses Inter font from Google Fonts. To change:
1. Update the Google Fonts link in HTML files
2. Update the `--font-family` variable in CSS

### Logo
Add your logo to the `images/` folder and update the navigation in HTML files.

## 📊 SEO & Analytics

### Google Search Console
1. Verify your site ownership
2. Submit your sitemap.xml
3. Monitor search performance

### Google Analytics
Add your Google Analytics code to all HTML files:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Google AdSense
1. Apply for AdSense approval
2. Add the AdSense code to HTML files
3. Place ad units where desired

## 🔧 Technical Features

- **Semantic HTML5**: Proper document structure
- **CSS Grid & Flexbox**: Modern layout techniques
- **Lazy Loading**: Images load as needed
- **Service Worker Ready**: Prepared for PWA features
- **Schema.org Markup**: Rich snippets for search engines
- **Open Graph Tags**: Social media sharing optimization
- **Mobile Navigation**: Hamburger menu for mobile devices
- **Reading Progress**: Progress bar for articles
- **Scroll to Top**: Smooth scrolling functionality

## 📱 Mobile Optimization

- Responsive design works on all screen sizes
- Touch-friendly navigation and buttons
- Optimized images for different screen densities
- Fast loading times on mobile networks
- Accessible tap targets (minimum 44px)

## ♿ Accessibility

- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader friendly
- High contrast mode support
- Skip to main content link
- Proper heading hierarchy
- Alt text for all images

## 🚀 Performance

- Optimized CSS and JavaScript
- Compressed images
- Minimal HTTP requests
- Lazy loading for images
- Efficient font loading
- Clean, semantic HTML

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📞 Support

If you have any questions or need help customizing the site, please open an issue or contact us through the website.

---

**Built with ❤️ for the blogging community**