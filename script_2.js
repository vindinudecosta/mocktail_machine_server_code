console.log('script_2.js: Loading...');

const drinks = [
    { name: "Virgin Mojito", image: "https://www.sustainablecooks.com/wp-content/uploads/2018/06/Classic-Virgin-Mojito-Recipe-2.jpg" },
    { name: "Shirley Temple", image: "https://bellyfull.net/wp-content/uploads/2020/12/Shirley-Temple-Drink-blog-3.jpg" },
    { name: "Virgin Pina Colada", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBmWCcCG0AVkrWGjAGYKVy0gGpFdsHWkkLvw&s" },
    { name: "Cucumber Cooler", image: "https://www.homemadefoodjunkie.com/wp-content/uploads/2023/07/cucumber-cooler-drink-2.jpg" },
    { name: "Nojito", image: "https://alekasgettogether.com/wp-content/uploads/2023/08/mojito-mocktail.jpg" },
    { name: "Cranberry Spritzer", image: "https://cookmorphosis.com/wp-content/uploads/2022/10/vertical-easy-and-quick-cranberry-mock-tail-1.jpg" },
    { name: "Mango Mule", image: "https://pinklotus.com/wp-content/uploads/2020/08/plpu-cancer-kicking-kitchen-mango-mule.jpg" },
    { name: "Virgin Mary", image: "https://foodbyjonister.com/wp-content/uploads/2021/07/VirginBloodyMary-867x1300.jpg" },
    { name: "Citrus Fizz", image: "https://cocktail-society.com/wp-content/uploads/2025/01/Citrus-Fizz-Mocktail.jpg" },
    { name: "Berry Blast", image: "https://i.vimeocdn.com/video/1358023096-968f3bc05f879d7d5497bf8c767abe4c8a9350d27f23b5d97e3e70a6327c20c1-d?f=webp" },
    { name: "Arnold Palmer", image: "https://www.metropolitan-market.com/getmedia/0fc57f78-b4a1-4545-acf0-9580bdeb0a64/231025-155-R231008-Apple-Palmer-Mocktail-Metropolitan-Market.jpg" },
    { name: "Sparkling Apple Cider", image: "https://healthdownsouth.com/wp-content/uploads/2024/09/apple-cider-mocktail-5.jpg" },
    { name: "Lemon Basil Spritzer", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_AiK53xfWHsSzpEfMo1pRn3S6choNSUVAMA&s" },
    { name: "Watermelon Lemonade", image: "https://thedefineddish.com/wp-content/uploads/2020/07/2020-07-06-03.19.08.jpg" },
    { name: "Ginger Beer Limeade", image: "https://greenheartlove.com/wp-content/uploads/2025/01/ginger-beer-mocktail-10-500x375.jpg" },
    { name: "Pineapple Ginger Ale", image: "https://www.cupofzest.com/wp-content/uploads/2021/01/Pineapple-Ginger-Beer-Mocktail-Horizontal.jpg" },
    { name: "Rose Lemon Spritzer", image: "https://www.halfbakedharvest.com/wp-content/uploads/2016/02/Rose-Lemon-Spriter-1.jpg" },
    { name: "Blue Lagoon Mocktail", image: "https://savortheflavour.com/wp-content/uploads/2020/07/Blue-Lagoon-Mocktail-Tasty.jpg" },
    { name: "Virgin Sangria", image: "https://www.simplywhisked.com/wp-content/uploads/2014/05/Virgin-Sangria-NEW-8.jpg" },
    { name: "Tropical Sunrise", image: "https://www.allrecipes.com/thmb/zL0-Fqh_E_Z9vuMMhiV8hbNumTc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/222510-Tequila-Sunrise-Cocktail-ddmfs-4x3-0872-7ddefb6ec8ed40d0930e5b92f178e2cf.jpg" }
];

// Load availability from localStorage
const drinkAvailability = JSON.parse(localStorage.getItem("drinkAvailability")) || {};

// Initialize elements
const messageText = document.getElementById('messageText');
const messageBox = document.getElementById('messageBox');
const progressBar = document.getElementById('progressBar');
let currentDrink = null;
let messageQueue = [];
let isProcessing = false;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    
    // Render drinks first
    renderDrinks();
    
    // Initialize Swiper after a small delay to ensure DOM is ready
    setTimeout(initSwiper, 100);
    
    // Setup SSE connection
    setupEventSource();
});

