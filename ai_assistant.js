/**
 * AnnaSetu AI Support Assistant
 * A self-injecting component for the restaurant portal.
 */
(function() {
    // Prevent double initialization
    if (window.__AnnaSetuAssistantExecuted) return;
    window.__AnnaSetuAssistantExecuted = true;

    // --- 1. Styles ---
    const styles = `
        #annasetu-chat-container {
            position: fixed;
            bottom: 32px;
            right: 32px;
            z-index: 9999;
            font-family: 'Nunito Sans', sans-serif;
        }

        #annasetu-chat-bubble {
            width: 56px;
            height: 56px;
            background: #4a7c59;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 32px rgba(74, 124, 89, 0.3);
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        #annasetu-chat-bubble:hover {
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 12px 48px rgba(74, 124, 89, 0.4);
        }

        #annasetu-chat-window {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 380px;
            height: 600px;
            max-height: calc(100vh - 120px);
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 24px;
            box-shadow: 0 20px 80px rgba(0, 0, 0, 0.15);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transform: translateY(20px) scale(0.95);
            opacity: 0;
            pointer-events: none;
            transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
        }

        #annasetu-chat-window.open {
            transform: translateY(0) scale(1);
            opacity: 1;
            pointer-events: auto;
        }

        .dark #annasetu-chat-window {
            background: rgba(18, 22, 41, 0.95);
            border-color: rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 80px rgba(0, 0, 0, 0.5);
            color: #f1f5f9;
        }

        #annasetu-chat-header {
            padding: 24px;
            background: linear-gradient(135deg, #4a7c59, #3d664a);
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        #annasetu-chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            scroll-behavior: smooth;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .chat-msg {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.5;
            position: relative;
            animation: msg-appear 0.3s ease-out;
        }

        @keyframes msg-appear {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .chat-msg.bot {
            align-self: flex-start;
            background: #f1f5f9;
            color: #1e293b;
            border-bottom-left-radius: 4px;
        }

        .dark .chat-msg.bot {
            background: #1e243b;
            color: #f1f5f9;
        }

        .chat-msg.user {
            align-self: flex-end;
            background: #4a7c59;
            color: white;
            border-bottom-right-radius: 4px;
        }

        #annasetu-chat-input-container {
            padding: 16px 20px;
            border-top: 1px solid rgba(0, 0, 0, 0.05);
            display: flex;
            gap: 12px;
            background: white;
        }

        .dark #annasetu-chat-input-container {
            background: #121629;
            border-color: rgba(255, 255, 255, 0.05);
        }

        #annasetu-chat-input {
            flex: 1;
            padding: 12px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            font-size: 14px;
            resize: none;
            outline: none;
            transition: border-color 0.3s;
            background: transparent;
        }

        .dark #annasetu-chat-input {
            border-color: rgba(255, 255, 255, 0.2);
            color: white;
        }

        #annasetu-chat-input:focus {
            border-color: #4a7c59;
        }

        #annasetu-chat-send {
            width: 44px;
            height: 44px;
            background: #4a7c59;
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
        }

        #annasetu-chat-send:active {
            transform: scale(0.9);
        }

        .typing-indicator {
            display: flex;
            gap: 4px;
            padding-top: 4px;
        }

        .typing-dot {
            width: 6px;
            height: 6px;
            background: #94a3b8;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-4px); }
        }

        @media (max-width: 768px) {
            #annasetu-chat-container {
                bottom: 180px !important; /* Lift significantly above mobile bottom nav */
                right: 16px !important;
            }
        }

        @media (max-width: 480px) {
            #annasetu-chat-window {
                width: calc(100vw - 40px);
                right: -10px;
                height: calc(100vh - 100px);
            }
        }
    `;

    // --- 2. Inject Elements ---
    const container = document.createElement('div');
    container.id = 'annasetu-chat-container';
    container.innerHTML = `
        <style>${styles}</style>
        <div id="annasetu-chat-window">
            <div id="annasetu-chat-header">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        <span class="material-symbols-outlined">smart_toy</span>
                    </div>
                    <div>
                        <div style="font-weight: bold; font-size: 16px;">AnnaSetu Assistant</div>
                        <div style="font-size: 11px; opacity: 0.8; display: flex; align-items: center; gap: 4px;">
                            <span style="width: 6px; height: 6px; background: #4dfa6b; border-radius: 50%;"></span> Online
                        </div>
                    </div>
                </div>
                <button id="annasetu-chat-close" style="background: transparent; border: none; color: white; cursor: pointer;">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            <div id="annasetu-chat-messages">
                <div class="chat-msg bot">
                    Hello! I'm your AnnaSetu AI Assistant. How can I help you manage your food rescue operations today?
                </div>
            </div>
            <div id="annasetu-chat-input-container">
                <textarea id="annasetu-chat-input" placeholder="Type your question..." rows="1"></textarea>
                <button id="annasetu-chat-send">
                    <span class="material-symbols-outlined">send</span>
                </button>
            </div>
        </div>
        <div id="annasetu-chat-bubble">
            <span class="material-symbols-outlined" style="font-size: 28px;">chat_bubble</span>
        </div>
    `;
    document.body.appendChild(container);

    // --- 3. Interaction Logic ---
    const bubble = document.getElementById('annasetu-chat-bubble');
    const windowEl = document.getElementById('annasetu-chat-window');
    const closeBtn = document.getElementById('annasetu-chat-close');
    const sendBtn = document.getElementById('annasetu-chat-send');
    const input = document.getElementById('annasetu-chat-input');
    const messagesContainer = document.getElementById('annasetu-chat-messages');

    bubble.addEventListener('click', () => {
        windowEl.classList.toggle('open');
        if (windowEl.classList.contains('open')) input.focus();
    });

    closeBtn.addEventListener('click', () => {
        windowEl.classList.remove('open');
    });

    const addMessage = (text, sender) => {
        const msg = document.createElement('div');
        msg.className = `chat-msg ${sender}`;
        msg.textContent = text;
        messagesContainer.appendChild(msg);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    const showTypingIndicator = () => {
        const indicator = document.createElement('div');
        indicator.id = 'annasetu-typing';
        indicator.className = 'chat-msg bot';
        indicator.innerHTML = `
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        messagesContainer.appendChild(indicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return indicator;
    };

    const handleSend = () => {
        const text = input.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        input.value = '';
        input.style.height = 'auto';

        const indicator = showTypingIndicator();

        // Simulate "Backend" Delay
        setTimeout(() => {
            indicator.remove();
            const response = getAIResponse(text);
            addMessage(response, 'bot');
        }, 1000 + Math.random() * 1000);
    };

    sendBtn.addEventListener('click', handleSend);
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    // Auto-resize textarea
    input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = (input.scrollHeight) + 'px';
    });

    // --- 4. "Backend" Logic (AI Response Engine) ---
    function getAIResponse(query) {
        query = query.toLowerCase();
        
        // Context Awareness based on page title or content
        const pageTitle = document.title.toLowerCase();
        const isNGO = pageTitle.includes('ngo') || document.body.innerText.toLowerCase().includes('rescue coordination');

        if (query.includes('hello') || query.includes('hi')) {
            return isNGO 
                ? "Hello! I'm your NGO Operations Assistant. How can I help you coordinate rescues or manage volunteers today?"
                : "Hi there! I'm ready to help you with your AnnaSetu restaurant dashboard. What's on your mind?";
        }
        
        // NGO Specific Logic
        if (isNGO) {
            if (query.includes('dispatch') || query.includes('track') || query.includes('driver')) {
                return "In the Dispatch Dashboard, you can track live rescues and assign drivers to pending pickups. Would you like to see the current active routes?";
            }
            if (query.includes('alert') || query.includes('notification') || query.includes('pending')) {
                return "The Alert Management section shows all incoming surplus notifications from restaurants. You should prioritize alerts marked as 'Expiring Soon'.";
            }
            if (query.includes('volunteer') || query.includes('fleet') || query.includes('team')) {
                return "You can manage your fleet of 24 active volunteers in the Volunteer Fleet section. You can see their current status, location, and assigned tasks.";
            }
            if (query.includes('rescue') || query.includes('coordination') || query.includes('assign')) {
                return "Rescue Coordination is where you match surplus food with nearby hunger centers. Our AI suggests the most efficient pairings to minimize travel time.";
            }
            if (query.includes('impact') || query.includes('report') || query.includes('stats')) {
                return "Your impact reporting shows you've served over 12,500 meals this month! You can generate a full transparency report for your donors in the Impact section.";
            }
        }

        // Restaurant Specific Logic
        if (query.includes('impact') || query.includes('analytics') || query.includes('kg') || query.includes('saved')) {
            return "Based on your data, you've saved 2,840 kg of food this month, preventing 5.2 tons of CO2 emissions. Your impact is in the top 5% of local restaurants!";
        }
        
        if (query.includes('surplus') || query.includes('log') || query.includes('excess')) {
            return "You can log new surplus items in the 'Surplus Log' section. Don't forget to use our AI Food Scanner for faster logging and freshness estimation!";
        }
        
        if (query.includes('location') || query.includes('branch')) {
            return "You have 6 active locations registered. You can manage their individual inventory and staff access in the 'Locations' tab.";
        }
        
        if (query.includes('team') || query.includes('member') || query.includes('staff')) {
            return "You can add or remove team members and assign roles (Manager, Staff, Volunteer) in the 'Team' section.";
        }

        if (query.includes('report') || query.includes('download')) {
            return "You can download a comprehensive PDF or CSV impact report. It's great for your sustainability audits!";
        }

        if (query.includes('help') || query.includes('how to')) {
            return "I can help you navigate the portal, understand your operations, or guide you through tasks. Try asking about " + (isNGO ? "volunteer assignments" : "logging surplus") + ".";
        }

        // Generic fallback
        return "That's a great question! I'm here to help you optimize your food rescue operations. Is there something specific about the " + 
               (pageTitle.includes('dashboard') ? "current view" : "features") + " you'd like to explore?";
    }

})();
