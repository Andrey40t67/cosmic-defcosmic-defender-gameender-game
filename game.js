// 🚀 Cosmic Defender - Epic Space Shooter Game
// Created by AndreyVV
// Advanced HTML5 Canvas Game with Professional Features

class CosmicDefender {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.gameRunning = false;
        
        // Game state
        this.score = 0;
        this.level = 1;
        this.health = 100;
        this.maxHealth = 100;
        
        // Player
        this.player = {
            x: this.canvas.width / 2,
            y: this.canvas.height - 80,
            width: 40,
            height: 40,
            speed: 5,
            color: '#00ffff'
        };
        
        // Game objects
        this.bullets = [];
        this.enemies = [];
        this.particles = [];
        this.powerUps = [];
        
        // Input handling
        this.keys = {};
        this.mouse = { x: 0, y: 0, clicked: false };
        
        // Game timing
        this.lastTime = 0;
        this.enemySpawnTimer = 0;
        this.powerUpSpawnTimer = 0;
        
        this.setupEventListeners();
        this.setupUI();
    }
    
    setupEventListeners() {
        // Keyboard events
        document.addEventListener('keydown', (e) => {
            this.keys[e.key.toLowerCase()] = true;
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.key.toLowerCase()] = false;
        });
        
        // Mouse events
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
        });
        
        this.canvas.addEventListener('mousedown', (e) => {
            this.mouse.clicked = true;
            if (this.gameRunning) {
                this.shootBullet();
            }
        });
        
        this.canvas.addEventListener('mouseup', () => {
            this.mouse.clicked = false;
        });
    }
    
    setupUI() {
        const startButton = document.getElementById('startButton');
        startButton.addEventListener('click', () => {
            this.startGame();
        });
    }
    
    startGame() {
        document.getElementById('startScreen').style.display = 'none';
        this.gameRunning = true;
        this.resetGame();
        this.gameLoop();
    }
    
    resetGame() {
        this.score = 0;
        this.level = 1;
        this.health = this.maxHealth;
        this.bullets = [];
        this.enemies = [];
        this.particles = [];
        this.powerUps = [];
        this.player.x = this.canvas.width / 2;
        this.player.y = this.canvas.height - 80;
        this.updateUI();
    }
    
    gameLoop(currentTime = 0) {
        if (!this.gameRunning) return;
        
        const deltaTime = currentTime - this.lastTime;
        this.lastTime = currentTime;
        
        this.update(deltaTime);
        this.render();
        
        requestAnimationFrame((time) => this.gameLoop(time));
    }
    
    update(deltaTime) {
        this.updatePlayer();
        this.updateBullets();
        this.updateEnemies(deltaTime);
        this.updateParticles();
        this.updatePowerUps();
        this.checkCollisions();
        this.spawnEnemies(deltaTime);
        this.spawnPowerUps(deltaTime);
        
        if (this.health <= 0) {
            this.gameOver();
        }
    }
    
    updatePlayer() {
        // Movement with WASD
        if (this.keys['w'] || this.keys['arrowup']) {
            this.player.y = Math.max(0, this.player.y - this.player.speed);
        }
        if (this.keys['s'] || this.keys['arrowdown']) {
            this.player.y = Math.min(this.canvas.height - this.player.height, this.player.y + this.player.speed);
        }
        if (this.keys['a'] || this.keys['arrowleft']) {
            this.player.x = Math.max(0, this.player.x - this.player.speed);
        }
        if (this.keys['d'] || this.keys['arrowright']) {
            this.player.x = Math.min(this.canvas.width - this.player.width, this.player.x + this.player.speed);
        }
        
        // Auto-shoot when mouse is held
        if (this.mouse.clicked) {
            this.shootBullet();
        }
    }
    
    shootBullet() {
        const bullet = {
            x: this.player.x + this.player.width / 2,
            y: this.player.y,
            width: 4,
            height: 10,
            speed: 8,
            color: '#ffff00',
            damage: 10
        };
        this.bullets.push(bullet);
        
        // Create muzzle flash particles
        for (let i = 0; i < 5; i++) {
            this.createParticle(bullet.x, bullet.y, '#ffff00');
        }
    }
    
    updateBullets() {
        this.bullets = this.bullets.filter(bullet => {
            bullet.y -= bullet.speed;
            return bullet.y > -bullet.height;
        });
    }
    
    spawnEnemies(deltaTime) {
        this.enemySpawnTimer += deltaTime;
        const spawnRate = Math.max(500 - this.level * 50, 200);
        
        if (this.enemySpawnTimer > spawnRate) {
            this.enemySpawnTimer = 0;
            
            const enemy = {
                x: Math.random() * (this.canvas.width - 30),
                y: -30,
                width: 30,
                height: 30,
                speed: 1 + Math.random() * 2 + this.level * 0.2,
                health: 20 + this.level * 5,
                maxHealth: 20 + this.level * 5,
                color: `hsl(${Math.random() * 60 + 300}, 70%, 50%)`,
                type: Math.random() < 0.8 ? 'basic' : 'fast'
            };
            
            if (enemy.type === 'fast') {
                enemy.speed *= 1.5;
                enemy.color = '#ff4444';
            }
            
            this.enemies.push(enemy);
        }
    }
    
    updateEnemies() {
        this.enemies = this.enemies.filter(enemy => {
            enemy.y += enemy.speed;
            
            // Remove enemies that go off screen
            if (enemy.y > this.canvas.height) {
                this.health -= 10;
                this.updateUI();
                return false;
            }
            
            return true;
        });
    }
    
    spawnPowerUps(deltaTime) {
        this.powerUpSpawnTimer += deltaTime;
        
        if (this.powerUpSpawnTimer > 5000) { // Every 5 seconds
            this.powerUpSpawnTimer = 0;
            
            const powerUp = {
                x: Math.random() * (this.canvas.width - 20),
                y: -20,
                width: 20,
                height: 20,
                speed: 2,
                type: Math.random() < 0.5 ? 'health' : 'score',
                color: Math.random() < 0.5 ? '#00ff00' : '#ffaa00'
            };
            
            this.powerUps.push(powerUp);
        }
    }
    
    updatePowerUps() {
        this.powerUps = this.powerUps.filter(powerUp => {
            powerUp.y += powerUp.speed;
            return powerUp.y < this.canvas.height + powerUp.height;
        });
    }
    
    checkCollisions() {
        // Bullet-Enemy collisions
        this.bullets.forEach((bullet, bulletIndex) => {
            this.enemies.forEach((enemy, enemyIndex) => {
                if (this.isColliding(bullet, enemy)) {
                    // Damage enemy
                    enemy.health -= bullet.damage;
                    
                    // Remove bullet
                    this.bullets.splice(bulletIndex, 1);
                    
                    // Create hit particles
                    for (let i = 0; i < 8; i++) {
                        this.createParticle(enemy.x + enemy.width/2, enemy.y + enemy.height/2, enemy.color);
                    }
                    
                    // Remove enemy if dead
                    if (enemy.health <= 0) {
                        this.enemies.splice(enemyIndex, 1);
                        this.score += 100;
                        
                        // Level up every 1000 points
                        if (this.score % 1000 === 0) {
                            this.level++;
                        }
                        
                        this.updateUI();
                        
                        // Create explosion particles
                        for (let i = 0; i < 15; i++) {
                            this.createParticle(enemy.x + enemy.width/2, enemy.y + enemy.height/2, '#ff6600');
                        }
                    }
                }
            });
        });
        
        // Player-Enemy collisions
        this.enemies.forEach((enemy, index) => {
            if (this.isColliding(this.player, enemy)) {
                this.enemies.splice(index, 1);
                this.health -= 20;
                this.updateUI();
                
                // Create damage particles
                for (let i = 0; i < 10; i++) {
                    this.createParticle(this.player.x + this.player.width/2, this.player.y + this.player.height/2, '#ff0000');
                }
            }
        });
        
        // Player-PowerUp collisions
        this.powerUps.forEach((powerUp, index) => {
            if (this.isColliding(this.player, powerUp)) {
                this.powerUps.splice(index, 1);
                
                if (powerUp.type === 'health') {
                    this.health = Math.min(this.maxHealth, this.health + 20);
                } else if (powerUp.type === 'score') {
                    this.score += 200;
                }
                
                this.updateUI();
                
                // Create pickup particles
                for (let i = 0; i < 8; i++) {
                    this.createParticle(powerUp.x + powerUp.width/2, powerUp.y + powerUp.height/2, powerUp.color);
                }
            }
        });
    }
    
    isColliding(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }
    
    createParticle(x, y, color) {
        const particle = {
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 6,
            vy: (Math.random() - 0.5) * 6,
            life: 1.0,
            decay: 0.02,
            color: color,
            size: Math.random() * 3 + 1
        };
        this.particles.push(particle);
    }
    
    updateParticles() {
        this.particles = this.particles.filter(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.life -= particle.decay;
            particle.vy += 0.1; // Gravity
            return particle.life > 0;
        });
    }
    
    render() {
        // Clear canvas with gradient background
        const gradient = this.ctx.createRadialGradient(
            this.canvas.width/2, this.canvas.height/2, 0,
            this.canvas.width/2, this.canvas.height/2, this.canvas.width
        );
        gradient.addColorStop(0, '#000428');
        gradient.addColorStop(1, '#004e92');
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw stars
        this.drawStars();
        
        // Draw game objects
        this.drawPlayer();
        this.drawBullets();
        this.drawEnemies();
        this.drawPowerUps();
        this.drawParticles();
    }
    
    drawStars() {
        this.ctx.fillStyle = 'white';
        for (let i = 0; i < 100; i++) {
            const x = (i * 7) % this.canvas.width;
            const y = (i * 11) % this.canvas.height;
            const size = Math.sin(Date.now() * 0.001 + i) * 0.5 + 1;
            this.ctx.fillRect(x, y, size, size);
        }
    }
    
    drawPlayer() {
        // Draw player ship
        this.ctx.fillStyle = this.player.color;
        this.ctx.fillRect(this.player.x, this.player.y, this.player.width, this.player.height);
        
        // Draw ship details
        this.ctx.fillStyle = '#ffffff';
        this.ctx.fillRect(this.player.x + 15, this.player.y - 5, 10, 15);
        
        // Draw engine glow
        this.ctx.fillStyle = '#ff6600';
        this.ctx.fillRect(this.player.x + 10, this.player.y + this.player.height, 20, 8);
    }
    
    drawBullets() {
        this.bullets.forEach(bullet => {
            this.ctx.fillStyle = bullet.color;
            this.ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            
            // Add bullet glow
            this.ctx.shadowColor = bullet.color;
            this.ctx.shadowBlur = 10;
            this.ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            this.ctx.shadowBlur = 0;
        });
    }
    
    drawEnemies() {
        this.enemies.forEach(enemy => {
            // Draw enemy
            this.ctx.fillStyle = enemy.color;
            this.ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
            
            // Draw health bar
            const healthPercent = enemy.health / enemy.maxHealth;
            this.ctx.fillStyle = 'red';
            this.ctx.fillRect(enemy.x, enemy.y - 8, enemy.width, 4);
            this.ctx.fillStyle = 'green';
            this.ctx.fillRect(enemy.x, enemy.y - 8, enemy.width * healthPercent, 4);
        });
    }
    
    drawPowerUps() {
        this.powerUps.forEach(powerUp => {
            this.ctx.fillStyle = powerUp.color;
            this.ctx.fillRect(powerUp.x, powerUp.y, powerUp.width, powerUp.height);
            
            // Add glow effect
            this.ctx.shadowColor = powerUp.color;
            this.ctx.shadowBlur = 15;
            this.ctx.fillRect(powerUp.x, powerUp.y, powerUp.width, powerUp.height);
            this.ctx.shadowBlur = 0;
        });
    }
    
    drawParticles() {
        this.particles.forEach(particle => {
            this.ctx.globalAlpha = particle.life;
            this.ctx.fillStyle = particle.color;
            this.ctx.fillRect(particle.x, particle.y, particle.size, particle.size);
        });
        this.ctx.globalAlpha = 1;
    }
    
    updateUI() {
        document.getElementById('score').textContent = `Score: ${this.score}`;
        document.getElementById('health').textContent = `Health: ${this.health}`;
        document.getElementById('level').textContent = `Level: ${this.level}`;
    }
    
    gameOver() {
        this.gameRunning = false;
        
        // Show game over screen
        const startScreen = document.getElementById('startScreen');
        const gameTitle = document.getElementById('gameTitle');
        const startButton = document.getElementById('startButton');
        
        gameTitle.textContent = '💀 GAME OVER';
        startButton.textContent = 'PLAY AGAIN';
        startScreen.style.display = 'flex';
        
        // Add final score display
        const scoreDisplay = document.createElement('p');
        scoreDisplay.textContent = `Final Score: ${this.score} | Level Reached: ${this.level}`;
        scoreDisplay.style.fontSize = '20px';
        scoreDisplay.style.marginBottom = '20px';
        
        startScreen.insertBefore(scoreDisplay, startButton);
    }
}

// Initialize game when page loads
window.addEventListener('load', () => {
    const game = new CosmicDefender();
});

// Add background particles
function createBackgroundParticles() {
    const container = document.getElementById('gameContainer');
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 2 + 's';
        particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
        container.appendChild(particle);
    }
}

// Create particles when page loads
window.addEventListener('load', createBackgroundParticles);