function renderDrinks() {
    const drinkList = document.getElementById('drinkList');
    if (!drinkList) {
        console.error('Drink list element not found');
        return;
    }

    // Clear existing content
    drinkList.innerHTML = '';

    // Create drink slides
    drinks.forEach((drink, index) => {
        const slide = document.createElement('div');
        slide.className = 'swiper-slide';

        const drinkDiv = document.createElement('div');
        drinkDiv.className = 'drink';
        
        // Set availability class
        if (drinkAvailability[drink.name] === false) {
            drinkDiv.classList.add('not-available');
        } else {
            drinkDiv.classList.add('available');
        }

        // Create image container
        const imgContainer = document.createElement('div');
        imgContainer.className = 'drink-img-container';
        
        const img = document.createElement('img');
        img.className = 'drink-image';
        img.alt = drink.name;
        img.loading = 'lazy';
        loadImageWithFallback(img, drink.image, drink.name);

        // Add drink number
        const number = document.createElement('div');
        number.className = 'drink-number';
        number.textContent = index + 1;

        // Add availability icon
        const icon = document.createElement('div');
        icon.className = 'availability-icon';
        icon.textContent = drinkDiv.classList.contains('available') ? '✔' : '✖';
        icon.style.backgroundColor = drinkDiv.classList.contains('available') ? '#00ff99' : '#ff3366';

        const h3 = document.createElement('h3');
        h3.textContent = drink.name;

        // Toggle availability on click
        drinkDiv.addEventListener('click', function() {
            const isAvailable = this.classList.contains('available');
            this.classList.toggle('available', !isAvailable);
            this.classList.toggle('not-available', isAvailable);
            
            // Update icon
            const icon = this.querySelector('.availability-icon');
            icon.textContent = !isAvailable ? '✔' : '✖';
            icon.style.backgroundColor = !isAvailable ? '#00ff99' : '#ff3366';
            
            // Update storage
            drinkAvailability[drink.name] = !isAvailable;
            localStorage.setItem('drinkAvailability', JSON.stringify(drinkAvailability));
        });

        // Build the DOM structure
        drinkDiv.appendChild(number);
        drinkDiv.appendChild(icon);
        imgContainer.appendChild(img);
        drinkDiv.appendChild(imgContainer);
        drinkDiv.appendChild(h3);
        slide.appendChild(drinkDiv);
        drinkList.appendChild(slide);
    });
}

function loadImageWithFallback(imgElement, imageUrl, drinkName) {
    const placeholderUrl = `https://via.placeholder.com/150/1e1e2f/00ffc8?text=${encodeURIComponent(drinkName.substring(0, 15))}`;
    
    imgElement.style.opacity = '0';
    imgElement.src = imageUrl;
    
    imgElement.onload = function() {
        imgElement.style.opacity = '1';
    };
    
    imgElement.onerror = function() {
        console.error(`Failed to load image: ${imageUrl}`);
        imgElement.src = placeholderUrl;
        imgElement.style.opacity = '1';
        imgElement.onerror = null;
    };
    
    // Timeout for slow-loading images
    setTimeout(() => {
        if (!imgElement.complete || imgElement.naturalWidth === 0) {
            imgElement.src = placeholderUrl;
            imgElement.style.opacity = '1';
        }
    }, 3000);
}

function initSwiper() {
    if (typeof Swiper === 'undefined') {
        console.error('Swiper library not loaded');
        return;
    }

    const swiperContainer = document.querySelector('.swiper-container');
    if (!swiperContainer) {
        console.error('Swiper container not found');
        return;
    }

    const swiper = new Swiper('.swiper-container', {
        slidesPerView: 'auto',
        centeredSlides: true,
        spaceBetween: 20,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        breakpoints: {
            320: { slidesPerView: 1, spaceBetween: 10 },
            480: { slidesPerView: 2, spaceBetween: 15 },
            720: { slidesPerView: 3, spaceBetween: 20 },
            1024: { slidesPerView: 4, spaceBetween: 25 }
        }
    });

    console.log('Swiper initialized successfully');
}


// Full-screen toggle
const fullscreenBtn = document.querySelector('.fullscreen-btn');
const enterIcon = document.querySelector('.enter-fullscreen');
const exitIcon = document.querySelector('.exit-fullscreen');

