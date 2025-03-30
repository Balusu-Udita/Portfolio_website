document.addEventListener('DOMContentLoaded', function() {
    // Canvas setup for home animation
    const homeSection = document.getElementById('home');
    if (homeSection) {
        const canvas = document.createElement('canvas');
        canvas.id = 'animation-canvas';
        canvas.style.position = 'absolute';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.zIndex = '1';
        canvas.style.pointerEvents = 'none';
        canvas.style.opacity = '0.6';
        
        homeSection.appendChild(canvas);
        
        // Initialize canvas
        const ctx = canvas.getContext('2d');
        
        // Set canvas dimensions
        function resizeCanvas() {
            canvas.width = homeSection.clientWidth;
            canvas.height = homeSection.clientHeight;
        }
        
        // Resize canvas initially and on window resize
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        // Particle class
        class Particle {
            constructor(canvas, isDarkMode) {
                this.canvas = canvas;
                this.ctx = canvas.getContext('2d');
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 5 + 1;
                this.speedX = Math.random() * 3 - 1.5;
                this.speedY = Math.random() * 3 - 1.5;
                this.isDarkMode = isDarkMode;
                this.color = this.getColor();
            }
            
            getColor() {
                const darkModeColors = [
                    'rgba(109, 131, 255, 0.7)', // primary
                    'rgba(80, 214, 201, 0.6)', // secondary
                    'rgba(255, 200, 41, 0.5)'  // accent
                ];
                
                const lightModeColors = [
                    'rgba(74, 99, 231, 0.5)', // primary
                    'rgba(51, 180, 166, 0.4)', // secondary
                    'rgba(255, 187, 0, 0.3)'  // accent
                ];
                
                const colors = this.isDarkMode ? darkModeColors : lightModeColors;
                return colors[Math.floor(Math.random() * colors.length)];
            }
            
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                
                // Bounce off edges
                if (this.x < 0 || this.x > this.canvas.width) {
                    this.speedX = -this.speedX;
                }
                
                if (this.y < 0 || this.y > this.canvas.height) {
                    this.speedY = -this.speedY;
                }
                
                // Update color if dark mode changes
                if (this.isDarkMode !== document.body.classList.contains('dark-mode')) {
                    this.isDarkMode = !this.isDarkMode;
                    this.color = this.getColor();
                }
            }
            
            draw() {
                this.ctx.fillStyle = this.color;
                this.ctx.beginPath();
                this.ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                this.ctx.fill();
            }
        }
        
        // Create particles
        const particles = [];
        const particleCount = Math.min(Math.floor(canvas.width * canvas.height / 15000), 100);
        
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle(canvas, document.body.classList.contains('dark-mode')));
        }
        
        // Draw lines between particles
        function drawLines(particles, threshold, ctx) {
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < threshold) {
                        const opacity = 1 - distance / threshold;
                        ctx.strokeStyle = document.body.classList.contains('dark-mode') 
                            ? `rgba(109, 131, 255, ${opacity * 0.2})` 
                            : `rgba(74, 99, 231, ${opacity * 0.15})`;
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
        }
        
        // Animation loop
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Update and draw particles
            particles.forEach(particle => {
                particle.update();
                particle.draw();
            });
            
            // Draw connecting lines
            const threshold = Math.min(canvas.width, canvas.height) * 0.12;
            drawLines(particles, threshold, ctx);
            
            requestAnimationFrame(animate);
        }
        
        // Start animation
        animate();
        
        // Interactive effect - particles follow cursor
        homeSection.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            
            particles.forEach(particle => {
                const dx = mouseX - particle.x;
                const dy = mouseY - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    const angle = Math.atan2(dy, dx);
                    const force = 0.5 * (1 - distance / 150);
                    
                    particle.speedX += Math.cos(angle) * force;
                    particle.speedY += Math.sin(angle) * force;
                    
                    // Limit speed
                    const speed = Math.sqrt(particle.speedX * particle.speedX + particle.speedY * particle.speedY);
                    if (speed > 3) {
                        particle.speedX = (particle.speedX / speed) * 3;
                        particle.speedY = (particle.speedY / speed) * 3;
                    }
                }
            });
        });
    }
});
