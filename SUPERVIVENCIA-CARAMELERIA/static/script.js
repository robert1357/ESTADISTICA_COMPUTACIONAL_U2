// Game state management and UI enhancements
class GameUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFormValidation();
        this.addAnimations();
    }

    setupEventListeners() {
        // Auto-dismiss alerts after 5 seconds
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            setTimeout(() => {
                if (alert.classList.contains('show')) {
                    alert.classList.remove('show');
                    setTimeout(() => alert.remove(), 300);
                }
            }, 5000);
        });

        // Add click effects to buttons
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('click', this.handleButtonClick.bind(this));
        });

        // Setup form validation for the candy exchange
        this.setupCandyExchangeValidation();
    }

    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        });
    }

    setupCandyExchangeValidation() {
        const candyForm = document.querySelector('form[action*="intercambio_caramelo"]');
        if (!candyForm) return;

        const selects = candyForm.querySelectorAll('select');
        const submitBtn = candyForm.querySelector('button[type="submit"]');

        selects.forEach(select => {
            select.addEventListener('change', () => {
                this.validateCandyExchange(selects, submitBtn);
            });
        });
    }

    validateCandyExchange(selects, submitBtn) {
        const values = Array.from(selects).map(select => parseInt(select.value) || 0);
        const total = values.reduce((sum, val) => sum + val, 0);
        
        const isValid = total === 3;
        const feedback = document.getElementById('candy-feedback') || this.createFeedbackElement();
        
        if (total === 0) {
            feedback.textContent = 'Selecciona los pares que quieres recibir';
            feedback.className = 'text-muted small';
        } else if (total < 3) {
            feedback.textContent = `Necesitas ${3 - total} par(es) más`;
            feedback.className = 'text-warning small';
        } else if (total > 3) {
            feedback.textContent = `Tienes ${total - 3} par(es) de más`;
            feedback.className = 'text-danger small';
        } else {
            feedback.textContent = '¡Perfecto! 3 pares seleccionados';
            feedback.className = 'text-success small';
        }

        // Update submit button state
        if (submitBtn && !submitBtn.disabled) {
            submitBtn.style.opacity = isValid ? '1' : '0.7';
        }
    }

    createFeedbackElement() {
        const feedback = document.createElement('div');
        feedback.id = 'candy-feedback';
        feedback.className = 'text-muted small mt-2';
        
        const candyForm = document.querySelector('form[action*="intercambio_caramelo"]');
        if (candyForm) {
            const lastSelect = candyForm.querySelector('select:last-of-type');
            if (lastSelect && lastSelect.parentNode) {
                lastSelect.parentNode.appendChild(feedback);
            }
        }
        
        return feedback;
    }

    handleButtonClick(event) {
        const button = event.target;
        
        // Add click animation
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = '';
        }, 150);

        // Add loading state for form submissions
        if (button.type === 'submit') {
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
                button.disabled = true;
            }, 100);
        }
    }

    handleFormSubmit(event) {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // Validate main exchange form
        if (form.action.includes('intercambio_principal')) {
            const objeto1 = form.querySelector('select[name="objeto1"]');
            const objeto2 = form.querySelector('select[name="objeto2"]');
            
            if (!objeto1.value || !objeto2.value) {
                event.preventDefault();
                this.showTempMessage('Debes seleccionar ambos objetos', 'error');
                return;
            }
        }

        // Validate candy exchange form
        if (form.action.includes('intercambio_caramelo')) {
            const selects = form.querySelectorAll('select');
            const total = Array.from(selects)
                .map(select => parseInt(select.value) || 0)
                .reduce((sum, val) => sum + val, 0);
            
            if (total !== 3) {
                event.preventDefault();
                this.showTempMessage('Debes seleccionar exactamente 3 pares', 'error');
                return;
            }
        }

        // Show success animation
        this.showSuccessAnimation(form);
    }

    showTempMessage(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container-fluid');
        const firstRow = container.querySelector('.row');
        container.insertBefore(alertDiv, firstRow);
        
        // Auto-dismiss
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }

    showSuccessAnimation(form) {
        const card = form.closest('.card');
        if (card) {
            card.classList.add('trade-success');
            setTimeout(() => {
                card.classList.remove('trade-success');
            }, 1000);
        }
    }

    addAnimations() {
        // Add fade-in animation to cards
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

        // Add pulse animation to inventory items with high counts
        const inventoryItems = document.querySelectorAll('.inventory-item');
        inventoryItems.forEach(item => {
            const countElement = item.querySelector('.item-count');
            if (countElement && parseInt(countElement.textContent) > 10) {
                item.classList.add('pulse');
            }
        });
    }

    // Utility method to update inventory display
    updateInventoryDisplay(newState) {
        const inventoryItems = document.querySelectorAll('.inventory-item');
        inventoryItems.forEach(item => {
            const itemName = item.querySelector('.item-name').textContent.toLowerCase();
            const countElement = item.querySelector('.item-count');
            
            if (newState[itemName] !== undefined) {
                countElement.textContent = newState[itemName];
                
                // Add animation for updated values
                countElement.style.transform = 'scale(1.2)';
                countElement.style.color = '#28a745';
                
                setTimeout(() => {
                    countElement.style.transform = 'scale(1)';
                    countElement.style.color = '';
                }, 300);
            }
        });
    }
}

// Initialize game UI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const gameUI = new GameUI();
    
    // Add some fun easter eggs
    let clickCount = 0;
    const header = document.querySelector('header h1');
    
    if (header) {
        header.addEventListener('click', () => {
            clickCount++;
            if (clickCount === 5) {
                header.style.animation = 'pulse 1s ease-in-out';
                setTimeout(() => {
                    header.style.animation = '';
                }, 1000);
                clickCount = 0;
            }
        });
    }
});

// Add keyboard shortcuts for power users
document.addEventListener('keydown', (event) => {
    if (event.ctrlKey || event.metaKey) {
        switch(event.key) {
            case 'r':
                event.preventDefault();
                window.location.href = '/reset';
                break;
            case '1':
                event.preventDefault();
                const mainTradeBtn = document.querySelector('form[action*="intercambio_principal"] button[type="submit"]');
                if (mainTradeBtn && !mainTradeBtn.disabled) {
                    mainTradeBtn.click();
                }
                break;
            case '2':
                event.preventDefault();
                const candyTradeBtn = document.querySelector('form[action*="intercambio_caramelo"] button[type="submit"]');
                if (candyTradeBtn && !candyTradeBtn.disabled) {
                    candyTradeBtn.click();
                }
                break;
        }
    }
});