if (fullscreenBtn) {
    fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().then(() => {
                if (enterIcon && exitIcon) {
                    enterIcon.style.display = 'none';
                    exitIcon.style.display = 'block';
                }
            }).catch(err => console.error('script_2.js: Fullscreen error:', err));
        } else {
            document.exitFullscreen().then(() => {
                if (enterIcon && exitIcon) {
                    enterIcon.style.display = 'block';
                    exitIcon.style.display = 'none';
                }
            }).catch(err => console.error('script_2.js: Exit fullscreen error:', err));
        }
    });
}

if (document.fullscreenElement && enterIcon && exitIcon) {
    enterIcon.style.display = 'none';
    exitIcon.style.display = 'block';
} else if (enterIcon && exitIcon) {
    enterIcon.style.display = 'block';
    exitIcon.style.display = 'none';
}


document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    
    // Initialize SSE connection
    setupEventSource();
    
    // Render drinks and initialize Swiper
    renderDrinks().then(() => {
        initSwiper();
        
        // Force Swiper to update after images load
        const images = document.querySelectorAll('.drink-image');
        let loadedImages = 0;
        
        images.forEach(img => {
            if (img.complete) {
                loadedImages++;
            } else {
                img.addEventListener('load', () => {
                    loadedImages++;
                    if (loadedImages === images.length) {
                        if (typeof Swiper !== 'undefined' && window.swiperInstance) {
                            window.swiperInstance.update();
                        }
                    }
                });
            }
        });
    }).catch(err => {
        console.error('Initialization error:', err);
    });
});

function setupEventSource() {
    console.log('Setting up SSE connection...');
    
    // Close any existing connection
    if (window.eventSource) {
        window.eventSource.close();
    }

    // Create new connection
    window.eventSource = new EventSource('/status-stream');
    
    // Connection opened
    window.eventSource.onopen = () => {
        console.log('SSE connection established');
        messageText.textContent = 'Connected to mocktail machine';
    };

    // Error handling
    window.eventSource.onerror = (e) => {
        console.error('SSE error:', e);
        if (e.eventPhase === EventSource.CLOSED) {
            messageText.textContent = 'Connection closed - reconnecting...';
            setTimeout(setupEventSource, 3000);
        }
    };

    // Message handler - THIS WAS MISSING
    window.eventSource.addEventListener('message', (e) => {
        try {
            const data = JSON.parse(e.data);
            console.log('SSE Message received:', data);
            
            // Update UI based on message type
            if (data.type === 'status_update') {
                updateStatusDisplay(data);
            }
            // Add other message types as needed
            
        } catch (err) {
            console.error('Error processing message:', err);
        }
    });

    // Specific handler for status updates
    window.eventSource.addEventListener('status_update', (e) => {
        try {
            const data = JSON.parse(e.data);
            console.log('Status update received:', data);
            updateStatusDisplay(data);
        } catch (err) {
            console.error('Error processing status update:', err);
        }
    });
}
function updateStatusDisplay(data) {
    // Clear any existing timeout
    if (window.statusTimeout) {
        clearTimeout(window.statusTimeout);
    }
    
    // Update message text
    if (data.message) {
        messageText.textContent = data.message;
        messageBox.classList.add('active');
        
        // Update progress bar if duration exists
        if (data.duration) {
            progressBar.style.width = '0%';
            progressBar.style.transition = 'none'; // Reset transition
            setTimeout(() => {
                progressBar.style.transition = `width ${data.duration}ms linear`;
                progressBar.style.width = '100%';
            }, 50);
        }
        
        // Highlight the drink if specified
        if (data.drink) {
            document.querySelectorAll('.drink').forEach(el => {
                const name = el.querySelector('h3')?.textContent;
                el.classList.toggle('preparing', name && name.toLowerCase() === data.drink.toLowerCase());
            });
        }
        
        // Set timeout to clear message
        if (data.duration) {
            window.statusTimeout = setTimeout(() => {
                messageText.textContent = 'Ready for next command';
                messageBox.classList.remove('active');
                progressBar.style.width = '0%';
            }, data.duration);
        }
    }
}

// Clean up when page is unloaded
window.addEventListener('beforeunload', () => {
    if (window.eventSource) {
        window.eventSource.close();
    }
    if (window.statusTimeout) {
        clearTimeout(window.statusTimeout);
    }
});

// Replace the polling initialization with:
console.log('script_2.js: Setting up SSE connection...');
setupEventSource();