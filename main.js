/**
 * 3D Character AI - Main JavaScript
 * Handles all frontend interactions
 */

// ==========================================
// MOBILE MENU
// ==========================================

function toggleMobileMenu() {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
}

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    const nav = document.querySelector('.navbar');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.getElementById('navLinks');

    if (!nav.contains(e.target) && navLinks && navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
    }
});


// ==========================================
// PASSWORD TOGGLE
// ==========================================

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const button = input.nextElementSibling;
    const icon = button.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// ==========================================
// FLASH MESSAGES
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    const flashes = document.querySelectorAll('.flash');
    
    flashes.forEach(flash => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(100%)';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });
});

// ==========================================
// SMOOTH SCROLL
// ==========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ==========================================
// NAVBAR SCROLL EFFECT
// ==========================================

window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(15, 23, 42, 0.98)';
        navbar.style.backdropFilter = 'blur(20px)';
    } else {
        navbar.style.background = 'rgba(15, 23, 42, 0.8)';
    }
});

// ==========================================
// FORM VALIDATION
// ==========================================

document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
        const requiredFields = form.querySelectorAll('[required]');
        let valid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                valid = false;
                field.style.borderColor = 'var(--error)';
                
                // Shake animation
                field.animate([
                    { transform: 'translateX(0)' },
                    { transform: 'translateX(-10px)' },
                    { transform: 'translateX(10px)' },
                    { transform: 'translateX(0)' }
                ], {
                    duration: 300,
                    iterations: 1
                });
            } else {
                field.style.borderColor = '';
            }
        });

        if (!valid) {
            e.preventDefault();
            showToast('Please fill in all required fields', 'error');
        }
    });
});

// ==========================================
// INPUT FOCUS EFFECTS
// ==========================================

document.querySelectorAll('input, textarea').forEach(input => {
    input.addEventListener('focus', () => {
        input.parentElement?.classList.add('focused');
    });

    input.addEventListener('blur', () => {
        input.parentElement?.classList.remove('focused');
    });
});

// ==========================================
// PARALLAX EFFECT
// ==========================================

window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const orbs = document.querySelectorAll('.gradient-orb');

    orbs.forEach((orb, index) => {
        const speed = 0.5 + (index * 0.1);
        orb.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// ==========================================
// INTERSECTION OBSERVER FOR ANIMATIONS
// ==========================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.feature-card, .step, .stat-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ==========================================
// TOAST NOTIFICATIONS
// ==========================================

function showToast(message, type = 'info') {
    // Remove existing toasts
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Styles
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: var(--surface);
        color: var(--text);
        padding: 16px 24px;
        border-radius: 12px;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 3000;
        animation: slideIn 0.3s ease;
        font-weight: 500;
    `;
    
    // Type-specific styling
    if (type === 'success') {
        toast.style.borderLeft = '4px solid var(--success)';
    } else if (type === 'error') {
        toast.style.borderLeft = '4px solid var(--error)';
    } else if (type === 'warning') {
        toast.style.borderLeft = '4px solid var(--warning)';
    }

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ==========================================
// LOADING STATES
// ==========================================

document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn && !submitBtn.classList.contains('no-loading')) {
            submitBtn.disabled = true;
            submitBtn.dataset.originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        }
    });
});

// ==========================================
// CHARACTER COUNTER
// ==========================================

document.querySelectorAll('textarea[maxlength]').forEach(textarea => {
    const maxLength = textarea.getAttribute('maxlength');
    const counter = document.createElement('div');
    counter.className = 'char-counter';
    counter.innerHTML = `<span>0</span>/${maxLength}`;
    textarea.parentNode.appendChild(counter);

    textarea.addEventListener('input', () => {
        const remaining = textarea.value.length;
        counter.querySelector('span').textContent = remaining;
        
        if (remaining > maxLength * 0.9) {
            counter.style.color = 'var(--warning)';
        } else {
            counter.style.color = 'var(--text-dark)';
        }
    });
});

// ==========================================
// OTP INPUT AUTO-FOCUS
// ==========================================

const otpInput = document.getElementById('otp');
if (otpInput) {
    otpInput.addEventListener('input', function(e) {
        this.value = this.value.replace(/[^0-9]/g, '');
        
        // Auto-submit when 6 digits entered
        if (this.value.length === 6) {
            this.closest('form').submit();
        }
    });
    
    // Focus on load
    otpInput.focus();
}

// ==========================================
// UNSAVED CHANGES WARNING
// ==========================================

let formChanged = false;
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('change', () => formChanged = true);
    form.addEventListener('submit', () => formChanged = false);
});

window.addEventListener('beforeunload', (e) => {
    if (formChanged) {
        e.preventDefault();
        e.returnValue = '';
    }
});

// ==========================================
// GENERATION PAGE FUNCTIONS
// ==========================================

// These are defined in generate_3d.html but included here for reference
function setPrompt(text) {
    const input = document.getElementById('promptInput');
    if (input) input.value = text;
}

function clearPrompt() {
    const input = document.getElementById('promptInput');
    if (input) input.value = '';
}

function setRandomPrompt() {
    const prompts = [
        'a cute dragon with wings',
        'futuristic soldier with gun',
        'ancient stone temple',
        'robot companion character',
        'magical crystal sword',
        'steampunk airship',
        'cyberpunk street vendor',
        'medieval knight armor',
        'cute alien creature',
        'post-apocalyptic vehicle'
    ];
    const random = prompts[Math.floor(Math.random() * prompts.length)];
    setPrompt(random);
}

// ==========================================
// 3D MODEL DOWNLOAD FUNCTION (NEW - WORKING)
// ==========================================

/**
 * Download a 3D model file from the server
 * @param {string} url - The download URL (e.g., '/download-file/filename.glb')
 * @param {string} filename - Optional custom filename
 */
function downloadModelFile(url, filename) {
    if (!url) {
        showToast('No model to download!', 'error');
        return;
    }

    // Show loading toast
    showToast('Starting download...', 'info');

    // Use fetch to get the file as blob
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Download failed: ${response.status} ${response.statusText}`);
            }
            return response.blob();
        })
        .then(blob => {
            // Create blob URL
            const blobUrl = window.URL.createObjectURL(blob);
            
            // Extract filename from URL if not provided
            const downloadName = filename || url.split('/').pop() || 'model.glb';
            
            // Create temporary link element
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = downloadName;
            link.style.display = 'none';
            
            // Append to body, click, then remove
            document.body.appendChild(link);
            link.click();
            
            // Cleanup
            setTimeout(() => {
                document.body.removeChild(link);
                window.URL.revokeObjectURL(blobUrl);
            }, 100);
            
            showToast(`Downloaded: ${downloadName}`, 'success');
            console.log('✅ Downloaded:', downloadName);
        })
        .catch(error => {
            console.error('❌ Download error:', error);
            showToast('Download failed: ' + error.message, 'error');
            
            // Fallback: try direct download
            fallbackDownload(url, filename);
        });
}

