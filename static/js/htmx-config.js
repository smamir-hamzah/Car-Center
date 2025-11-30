/**
 * HTMX Configuration and Utilities
 * Handles auto-refresh, loading states, and error handling
 */

// Configure HTMX globally
document.addEventListener('DOMContentLoaded', function () {

    // Prevent auto-refresh when user is typing in forms
    document.body.addEventListener('htmx:beforeRequest', function (event) {
        // Check if any input, textarea, or select is focused
        const activeElement = document.activeElement;
        if (activeElement && (
            activeElement.tagName === 'INPUT' ||
            activeElement.tagName === 'TEXTAREA' ||
            activeElement.tagName === 'SELECT'
        )) {
            // Cancel the auto-refresh request if user is interacting with a form
            if (event.detail.elt.hasAttribute('hx-trigger') &&
                event.detail.elt.getAttribute('hx-trigger').includes('every')) {
                event.preventDefault();
                console.log('Auto-refresh paused: user is filling a form');
            }
        }
    });

    // Add loading indicator
    document.body.addEventListener('htmx:beforeRequest', function (event) {
        // Only show loading for manual requests, not auto-refresh
        if (!event.detail.elt.getAttribute('hx-trigger')?.includes('every')) {
            showLoadingIndicator();
        }
    });

    document.body.addEventListener('htmx:afterRequest', function (event) {
        hideLoadingIndicator();
    });

    // Handle errors
    document.body.addEventListener('htmx:responseError', function (event) {
        console.error('HTMX request failed:', event.detail);
        hideLoadingIndicator();
        // Don't show error for auto-refresh failures
        if (!event.detail.elt.getAttribute('hx-trigger')?.includes('every')) {
            showErrorMessage('Failed to load content. Please try again.');
        }
    });

    // Preserve scroll position on auto-refresh
    let scrollPosition = 0;
    document.body.addEventListener('htmx:beforeSwap', function (event) {
        if (event.detail.elt.hasAttribute('hx-trigger') &&
            event.detail.elt.getAttribute('hx-trigger').includes('every')) {
            scrollPosition = window.scrollY;
        }
    });

    document.body.addEventListener('htmx:afterSwap', function (event) {
        if (event.detail.elt.hasAttribute('hx-trigger') &&
            event.detail.elt.getAttribute('hx-trigger').includes('every')) {
            window.scrollTo(0, scrollPosition);
        }
    });
});

// Loading indicator functions
function showLoadingIndicator() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('hidden');
    }
}

function hideLoadingIndicator() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('hidden');
    }
}

// Error message display
function showErrorMessage(message) {
    // Create a temporary error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        font-weight: 600;
    `;
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);

    // Remove after 5 seconds
    setTimeout(() => {
        errorDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
