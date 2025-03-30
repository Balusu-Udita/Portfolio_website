document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const themeToggle = document.getElementById('theme-toggle');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const navItems = document.querySelectorAll('.nav-links li a');
    const skillProgressBars = document.querySelectorAll('.skill-progress');
    const flashMessages = document.querySelectorAll('.flash-message');
    const certificateCards = document.querySelectorAll('.certificate-card');
    const modalCloseButtons = document.querySelectorAll('.close-modal');
    const contactForm = document.getElementById('contact-form');
    const sections = document.querySelectorAll('section');
    
    // Initialize variables
    let isDarkMode = localStorage.getItem('darkMode') === 'true';
    
    // Apply dark mode if saved in local storage
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
    
    // Toggle dark/light mode
    themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        isDarkMode = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDarkMode);
        
        if (isDarkMode) {
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
    });
    
    // Mobile menu toggle
    mobileMenuBtn.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        if (navLinks.classList.contains('active')) {
            mobileMenuBtn.innerHTML = '<i class="fas fa-times"></i>';
        } else {
            mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        }
    });
    
    // Close mobile menu when clicking a nav link
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navLinks.classList.remove('active');
            mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Animate skill progress bars when in view
    const animateSkillBars = () => {
        skillProgressBars.forEach(bar => {
            const skillValue = bar.getAttribute('data-value');
            bar.style.width = skillValue;
        });
    };
    
    // Initialize IntersectionObserver for animations
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                
                // If skills section is visible, animate skill bars
                if (entry.target.id === 'skills') {
                    animateSkillBars();
                }
            }
        });
    }, { threshold: 0.2 });
    
    // Observe all sections for animations
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // Modal handling for certificates
    certificateCards.forEach(card => {
        card.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
            }
        });
    });
    
    // Close modals
    modalCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
    
    // Auto-dismiss flash messages
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 500);
            }, 5000);
        });
    }
    
    // Form validation
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const subjectInput = document.getElementById('subject');
            const messageInput = document.getElementById('message');
            let isValid = true;
            
            // Reset error messages
            document.querySelectorAll('.error-message').forEach(el => el.remove());
            
            // Validate name
            if (nameInput.value.trim() === '') {
                showError(nameInput, 'Please enter your name');
                isValid = false;
            }
            
            // Validate email
            if (emailInput.value.trim() === '') {
                showError(emailInput, 'Please enter your email');
                isValid = false;
            } else if (!isValidEmail(emailInput.value)) {
                showError(emailInput, 'Please enter a valid email address');
                isValid = false;
            }
            
            // Validate subject
            if (subjectInput.value.trim() === '') {
                showError(subjectInput, 'Please enter a subject');
                isValid = false;
            }
            
            // Validate message
            if (messageInput.value.trim() === '') {
                showError(messageInput, 'Please enter your message');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
    
    // Show error message function
    function showError(input, message) {
        const formGroup = input.parentElement;
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.style.color = 'red';
        errorElement.style.fontSize = '0.8rem';
        errorElement.style.marginTop = '5px';
        errorElement.textContent = message;
        formGroup.appendChild(errorElement);
        input.style.borderColor = 'red';
    }
    
    // Email validation function
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
    
    // Active nav link based on scroll position
    function setActiveNavLink() {
        const scrollPosition = window.scrollY;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navItems.forEach(item => {
                    item.classList.remove('active');
                    if (item.getAttribute('href') === `#${sectionId}`) {
                        item.classList.add('active');
                    }
                });
            }
        });
    }
    
    // Update active nav link on scroll
    window.addEventListener('scroll', setActiveNavLink);
    
    // Initial call to set active nav link
    setActiveNavLink();
    
    // Typing animation for home section
    const typewriterElement = document.querySelector('.typewriter');
    if (typewriterElement) {
        const words = ['Developer', 'Student', 'Programmer', 'Tech Enthusiast'];
        let wordIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typeDelay = 150;
        
        function typeWriter() {
            const currentWord = words[wordIndex];
            
            if (isDeleting) {
                typewriterElement.textContent = currentWord.substring(0, charIndex - 1);
                charIndex--;
                typeDelay = 80;
            } else {
                typewriterElement.textContent = currentWord.substring(0, charIndex + 1);
                charIndex++;
                typeDelay = 150;
            }
            
            if (!isDeleting && charIndex === currentWord.length) {
                isDeleting = true;
                typeDelay = 1000; // Pause at end of word
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                typeDelay = 500; // Pause before typing next word
            }
            
            setTimeout(typeWriter, typeDelay);
        }
        
        // Start typing animation
        setTimeout(typeWriter, 1000);
    }
});
