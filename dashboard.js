// ========================================
// Challenge Triple A - Dashboard JavaScript
// ========================================

// === CONSOLE STYLING ===
const styles = {
    success: 'background:  #00d4aa; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;',
    error: 'background: #ef4444; color: white; padding:  3px 8px; border-radius: 3px; font-weight: bold;',
    info: 'background: #0ea5e9; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;',
    warning: 'background:  #fbbf24; color: #0a0e27; padding: 3px 8px; border-radius: 3px; font-weight: bold;',
    action: 'background: #8b5cf6; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;',
    text: 'color: #94a3b8; padding-left: 8px;'
};

// === LIVE CLOCK ===
function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    
    const clockElement = document.getElementById('liveClock');
    if (clockElement) {
        clockElement.textContent = `${hours}:${minutes}:${seconds}`;
    }
}

// Start clock
updateClock();
setInterval(updateClock, 1000);


// === ANIMATE PROGRESS BARS ===
function animateProgressBars() {
    // RAM progress bar
    const ramBar = document.querySelector('.progress-bar-fill');
    if (ramBar) {
        const width = ramBar.getAttribute('data-width');
        if (width) {
            setTimeout(() => {
                ramBar.style.width = width + '%';
            }, 100);
        }
    }
    
    // File progress bars
    const fileBars = document.querySelectorAll('.file-bar-fill');
    fileBars.forEach((bar, index) => {
        const width = bar.getAttribute('data-width');
        if (width) {
            setTimeout(() => {
                bar.style.width = width + '%';
            }, 200 + (index * 100)); // Stagger animation
        }
    });
}


// === REFRESH BUTTON ===
const refreshBtn = document.getElementById('refreshBtn');
if (refreshBtn) {
    refreshBtn.addEventListener('click', function() {
        // Add rotation animation
        const icon = this.querySelector('.refresh-icon');
        if (icon) {
            icon.style.transform = 'rotate(360deg)';
            icon.style.transition = 'transform 0.5s ease';
        }
        
        // Reload page
        setTimeout(() => {
            location.reload();
        }, 500);
    });
}


// === SMOOTH SCROLL NAVIGATION ===
const navLinks = document.querySelectorAll('.nav-link');

navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Remove active class from all links
        navLinks.forEach(l => l.classList.remove('active'));
        
        // Add active class to clicked link
        this.classList.add('active');
        
        // Get target section
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
            // Smooth scroll to section
            targetSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }
        
        // Close mobile menu if open
        if (window.innerWidth <= 768) {
            const sidebar = document.getElementById('sidebar');
            const menuToggle = document.getElementById('mobileMenuToggle');
            
            if (sidebar) sidebar.classList.remove('active');
            if (menuToggle) menuToggle.classList.remove('active');
        }
    });
});


// === MOBILE MENU TOGGLE ===
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const sidebar = document.getElementById('sidebar');

if (mobileMenuToggle && sidebar) {
    mobileMenuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('active');
        this.classList.toggle('active');
    });
}

// === HIGHLIGHT ACTIVE SECTION ON SCROLL ===
const sections = document.querySelectorAll('.section');

function highlightActiveSection() {
    let current = 'overview'; // Default to overview
    
    // Get scroll position
    const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
    
    // Check if we're at the bottom of the page
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    const isAtBottom = (scrollPosition + windowHeight) >= (documentHeight - 50);
    
    // If at bottom, highlight last section
    if (isAtBottom && sections.length > 0) {
        const lastSection = sections[sections.length - 1];
        current = lastSection.getAttribute('id');
    } else {
        // Normal scroll detection
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            const sectionBottom = sectionTop + sectionHeight;
            
            // Adjust offset for sticky header (100px)
            const offset = 150;
            
            // Check if section is in viewport
            if (scrollPosition >= (sectionTop - offset) && scrollPosition < (sectionBottom - offset)) {
                current = section.getAttribute('id');
            }
        });
    }
    
    // Update active link
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// Listen to scroll events (with throttling for performance)
let scrollTimeout;
window.addEventListener('scroll', () => {
    if (scrollTimeout) {
        window.cancelAnimationFrame(scrollTimeout);
    }
    
    scrollTimeout = window.requestAnimationFrame(() => {
        highlightActiveSection();
    });
});


