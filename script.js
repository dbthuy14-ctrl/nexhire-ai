document.addEventListener('DOMContentLoaded', () => {
    // ---- Navbar Scroll Effect ----
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ---- Smooth Scrolling for Anchor Links ----
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // ---- Scroll Animations via Intersection Observer ----
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Removed unobserve so animations keep triggering or stay triggered if desired.
                // Re-triggering elements is important when switching views
            }
        });
    }, observerOptions);

    const observeElements = () => {
        const fadeElements = document.querySelectorAll('.fade-in-up');
        fadeElements.forEach(el => {
            el.classList.remove('visible'); // Reset on re-observation
            observer.observe(el);
        });
    };
    
    // Initial observation
    observeElements();

    // ---- Portal Toggle Logic ----
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    const portalViews = document.querySelectorAll('.portal-view');
    const toggleContainer = document.querySelector('.portal-toggle');
    const navCtaBtn = document.getElementById('nav-cta-btn');

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state on buttons
            toggleBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const targetId = btn.getAttribute('data-target');
            
            // Adjust slider visuals
            if (targetId === 'candidate-portal') {
                toggleContainer.classList.add('candidate-active');
                navCtaBtn.textContent = 'Join as Talent';
                navCtaBtn.style.background = '#0ea5e9'; // Set nav primary to sky
                navCtaBtn.style.color = 'white';
            } else {
                toggleContainer.classList.remove('candidate-active');
                navCtaBtn.textContent = 'Start Hiring';
                navCtaBtn.style.background = 'var(--text-primary)'; // Reset to original
                navCtaBtn.style.color = 'var(--bg-main)';
            }

            // Swap view visibility
            portalViews.forEach(view => {
                view.classList.remove('active');
            });
            document.getElementById(targetId).classList.add('active');
            
            // Re-trigger scroll animations within the newly active view
            observeElements();
        });
    });

    // ---- Payment Modal Functionality (Simulated) ----
    const paymentBtns = document.querySelectorAll('.payment-btn');
    const modal = document.getElementById('payment-modal');
    const closeModal = document.querySelector('.close-modal');
    const modalPlanDesc = document.getElementById('modal-plan-desc');
    const modalPrice = document.getElementById('modal-price');
    const payBtn = document.querySelector('.stripe-pay-btn');

    const planDetails = {
        starter: {
            desc: "NexHire AI • Starter Plan (One-time)",
            price: "$299.00"
        },
        pro: {
            desc: "NexHire AI • Pro Plan (Annual Subscription)",
            price: "$1,490.00 / yr"
        }
    };

    paymentBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const plan = btn.getAttribute('data-plan');
            if (planDetails[plan]) {
                modalPlanDesc.textContent = planDetails[plan].desc;
                modalPrice.textContent = planDetails[plan].price;
            }
            modal.style.visibility = 'visible';
            modal.style.opacity = '1';
            
            setTimeout(() => {
                modal.classList.add('active');
            }, 10);
        });
    });

    const closePaymentModal = () => {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.style.opacity = '0';
            modal.style.visibility = 'hidden';
            payBtn.innerHTML = '<i class="fa-solid fa-lock"></i> Pay ' + modalPrice.textContent;
            payBtn.disabled = false;
        }, 300);
    };

    if(closeModal) closeModal.addEventListener('click', closePaymentModal);

    // Mock Payment Submit
    if(payBtn) {
        payBtn.addEventListener('click', (e) => {
            e.preventDefault();
            payBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
            payBtn.disabled = true;

            setTimeout(() => {
                payBtn.innerHTML = '<i class="fa-solid fa-check"></i> Payment Successful!';
                payBtn.style.background = '#10b981'; // Success Green
                
                setTimeout(() => {
                    closePaymentModal();
                    setTimeout(() => {
                        payBtn.style.background = '#635bff';
                    }, 300);
                }, 2000);
            }, 1500);
        });
    }

    // ---- Candidate Signup Modal ----
    const applicantBtns = document.querySelectorAll('.applicant-btn');
    const candidateModal = document.getElementById('candidate-modal');
    const closeCandidateModalBtn = document.querySelector('.close-candidate-modal');

    applicantBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            candidateModal.style.visibility = 'visible';
            candidateModal.style.opacity = '1';
            setTimeout(() => {
                candidateModal.classList.add('active');
            }, 10);
        });
    });

    const closeCandidateModal = () => {
        candidateModal.classList.remove('active');
        setTimeout(() => {
            candidateModal.style.opacity = '0';
            candidateModal.style.visibility = 'hidden';
        }, 300);
    };

    if(closeCandidateModalBtn) closeCandidateModalBtn.addEventListener('click', closeCandidateModal);

    // Close Modals when clicking outside content
    window.addEventListener('click', (e) => {
        if (e.target === modal) closePaymentModal();
        if (e.target === candidateModal) closeCandidateModal();
    });

    // ---- Mobile Menu Toggle ----
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    let menuOpen = false;
    mobileMenuBtn.addEventListener('click', () => {
        menuOpen = !menuOpen;
        if (menuOpen) {
            navLinks.style.display = 'flex';
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '100%';
            navLinks.style.left = '0';
            navLinks.style.width = '100%';
            navLinks.style.background = 'rgba(9, 9, 11, 0.95)';
            navLinks.style.backdropFilter = 'blur(10px)';
            navLinks.style.padding = '2rem';
            navLinks.style.borderBottom = '1px solid rgba(255,255,255,0.08)';
            mobileMenuBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
        } else {
            navLinks.style.display = '';
            mobileMenuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
        }
    });
});

// ---- MVP Chatbot Logic ----
async function sendChatMessage() {
    const input = document.getElementById('chatbot-input-field');
    const messages = document.getElementById('chatbot-messages');
    if (!input || !input.value.trim()) return;

    const userText = input.value.trim();
    // Add user bubble
    messages.innerHTML += `<div class="chat-bubble user">${userText}</div>`;
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    // Add thinking bubble
    const aiBubble = document.createElement('div');
    aiBubble.className = 'chat-bubble ai';
    aiBubble.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Thinking...';
    messages.appendChild(aiBubble);
    messages.scrollTop = messages.scrollHeight;

    try {
        const res = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userText })
        });
        const data = await res.json();
        aiBubble.innerHTML = data.reply || "I am currently disconnected. Please check the backend.";
    } catch (err) {
        aiBubble.innerHTML = "Ah! Connection issue to the AI brain.";
    }
    messages.scrollTop = messages.scrollHeight;
}
// Add enter key support
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chatbot-input-field');
    if (chatInput) {
        chatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') sendChatMessage();
        });
    }
});
