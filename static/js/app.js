// Disease Prediction System - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeSymptomForm();
    initializeAnimations();
    initializeAccessibility();
});

function initializeSymptomForm() {
    const form = document.getElementById('symptomForm');
    if (!form) return;

    // Add form validation
    form.addEventListener('submit', function(e) {
        const checkedSymptoms = form.querySelectorAll('input[name="symptoms"]:checked');
        
        if (checkedSymptoms.length === 0) {
            e.preventDefault();
            showAlert('Please select at least one symptom before submitting.', 'warning');
            return false;
        }

        // Show loading state
        showLoadingState(true);
        
        // Optional: Add a small delay to show loading animation
        setTimeout(() => {
            // Form will submit naturally
        }, 100);
    });

    // Add symptom counter
    updateSymptomCounter();
    
    // Listen for checkbox changes
    const checkboxes = form.querySelectorAll('input[name="symptoms"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateSymptomCounter();
            highlightCheckedSymptom(this);
        });
    });
}

function clearForm() {
    const form = document.getElementById('symptomForm');
    if (!form) return;
    
    const checkboxes = form.querySelectorAll('input[name="symptoms"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
        const parent = checkbox.closest('.form-check');
        parent.classList.remove('selected-symptom');
    });
    
    updateSymptomCounter();
    showAlert('All symptoms cleared.', 'info');
}

function updateSymptomCounter() {
    const form = document.getElementById('symptomForm');
    if (!form) return;
    
    const checkedSymptoms = form.querySelectorAll('input[name="symptoms"]:checked');
    const count = checkedSymptoms.length;
    
    // Update or create counter badge
    let counter = document.getElementById('symptom-counter');
    if (!counter) {
        counter = document.createElement('span');
        counter.id = 'symptom-counter';
        counter.className = 'badge bg-info ms-2';
        
        const header = document.querySelector('.card-header h4');
        if (header) {
            header.appendChild(counter);
        }
    }
    
    if (count > 0) {
        counter.textContent = `${count} selected`;
        counter.style.display = 'inline';
    } else {
        counter.style.display = 'none';
    }
}

function highlightCheckedSymptom(checkbox) {
    const parent = checkbox.closest('.form-check');
    if (checkbox.checked) {
        parent.classList.add('selected-symptom');
        // Add a subtle animation
        parent.style.transform = 'scale(1.02)';
        setTimeout(() => {
            parent.style.transform = '';
        }, 150);
    } else {
        parent.classList.remove('selected-symptom');
    }
}

function showLoadingState(show) {
    const form = document.getElementById('symptomForm');
    const submitButton = form?.querySelector('button[type="submit"]');
    
    if (!form || !submitButton) return;
    
    if (show) {
        form.classList.add('form-loading');
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    } else {
        form.classList.remove('form-loading');
        submitButton.disabled = false;
        submitButton.innerHTML = '<i class="fas fa-search me-2"></i>Predict Disease';
    }
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    
    const icon = getAlertIcon(type);
    alertDiv.innerHTML = `
        <i class="fas fa-${icon} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at top of main content
    const main = document.querySelector('main');
    const container = main?.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv && alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

function getAlertIcon(type) {
    const icons = {
        'info': 'info-circle',
        'warning': 'exclamation-triangle',
        'danger': 'exclamation-circle',
        'success': 'check-circle'
    };
    return icons[type] || 'info-circle';
}

function initializeAnimations() {
    // Animate progress bars on results page
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
    
    // Animate cards on page load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

function initializeAccessibility() {
    // Add keyboard navigation for custom elements
    const checkboxContainers = document.querySelectorAll('.form-check');
    checkboxContainers.forEach(container => {
        container.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const checkbox = container.querySelector('input[type="checkbox"]');
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                    checkbox.dispatchEvent(new Event('change'));
                }
            }
        });
        
        // Make containers focusable
        container.setAttribute('tabindex', '0');
    });
    
    // Add ARIA labels for better screen reader support
    const form = document.getElementById('symptomForm');
    if (form) {
        form.setAttribute('aria-label', 'Symptom selection form');
    }
    
    // Update ARIA live region for symptom counter
    const counter = document.getElementById('symptom-counter');
    if (counter) {
        counter.setAttribute('aria-live', 'polite');
    }
}

// Utility function to format confidence percentage
function formatConfidence(confidence) {
    return Math.round(confidence * 100);
}

// Add smooth scrolling for anchor links
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

// Add print functionality improvements
function preparePrintView() {
    // Hide unnecessary elements before printing
    const elementsToHide = document.querySelectorAll('.btn, .navbar, footer, .alert');
    elementsToHide.forEach(el => {
        el.style.display = 'none';
    });
    
    // Ensure content is visible
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.breakInside = 'avoid';
    });
}

// Listen for print events
window.addEventListener('beforeprint', preparePrintView);

window.addEventListener('afterprint', function() {
    // Restore hidden elements after printing
    location.reload(); // Simple way to restore all elements
});

// Add error handling for network issues
window.addEventListener('online', function() {
    showAlert('Connection restored.', 'success');
});

window.addEventListener('offline', function() {
    showAlert('You are currently offline. Some features may not work properly.', 'warning');
});

// Initialize tooltips if Bootstrap is available
if (typeof bootstrap !== 'undefined') {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}
