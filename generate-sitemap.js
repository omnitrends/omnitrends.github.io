// generate-sitemap.js
const fs = require('fs');
const path = require('path');

const DOMAIN = 'https://omnitrends.github.io';
const TODAY = new Date().toISOString().slice(0, 10);

// Function to get file modification date
function getFileModDate(filePath) {
  try {
    const stats = fs.statSync(filePath);
    return stats.mtime.toISOString().slice(0, 10);
  } catch (error) {
    return TODAY;
  }
}

// Function to scan directory for HTML files
function scanDirectory(dir, baseDir = '') {
  const urls = [];
  
  try {
    const files = fs.readdirSync(dir);
    
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory()) {
        // Skip hidden directories and node_modules
        if (!file.startsWith('.') && file !== 'node_modules') {
          urls.push(...scanDirectory(filePath, path.join(baseDir, file)));
        }
      } else if (file.endsWith('.html')) {
        const relativePath = path.join(baseDir, file);
        const urlPath = relativePath.replace(/\\/g, '/').replace(/index\.html$/, '');
        const lastmod = getFileModDate(filePath);
        
        urls.push({
          loc: urlPath,
          lastmod: lastmod,
          changefreq: getChangeFreq(relativePath),
          priority: getPriority(relativePath)
        });
      }
    }
  } catch (error) {
    console.error(`Error scanning directory ${dir}:`, error.message);
  }
  
  return urls;
}

// Function to determine change frequency based on file type
function getChangeFreq(filePath) {
  if (filePath === 'index.html') return 'daily';
  if (filePath.startsWith('articles/') || filePath.startsWith('articles\\')) return 'weekly';
  if (filePath.startsWith('category/') || filePath.startsWith('category\\')) return 'weekly';
  if (filePath.startsWith('pages/') || filePath.startsWith('pages\\')) return 'monthly';
  return 'monthly';
}

// Function to determine priority based on file type
function getPriority(filePath) {
  if (filePath === 'index.html') return '1.0';
  if (filePath.startsWith('articles/') || filePath.startsWith('articles\\')) return '0.8';
  if (filePath.startsWith('category/') || filePath.startsWith('category\\')) return '0.7';
  if (filePath.startsWith('pages/') || filePath.startsWith('pages\\')) return '0.6';
  return '0.5';
}

// Generate sitemap
function generateSitemap() {
  console.log('🔍 Scanning website structure...');
  
  const urls = scanDirectory('.');
  
  // Sort URLs by priority (highest first) and then alphabetically
  urls.sort((a, b) => {
    const priorityDiff = parseFloat(b.priority) - parseFloat(a.priority);
    if (priorityDiff !== 0) return priorityDiff;
    return a.loc.localeCompare(b.loc);
  });
  
  console.log(`📄 Found ${urls.length} pages`);
  
  // Generate XML
  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  xml += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;
  
  urls.forEach(url => {
    const fullUrl = url.loc === '' ? DOMAIN : `${DOMAIN}/${url.loc}`;
    xml += `  <url>\n`;
    xml += `    <loc>${fullUrl}</loc>\n`;
    xml += `    <lastmod>${url.lastmod}</lastmod>\n`;
    xml += `    <changefreq>${url.changefreq}</changefreq>\n`;
    xml += `    <priority>${url.priority}</priority>\n`;
    xml += `  </url>\n`;
  });
  
  xml += `</urlset>\n`;
  
  // Write sitemap
  fs.writeFileSync('sitemap.xml', xml);
  
  console.log('✅ sitemap.xml generated successfully!');
  console.log(`📊 Statistics:`);
  console.log(`   - Total URLs: ${urls.length}`);
  console.log(`   - Homepage: ${urls.filter(u => u.priority === '1.0').length}`);
  console.log(`   - Articles: ${urls.filter(u => u.priority === '0.8').length}`);
  console.log(`   - Categories: ${urls.filter(u => u.priority === '0.7').length}`);
  console.log(`   - Pages: ${urls.filter(u => u.priority === '0.6').length}`);
  console.log(`   - Other: ${urls.filter(u => u.priority === '0.5').length}`);
}

// Run the generator
generateSitemap();