// === CLOSE MOBILE MENU WHEN CLICKING OUTSIDE ===
document.addEventListener('click', function(event) {
    if (window.innerWidth <= 768) {
        const sidebar = document.getElementById('sidebar');
        const menuToggle = document.getElementById('mobileMenuToggle');
        
        // Check if click is outside sidebar and toggle button
        if (sidebar && menuToggle) {
            const isClickInsideSidebar = sidebar.contains(event.target);
            const isClickOnToggle = menuToggle.contains(event.target);
            
            if (!isClickInsideSidebar && !isClickOnToggle && sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
                menuToggle.classList.remove('active');
            }
        }
    }
});


// === INITIALIZE ON PAGE LOAD ===
document.addEventListener('DOMContentLoaded', function() {
    console.log(`%c SUCCESS %c${styles.text}Challenge Triple A Dashboard Loaded`, styles.success, styles.text);
    
    // Animate progress bars
    animateProgressBars();
    
    // Set initial active section
    highlightActiveSection();
});

// === SHOW MORE/LESS PROCESSES ===
const showMoreBtn = document.getElementById('showMoreBtn');
const showMoreContainer = document.getElementById('showMoreContainer');
const processPreview = document.getElementById('processPreview');
const allProcessesContainer = document.getElementById('allProcessesContainer');
const showLessBtn = document.getElementById('showLessBtn');

if (showMoreBtn && processPreview && allProcessesContainer && showLessBtn) {
    // Show all processes
    showMoreBtn.addEventListener('click', function() {
        // Hide preview with blur
        processPreview.style.display = 'none';
        
        // Hide "Show More" button
        showMoreContainer.style.display = 'none';
        
        // Show all processes container
        allProcessesContainer.style.display = 'block';
        
        // Show "Voir moins" button (IMPORTANT: use flex!)
        showLessBtn.style.display = 'flex';
        
        console.log(`%c SUCCESS %c${styles.text}All processes revealed successfully`, styles.success, styles.text);
    });
    
    // Hide all processes
    showLessBtn.addEventListener('click', function() {
        // Show preview with blur
        processPreview.style.display = 'block';
        
        // Show "Show More" button
        showMoreContainer.style.display = 'flex';
        
        // Hide all processes container
        allProcessesContainer.style.display = 'none';
        
        // Hide "Voir moins" button
        this.style.display = 'none';
        
        // Scroll back to processes section
        const processSection = document.getElementById('processes-section');
        if (processSection) {
            processSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        console.log(`%c SUCCESS %c${styles.text}Processes collapsed successfully`, styles.success, styles.text);
    });
}

// === CHRISTMAS THEME TOGGLE ===
const themeToggle = document.getElementById('themeToggle');
const snowflakes = document.getElementById('snowflakes');
const htmlElement = document.documentElement;

// Get theme icons
const defaultThemeIcon = document.querySelector('.theme-icon.default-theme');
const christmasThemeIcon = document.querySelector('.theme-icon.christmas-theme-icon');

// Check if Christmas theme is saved in localStorage
const savedTheme = localStorage.getItem('christmasTheme');
if (savedTheme === 'enabled') {
    enableChristmasTheme();
}

if (themeToggle) {
    themeToggle.addEventListener('click', function() {
        if (htmlElement.classList.contains('christmas-theme')) {
            disableChristmasTheme();
        } else {
            enableChristmasTheme();
        }
    });
}

function enableChristmasTheme() {
    htmlElement.classList.add('christmas-theme');
    
    // Show snowflakes
    if (snowflakes) {
        snowflakes.style.display = 'block';
    }
    
    // Toggle theme icons
    if (defaultThemeIcon && christmasThemeIcon) {
        defaultThemeIcon.style. display = 'none';
        christmasThemeIcon.style. display = 'block';
    }
    localStorage.setItem('christmasTheme', 'enabled');
    console.log(`%c SUCCESS %c${styles.text}🎄 Merry Christmas! Theme activated`, styles.success, styles.text);
}

function disableChristmasTheme() {
    htmlElement.classList.remove('christmas-theme');

    // Hide snowflakes
    if (snowflakes) {
        snowflakes.style.display = 'none';
    }

    // Toggle theme icons
    if (defaultThemeIcon && christmasThemeIcon) {
        defaultThemeIcon.style. display = 'block';
        christmasThemeIcon.style. display = 'none';
    }
    
    localStorage.setItem('christmasTheme', 'disabled');
    console.log(`%c INFO %c${styles.text}Christmas theme disabled`, styles.info, styles.text);
}