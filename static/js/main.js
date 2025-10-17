// Main JavaScript for Repair Tracker

// Global variables
let currentUser = null;
let authToken = null;
let userSettings = null;


const CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'RUB': '₽',
    'GBP': '£',
    'JPY': '¥'
};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Check authentication
    checkAuthentication();
    
    // Set up global event listeners
    setupGlobalEventListeners();
    
    // Initialize logout functionality
    setupLogout();
    
    // Load user settings
    loadUserSettings();
}


function formatCurrency(amountCents, currency = null) {
    if (!currency) {
        currency = userSettings?.currency || 'USD';
    }
    
    const symbol = CURRENCY_SYMBOLS[currency] || '$';
    const amount = (amountCents / 100).toFixed(2);
    
    return `${symbol}${amount}`;
}

// Make functions globally available
window.formatCurrency = formatCurrency;
window.getCurrencySymbol = getCurrencySymbol;

function getCurrencySymbol(currency = null) {
    if (!currency) {
        currency = userSettings?.currency || 'USD';
    }
    return CURRENCY_SYMBOLS[currency] || '$';
}

function updateAllCurrencySymbols() {
    // Update currency symbols on all pages
    const currencyElements = document.querySelectorAll('#currency-symbol');
    const symbol = getCurrencySymbol();
    
    currencyElements.forEach(element => {
        element.textContent = symbol;
    });
}

// Load user settings
async function loadUserSettings() {
    if (!authToken) return;
    
    try {
        const response = await fetch('/api/profile/settings', {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            userSettings = await response.json();
            console.log('User settings loaded:', userSettings);
            
            // Make settings available globally
            window.userSettings = userSettings;
            
            // Update currency symbols on all pages
            updateAllCurrencySymbols();
        }
    } catch (error) {
        console.error('Error loading user settings:', error);
    }
}

// Listen for settings updates from other pages
window.addEventListener('settingsUpdated', function(event) {
    console.log('Settings updated event received:', event.detail);
    if (event.detail && event.detail.settings) {
        userSettings = event.detail.settings;
        window.userSettings = userSettings;
        updateAllCurrencySymbols();
    }
});

// Listen for localStorage changes
window.addEventListener('storage', function(e) {
    if (e.key === 'userSettings') {
        console.log('Settings changed in localStorage, updating...');
        try {
            const newSettings = JSON.parse(e.newValue);
            userSettings = newSettings;
            window.userSettings = newSettings;
            updateAllCurrencySymbols();
        } catch (error) {
            console.error('Error parsing settings from localStorage:', error);
        }
    }
});

function checkAuthentication() {
    authToken = localStorage.getItem('access_token');
    
    if (authToken) {
        // Verify token is still valid
        verifyToken();
    } else {
        // Show auth buttons
        showAuthButtons();
    }
}

async function verifyToken() {
    try {
        const response = await fetch('/auth/me', {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            currentUser = await response.json();
            showUserInfo();
        } else {
            // Token is invalid
            localStorage.removeItem('access_token');
            authToken = null;
            showAuthButtons();
        }
    } catch (error) {
        console.error('Error verifying token:', error);
        localStorage.removeItem('access_token');
        authToken = null;
        showAuthButtons();
    }
}

function showUserInfo() {
    if (!currentUser) return;
    
    const userInfo = document.getElementById('user-info');
    const authButtons = document.getElementById('auth-buttons');
    const userName = document.getElementById('user-name');
    
    if (userInfo && authButtons && userName) {
        userName.textContent = currentUser.name || currentUser.email;
        userInfo.classList.remove('hidden');
        authButtons.classList.add('hidden');
    }
}

function showAuthButtons() {
    const userInfo = document.getElementById('user-info');
    const authButtons = document.getElementById('auth-buttons');
    
    if (userInfo && authButtons) {
        userInfo.classList.add('hidden');
        authButtons.classList.remove('hidden');
    }
}

function setupGlobalEventListeners() {
    // Add any global event listeners here
    document.addEventListener('click', function(e) {
        // Handle any global click events
        if (e.target.matches('[data-action="logout"]')) {
            logout();
        }
    });
}

function setupLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
}

function logout() {
    localStorage.removeItem('access_token');
    authToken = null;
    currentUser = null;
    showAuthButtons();
    window.location.href = '/login';
}

// Utility functions
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

function showError(message) {
    showNotification(message, 'error');
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showWarning(message) {
    showNotification(message, 'warning');
}

// API helper functions
async function apiRequest(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(url, mergedOptions);
        
        if (response.status === 401) {
            // Unauthorized - redirect to login
            localStorage.removeItem('access_token');
            window.location.href = '/login';
            return null;
        }
        
        return response;
    } catch (error) {
        console.error('API request error:', error);
        throw error;
    }
}

// Form validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password && password.length >= 6;
}

function validateRequired(value) {
    return value && value.trim().length > 0;
}

// Date formatting helpers
function formatDate(dateString) {
    const date = new Date(dateString);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${day}.${month}.${year} ${hours}:${minutes}`;
}

function formatCurrency(cents) {
    return `$${(cents / 100).toFixed(2)}`;
}

// Loading state helpers
function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="spinner"></div>';
    }
}

function hideLoading(element, content) {
    if (element) {
        element.innerHTML = content || '';
    }
}

// Confirmation dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Export functions for use in templates
window.RepairTracker = {
    showNotification,
    showError,
    showSuccess,
    showWarning,
    apiRequest,
    validateEmail,
    validatePassword,
    validateRequired,
    formatDate,
    formatDateTime,
    formatCurrency,
    showLoading,
    hideLoading,
    confirmAction,
    logout
};

