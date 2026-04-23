/**
 * AnnaSetu User Profile Manager
 * Handles profile icon injection and user data modal with premium aesthetics.
 */
(function() {
    // Prevent double initialization
    if (window.__AnnaSetuProfileExecuted) return;
    window.__AnnaSetuProfileExecuted = true;

    // --- 1. Styles ---
    const profileStyles = `
        #annasetu-profile-modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        }

        #annasetu-profile-modal-overlay.open {
            opacity: 1;
            pointer-events: auto;
        }

        #annasetu-profile-modal {
            width: 460px;
            max-width: 95vw;
            background: #ffffff;
            border-radius: 40px;
            box-shadow: 0 40px 120px rgba(0, 0, 0, 0.25);
            overflow: hidden;
            transform: scale(0.8) translateY(40px);
            transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
        }

        .dark-mode #annasetu-profile-modal {
            background: #1e211e;
            border-color: rgba(255, 255, 255, 0.05);
            color: #e6e8e3;
        }

        #annasetu-profile-modal-overlay.open #annasetu-profile-modal {
            transform: scale(1) translateY(0);
        }

        .profile-banner {
            height: 120px;
            background: linear-gradient(135deg, #4a7c59, #78a886, #facc15);
            position: relative;
        }

        .profile-header-main {
            padding: 0 32px 32px;
            text-align: center;
            margin-top: -60px;
        }

        .profile-avatar-large {
            width: 120px;
            height: 120px;
            background: #ffffff;
            border-radius: 45px;
            margin: 0 auto 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #4a7c59;
            font-size: 52px;
            font-weight: 800;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border: 6px solid #ffffff;
            transition: transform 0.3s;
            font-family: 'Literata', serif;
        }
        
        .dark-mode .profile-avatar-large {
            background: #1e211e;
            border-color: #1e211e;
            color: #78a886;
        }

        .profile-name-tag {
            font-family: 'Literata', serif;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 4px;
            color: #121412;
        }
        
        .dark-mode .profile-name-tag { color: #e6e8e3; }

        .profile-role-badge {
            display: inline-flex;
            align-items: center;
            padding: 6px 14px;
            background: rgba(74, 124, 89, 0.1);
            color: #4a7c59;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            gap: 6px;
        }

        .profile-details-grid {
            padding: 0 32px 32px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .detail-card {
            background: #faf6f0;
            padding: 16px 20px;
            border-radius: 24px;
            display: flex;
            align-items: center;
            gap: 16px;
            transition: all 0.3s;
            border: 1px solid transparent;
        }
        
        .dark-mode .detail-card {
            background: #2a2e2a;
        }

        .detail-card:hover {
            transform: translateX(8px);
            background: #ffffff;
            border-color: rgba(74, 124, 89, 0.2);
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        }
        
        .dark-mode .detail-card:hover {
            background: #343a34;
            border-color: rgba(120, 168, 134, 0.2);
        }

        .detail-icon {
            width: 48px;
            height: 48px;
            background: #ffffff;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #4a7c59;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        
        .dark-mode .detail-icon {
            background: #1e211e;
            color: #78a886;
        }

        .detail-text {
            flex: 1;
        }

        .detail-label {
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            color: #94a3b8;
            letter-spacing: 0.05em;
            margin-bottom: 2px;
        }

        .detail-value {
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
        }
        
        .dark-mode .detail-value { color: #e6e8e3; }

        #profile-close-x {
            position: absolute;
            top: 24px;
            right: 24px;
            width: 40px;
            height: 40px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            color: white;
            z-index: 10;
            transition: all 0.3s;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        #profile-close-x:hover {
            background: rgba(255, 255, 255, 0.4);
            transform: rotate(90deg);
        }

        .profile-actions {
            padding: 0 32px 40px;
        }

        .btn-profile-done {
            width: 100%;
            padding: 16px;
            background: #4a7c59;
            color: white;
            border: none;
            border-radius: 20px;
            font-weight: 800;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 10px 25px rgba(74, 124, 89, 0.3);
        }

        .btn-profile-done:hover {
            background: #3d664a;
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(74, 124, 89, 0.4);
        }
        
        .cursor-pointer { cursor: pointer; }
    `;

    // --- 2. Inject Elements ---
    function initProfile() {
        const sessionData = localStorage.getItem('annasetu_session');
        const user = sessionData ? JSON.parse(sessionData) : null;

        if (!user) return; // Not logged in

        // Inject Styles
        const styleSheet = document.createElement("style");
        styleSheet.innerText = profileStyles;
        document.head.appendChild(styleSheet);

        // Set cursor pointer on existing profile circle
        const existingCircle = document.getElementById('user-initial');
        if (existingCircle) {
            existingCircle.classList.add('cursor-pointer');
            existingCircle.title = "View Profile";
            // Update initial if needed
            if (user.fname) {
                existingCircle.textContent = user.fname.charAt(0).toUpperCase();
            }
        }

        // Inject Modal Overlay
        const overlay = document.createElement('div');
        overlay.id = 'annasetu-profile-modal-overlay';
        overlay.innerHTML = `
            <div id="annasetu-profile-modal">
                <div id="profile-close-x">
                    <span class="material-symbols-outlined">close</span>
                </div>
                <div class="profile-banner"></div>
                <div class="profile-header-main">
                    <div class="profile-avatar-large">${user.fname ? user.fname.charAt(0).toUpperCase() : 'A'}</div>
                    <h2 class="profile-name-tag">${user.fname || 'User'} ${user.lname || ''}</h2>
                    <div class="profile-role-badge">
                        <span class="material-symbols-outlined" style="font-size:16px;">verified</span>
                        Verified ${user.role === 'restaurant' ? 'Restaurant' : 'NGO'} Partner
                    </div>
                </div>
                
                <div class="profile-details-grid">
                    <div class="detail-card">
                        <div class="detail-icon">
                            <span class="material-symbols-outlined">mail</span>
                        </div>
                        <div class="detail-text">
                            <div class="detail-label">Email Address</div>
                            <div class="detail-value">${user.email || 'Not provided'}</div>
                        </div>
                    </div>
                    
                    <div class="detail-card">
                        <div class="detail-icon">
                            <span class="material-symbols-outlined">badge</span>
                        </div>
                        <div class="detail-text">
                            <div class="detail-label">${user.role === 'restaurant' ? 'FSSAI License' : 'Registration No.'}</div>
                            <div class="detail-value">${user.regno || 'N/A'}</div>
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-icon">
                            <span class="material-symbols-outlined">history</span>
                        </div>
                        <div class="detail-text">
                            <div class="detail-label">Partner Since</div>
                            <div class="detail-value">April 2026</div>
                        </div>
                    </div>
                </div>
                
                <div class="profile-actions">
                    <button class="btn-profile-done" id="profile-done-btn">Dismiss</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        // --- 3. Events ---
        const triggers = [
            document.getElementById('profile-trigger'),
            document.getElementById('user-initial')
        ].filter(el => el !== null);

        const closeBtns = [
            document.getElementById('profile-close-x'),
            document.getElementById('profile-done-btn')
        ].filter(el => el !== null);

        triggers.forEach(trigger => {
            trigger.addEventListener('click', () => {
                overlay.classList.add('open');
                // Play subtle sound if desired or just animate
            });
        });

        closeBtns.forEach(btn => {
            btn.addEventListener('click', () => overlay.classList.remove('open'));
        });

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) overlay.classList.remove('open');
        });
        
        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && overlay.classList.contains('open')) {
                overlay.classList.remove('open');
            }
        });
    }

    // Run on boot
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initProfile);
    } else {
        initProfile();
    }
})();

