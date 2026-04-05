/**
 * Session Timeout Logic with Glassmorphism Lock Screen
 */
(function() {
    'use strict';

    // Configuration from data attribute on body or default to 5 minutes
    const body = document.querySelector('body');
    const timeoutMinutes = parseInt(body.getAttribute('data-session-timeout')) || 5;
    const timeoutMs = timeoutMinutes * 60 * 1000;
    
    let inactivityTimer;
    const lockScreen = document.getElementById('lock-screen-overlay');
    const lockForm = document.getElementById('lock-form');
    const lockPasswordInput = document.getElementById('lock-password');
    const lockErrorMsg = document.getElementById('lock-error-msg');
    const unlockBtn = document.getElementById('unlock-btn');

    // Check if session is already locked on page load
    const isLocked = localStorage.getItem('isSessionLocked') === 'true';
    if (isLocked) {
        showLockScreen();
    }

    /**
     * Resets the inactivity timer on user activity
     */
    function resetTimer() {
        if (!localStorage.getItem('isSessionLocked')) {
            clearTimeout(inactivityTimer);
            inactivityTimer = setTimeout(showLockScreen, timeoutMs);
            
            // Sync last activity timestamp across tabs
            localStorage.setItem('lastActivity', Date.now());
        }
    }

    /**
     * Displays the lock screen
     */
    function showLockScreen() {
        if (lockScreen && !lockScreen.classList.contains('active')) {
            lockScreen.style.display = 'flex';
            setTimeout(() => {
                lockScreen.classList.add('active');
            }, 10);
            localStorage.setItem('isSessionLocked', 'true');
            lockPasswordInput.focus();
        }
    }

    /**
     * Hides the lock screen
     */
    function hideLockScreen() {
        if (lockScreen) {
            lockScreen.classList.remove('active');
            setTimeout(() => {
                lockScreen.style.display = 'none';
                lockPasswordInput.value = '';
                lockErrorMsg.style.display = 'none';
            }, 400);
            localStorage.removeItem('isSessionLocked');
            resetTimer();
        }
    }

    /**
     * AJAX Password Verification
     */
    async function verifyPassword(password) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const submitBtn = unlockBtn;
        const btnText = submitBtn.querySelector('.btn-text');
        const spinner = submitBtn.querySelector('.spinner-border');

        // Loading state
        btnText.classList.add('d-none');
        spinner.classList.remove('d-none');
        submitBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('password', password);
            formData.append('csrfmiddlewaretoken', csrfToken);

            const response = await fetch('/api/verify-password/', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                hideLockScreen();
            } else {
                showError(data.message || 'Mot de passe incorrect.');
            }
        } catch (error) {
            showError('Une erreur de connexion est survenue.');
            console.error('Lock screen error:', error);
        } finally {
            btnText.classList.remove('d-none');
            spinner.classList.add('d-none');
            submitBtn.disabled = false;
        }
    }

    function showError(msg) {
        lockErrorMsg.innerText = msg;
        lockErrorMsg.style.display = 'block';
        lockPasswordInput.classList.add('is-invalid');
        // Shake animation
        lockForm.classList.add('shake');
        setTimeout(() => lockForm.classList.remove('shake'), 500);
    }

    // Events to reset the timer
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
    events.forEach(eventName => {
        document.addEventListener(eventName, resetTimer, true);
    });

    // Forms handling
    if (lockForm) {
        lockForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const password = lockPasswordInput.value;
            if (password) {
                verifyPassword(password);
            }
        });
    }

    // Listen for storage changes (to sync across tabs)
    window.addEventListener('storage', (e) => {
        if (e.key === 'isSessionLocked') {
            if (e.newValue === 'true') {
                showLockScreen();
            } else {
                hideLockScreen();
            }
        }
        if (e.key === 'lastActivity' && !localStorage.getItem('isSessionLocked')) {
            clearTimeout(inactivityTimer);
            const timeSinceLastActivity = Date.now() - parseInt(e.newValue);
            const remaining = Math.max(0, timeoutMs - timeSinceLastActivity);
            inactivityTimer = setTimeout(showLockScreen, remaining);
        }
    });

    // Initialize timer
    resetTimer();

})();
