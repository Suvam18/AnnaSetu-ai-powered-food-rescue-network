/**
 * AnnaSetu User Profile Manager
 * Handles profile icon injection and user data modal.
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
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(8px);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
        }

        #annasetu-profile-modal-overlay.open {
            opacity: 1;
            pointer-events: auto;
        }

        #annasetu-profile-modal {
            width: 440px;
            max-width: 90vw;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 32px;
            box-shadow: 0 40px 100px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            transform: scale(0.9) translateY(20px);
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        #annasetu-profile-modal-overlay.open #annasetu-profile-modal {
            transform: scale(1) translateY(0);
        }

        .dark #annasetu-profile-modal {
            background: rgba(18, 22, 41, 0.95);
            border-color: rgba(255, 255, 255, 0.1);
            color: #f1f5f9;
        }

        .profile-header {
            padding: 40px 32px 24px;
            text-align: center;
            background: linear-gradient(135deg, rgba(74, 124, 89, 0.1), rgba(250, 204, 21, 0.05));
            position: relative;
        }

        .profile-avatar {
            width: 90px;
            height: 90px;
            background: linear-gradient(135deg, #4a7c59, #facc15);
            border-radius: 30px;
            margin: 0 auto 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 40px;
            font-weight: 800;
            box-shadow: 0 15px 30px rgba(74, 124, 89, 0.3);
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .profile-info-row {
            padding: 16px 32px;
            display: flex;
            align-items: flex-start;
            gap: 16px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        }

        .dark .profile-info-row {
            border-bottom-color: rgba(255, 255, 255, 0.05);
        }

        .profile-info-row:last-child {
            border-bottom: none;
        }

        .profile-label {
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #94a3b8;
            margin-bottom: 4px;
        }

        .profile-value {
            font-size: 15px;
            font-weight: 600;
            color: #1e293b;
        }

        .dark .profile-value {
            color: #f1f5f9;
        }

        .profile-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            background: #4a7c591a;
            color: #4a7c59;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 700;
            margin-top: 8px;
        }

        #profile-close-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        #profile-close-btn:hover {
            background: rgba(0,0,0,0.1);
            transform: rotate(90deg);
        }

        .profile-footer {
            padding: 24px 32px 32px;
            display: flex;
            gap: 12px;
        }

        .btn-profile-primary {
            flex: 1;
            padding: 12px;
            background: #4a7c59;
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-profile-primary:hover {
            background: #3d664a;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(74, 124, 89, 0.2);
        }
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

        // Inject Icon into Navbar
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            const initial = user.fname ? user.fname.charAt(0).toUpperCase() : 'A';
            const profileIconHtml = `
                <button id="profile-trigger" class="w-10 h-10 rounded-full bg-indigo-500 text-white flex items-center justify-center font-bold text-lg hover:scale-105 active:scale-95 transition-all shadow-md">
                    <span>${initial}</span>
                </button>
            `;
            themeToggle.insertAdjacentHTML('beforebegin', profileIconHtml);
        }

        // Inject Modal Overlay
        const overlay = document.createElement('div');
        overlay.id = 'annasetu-profile-modal-overlay';
        overlay.innerHTML = `
            <div id="annasetu-profile-modal">
                <div class="profile-header">
                    <div id="profile-close-btn">
                        <span class="material-symbols-outlined text-[20px]">close</span>
                    </div>
                    <div class="profile-avatar">${user.fname ? user.fname.charAt(0) : 'A'}</div>
                    <h2 class="text-2xl font-bold font-['Literata']">${user.fname || 'User Name'}</h2>
                    <div class="profile-badge">
                        <span class="material-symbols-outlined text-[14px] mr-1">verified</span>
                        Verified ${user.role === 'restaurant' ? 'Restaurant' : 'NGO'} Partner
                    </div>
                </div>
                <div class="profile-content">
                    <div class="profile-info-row">
                        <span class="material-symbols-outlined text-stone-400">person</span>
                        <div>
                            <div class="profile-label">Contact Person</div>
                            <div class="profile-value">${user.lname || 'Not provided'}</div>
                        </div>
                    </div>
                    <div class="profile-info-row">
                        <span class="material-symbols-outlined text-stone-400">mail</span>
                        <div>
                            <div class="profile-label">Email Address</div>
                            <div class="profile-value">${user.email || 'Not provided'}</div>
                        </div>
                    </div>
                    <div class="profile-info-row">
                        <span class="material-symbols-outlined text-stone-400">badge</span>
                        <div>
                            <div class="profile-label">${user.role === 'restaurant' ? 'FSSAI License' : 'Registration No.'}</div>
                            <div class="profile-value">${user.regno || 'N/A'}</div>
                        </div>
                    </div>
                </div>
                <div class="profile-footer">
                    <button class="btn-profile-primary" onclick="this.closest('#annasetu-profile-modal-overlay').classList.remove('open')">Done</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        // --- 3. Events ---
        const trigger = document.getElementById('profile-trigger');
        const closeBtn = document.getElementById('profile-close-btn');

        if (trigger) {
            trigger.addEventListener('click', () => overlay.classList.add('open'));
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', () => overlay.classList.remove('open'));
        }

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) overlay.classList.remove('open');
        });
    }

    // Run on boot
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initProfile);
    } else {
        initProfile();
    }
})();