/**
 * Fallback download method using direct link
 */
function fallbackDownload(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename || url.split('/').pop() || 'model.glb';
    link.target = '_blank'; // Open in new tab if download fails
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Trying alternative download...', 'warning');
}

/**
 * Legacy download function (for backward compatibility)
 */
function downloadModel() {
    // Try to get URL from global variable or data attribute
    const url = window.currentModelUrl || document.getElementById('downloadBtn')?.dataset?.url;
    downloadModelFile(url);
}

// ==========================================
// COPY TO CLIPBOARD
// ==========================================

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

// ==========================================
// KEYBOARD SHORTCUTS
// ==========================================

document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus search (if exists)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        const searchInput = document.querySelector('input[type="search"]');
        if (searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modal = document.querySelector('.modal.active');
        if (modal) modal.classList.remove('active');
    }
});

// ==========================================
// ANIMATION KEYFRAMES (injected via JS)
// ==========================================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

console.log('🎨 3D Character AI loaded successfully!');

// ==========================================
// GENERATE BUTTON HANDLERS
// ==========================================

// Handle generate form submission
document.addEventListener('DOMContentLoaded', () => {
    const generateForm = document.getElementById('generateForm');
    if (generateForm) {
        generateForm.addEventListener('submit', function(e) {
            const btn = document.getElementById('generateBtn');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
            }
        });
    }

    // Handle generate button click
    const generateBtn = document.getElementById('generateBtn');
    if (generateBtn) {
        generateBtn.addEventListener('click', function() {
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Please wait...';
        });
    }
});

// ==========================================
// CLEANED MAIN.JS - Remove old conflicting functions
// =========================================

console.log('🎨 3D Character AI loaded successfully!');

// Note: setPrompt, clearPrompt, setRandomPrompt, and download functions 
// are now defined directly in generate_3d.html to avoid scope issues

// Add this to your script for debugging
function debugDownload() {
    const btn = document.getElementById('downloadBtn');
    console.log('Button exists:', !!btn);
    console.log('Button display:', btn ? btn.style.display : 'N/A');
    console.log('data-url:', btn ? btn.getAttribute('data-url') : 'N/A');
    console.log('window.currentModelUrl:', window.currentModelUrl);
}