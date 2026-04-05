/**
 * Session Lock Mechanism
 * Handles inactivity tracking, lock screen display, and cross-tab synchronization.
 */

class SessionLock {
    constructor(config) {
        this.timeoutMinutes = config.timeoutMinutes || 0;
        this.unlockUrl = config.unlockUrl;
        this.isLocked = false;
        this.lastActivityTime = Date.now();
        this.warningVisible = false;
        this.timer = null;

        this.overlay = document.getElementById('lock-screen-overlay');
        this.warningOverlay = document.getElementById('lock-warning-overlay');
        this.countdownEl = document.getElementById('lock-countdown');
        this.form = document.getElementById('lock-form');
        this.passwordInput = document.getElementById('lock-password');
        this.errorMsg = document.getElementById('lock-error-msg');
        this.unlockBtn = document.getElementById('unlock-btn');

        this.init();
    }

    init() {
        if (!this.overlay) return;

        // Check initial state from localStorage
        if (localStorage.getItem('session_locked') === 'true') {
            this.lock();
        }

        // Start inactivity timer
        this.resetTimer();
        this.startInactivityTimer();

        // Event listeners for activity
        const activityEvents = ['mousemove', 'mousedown', 'keypress', 'touchmove', 'scroll'];
        activityEvents.forEach(evt => {
            window.addEventListener(evt, () => this.resetTimer(), { passive: true });
        });

        // Form submission
        if (this.form) {
            this.form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleUnlock();
            });
        }

        // Cross-tab synchronization
        window.addEventListener('storage', (e) => {
            if (e.key === 'session_locked') {
                if (e.newValue === 'true') {
                    this.lock();
                } else {
                    this.unlock();
                }
            }
        });
    }

    startInactivityTimer() {
        this.timer = setInterval(() => {
            if (this.isLocked) return;

            const now = Date.now();
            const elapsed = now - this.lastActivityTime;
            const timeoutMs = (this.timeoutMinutes * 60 * 1000);
            
            console.log(`[SessionLock Debug] Mins: ${this.timeoutMinutes}, TotalMs: ${timeoutMs}, Elapsed: ${elapsed}`);
            
            if (timeoutMs === 0) return; // If timeout is 0, don't lock
            
            const remaining = timeoutMs - elapsed;
            
            console.log(`[SessionLock Debug] Remaining: ${remaining} (WarningVisible: ${this.warningVisible})`);

            if (remaining <= 0) {
                if (this.warningVisible) this.hideWarning();
                setTimeout(() => this.lock(), 100);
            } else if (remaining <= 10000) {
                this.showWarning(Math.ceil(remaining / 1000));
            } else if (this.warningVisible) {
                this.hideWarning();
            }
        }, 1000);
    }

    resetTimer() {
        this.lastActivityTime = Date.now();
        if (this.warningVisible) {
            this.hideWarning();
        }
    }

    showWarning(seconds) {
        this.warningVisible = true;
        if (this.warningOverlay) {
            this.warningOverlay.classList.remove('d-none');
        }
        if (this.countdownEl) {
            this.countdownEl.textContent = seconds;
        }
        const circle = document.querySelector('.countdown-circle-progress');
        if (circle) {
            const dasharray = 283;
            const dashoffset = dasharray * ((10 - seconds) / 10);
            circle.style.strokeDashoffset = dashoffset;
        }
    }

    hideWarning() {
        this.warningVisible = false;
        if (this.warningOverlay) {
            this.warningOverlay.classList.add('d-none');
        }
    }

    lock() {
        if (this.isLocked) return;
        
        this.isLocked = true;
        this.overlay.classList.remove('d-none');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
        localStorage.setItem('session_locked', 'true');
        
        // Clear password input
        if (this.passwordInput) this.passwordInput.value = '';
        if (this.errorMsg) this.errorMsg.classList.add('d-none');
    }

    unlock() {
        this.isLocked = false;
        this.overlay.classList.add('d-none');
        document.body.style.overflow = ''; 
        localStorage.setItem('session_locked', 'false');
        this.resetTimer();
    }

    async handleUnlock() {
        const password = this.passwordInput.value;
        if (!password) return;

        // UI Feedback
        this.setLoading(true);
        this.errorMsg.classList.add('d-none');

        try {
            const response = await fetch(this.unlockUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: `password=${encodeURIComponent(password)}`
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.unlock();
            } else {
                this.errorMsg.classList.remove('d-none');
                this.passwordInput.value = '';
                this.passwordInput.focus();
            }
        } catch (error) {
            console.error('Unlock error:', error);
            alert('Une erreur est survenue lors du déverrouillage.');
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(isLoading) {
        if (!this.unlockBtn) return;
        const text = this.unlockBtn.querySelector('.btn-text');
        const spinner = this.unlockBtn.querySelector('.spinner-border');

        if (isLoading) {
            text.classList.add('d-none');
            spinner.classList.remove('d-none');
            this.unlockBtn.disabled = true;
        } else {
            text.classList.remove('d-none');
            spinner.classList.add('d-none');
            this.unlockBtn.disabled = false;
        }
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    // These values should be provided by the global_config context processor
    if (window.sessionTimeoutEnabled === false) return; // Feature is disabled
    
    const timeout = parseInt(window.sessionTimeoutCount) || 0; 
    
    if (timeout === 0) return; // Don't run lock logic if it is 0
    
    window.sessionLock = new SessionLock({
        timeoutMinutes: timeout,
        unlockUrl: '/api/verify-password/'
    });
});
