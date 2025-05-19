document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenu = document.getElementById('mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    
    mobileMenu.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        mobileMenu.innerHTML = navLinks.classList.contains('active') ? 
            '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
    });
    
    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    mobileMenu.innerHTML = '<i class="fas fa-bars"></i>';
                }
            }
        });
    });
    
    // Scroll down button
    document.getElementById('scroll-down').addEventListener('click', function() {
        window.scrollTo({
            top: document.getElementById('about').offsetTop - 70,
            behavior: 'smooth'
        });
    });
    
    // Typing effect
    const typedElement = document.getElementById('typed');
    const phrases = ['RoboKat', 'a Web Developer', 'a UI Designer', 'a Problem Solver'];
    let currentPhraseIndex = 0;
    let currentCharIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;
    
    function type() {
        const currentPhrase = phrases[currentPhraseIndex];
        
        if (isDeleting) {
            typedElement.textContent = currentPhrase.substring(0, currentCharIndex - 1);
            currentCharIndex--;
            typingSpeed = 50;
        } else {
            typedElement.textContent = currentPhrase.substring(0, currentCharIndex + 1);
            currentCharIndex++;
            typingSpeed = 100;
        }
        
        if (!isDeleting && currentCharIndex === currentPhrase.length) {
            isDeleting = true;
            typingSpeed = 1000; // Pause at end
        } else if (isDeleting && currentCharIndex === 0) {
            isDeleting = false;
            currentPhraseIndex = (currentPhraseIndex + 1) % phrases.length;
            typingSpeed = 500; // Pause before starting new word
        }
        
        setTimeout(type, typingSpeed);
    }
    
    setTimeout(type, 1000);
    
    // Skill cards expansion
    (function() {
        
        // Direct execution plus multiple event listeners for redundancy
        setupSkillCards();
        
        // Also set up on DOM content loaded
        document.addEventListener('DOMContentLoaded', setupSkillCards);  
        
        // And also on window load just to be absolutely sure
        window.addEventListener('load', setupSkillCards);
        
        function setupSkillCards() {
            const skillCards = document.querySelectorAll('.skill-card');
            
            skillCards.forEach(card => {
                // Remove any existing click listeners first
                const newCard = card.cloneNode(true);
                card.parentNode.replaceChild(newCard, card);
                
                // Add fresh click listener
                newCard.addEventListener('click', function(e) {
                    console.log("Card clicked: " + this.getAttribute('data-skill'));
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Toggle expanded class
                    this.classList.toggle('expanded');
                    
                    return false;
                });
            });
        }
    })();
    

});