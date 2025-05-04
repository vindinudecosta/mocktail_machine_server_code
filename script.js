// const drinks = [
//     "Virgin Mojito", "Shirley Temple", "Virgin Pina Colada", "Cucumber Cooler", "Nojito",
//     "Cranberry Spritzer", "Mango Mule", "Virgin Mary", "Citrus Fizz", "Berry Blast",
//     "Arnold Palmer", "Sparkling Apple Cider", "Lemon Basil Spritzer", "Watermelon Lemonade",
//     "Ginger Beer Limeade", "Pineapple Ginger Ale", "Rose Lemon Spritzer", "Blue Lagoon Mocktail",
//     "Virgin Sangria", "Tropical Sunrise"
// ];

// // Load availability from localStorage
// const drinkAvailability = JSON.parse(localStorage.getItem("drinkAvailability")) || {};

// // Render drinks
// const drinkList = document.getElementById("drinkList");
// drinks.forEach(drink => {
//     const div = document.createElement("div");
//     div.classList.add("drink");
    
//     // Check availability status
//     if (drinkAvailability[drink] === false) {
//         div.classList.add("not-available");
//     } else {
//         div.classList.add("available");
//     }
    
//     div.innerText = drink;
    
//     // Toggle availability on click
//     div.addEventListener("click", () => {
//         const isAvailable = div.classList.contains("available");
//         div.classList.toggle("available", !isAvailable);
//         div.classList.toggle("not-available", isAvailable);
//         drinkAvailability[drink] = !isAvailable;
        
//         // Save to local storage
//         localStorage.setItem("drinkAvailability", JSON.stringify(drinkAvailability));
//     });

//     drinkList.appendChild(div);
// });


// const drinks = [
//     { name: "Virgin Mojito", image: "https://via.placeholder.com/200x150?text=Virgin+Mojito" },
//     { name: "Shirley Temple", image: "https://via.placeholder.com/200x150?text=Shirley+Temple" },
//     { name: "Virgin Pina Colada", image: "https://via.placeholder.com/200x150?text=Virgin+Pina+Colada" },
//     { name: "Cucumber Cooler", image: "https://via.placeholder.com/200x150?text=Cucumber+Cooler" },
//     { name: "Nojito", image: "https://via.placeholder.com/200x150?text=Nojito" },
//     { name: "Cranberry Spritzer", image: "https://via.placeholder.com/200x150?text=Cranberry+Spritzer" },
//     { name: "Mango Mule", image: "https://via.placeholder.com/200x150?text=Mango+Mule" },
//     { name: "Virgin Mary", image: "https://via.placeholder.com/200x150?text=Virgin+Mary" },
//     { name: "Citrus Fizz", image: "https://via.placeholder.com/200x150?text=Citrus+Fizz" },
//     { name: "Berry Blast", image: "https://via.placeholder.com/200x150?text=Berry+Blast" },
//     { name: "Arnold Palmer", image: "https://via.placeholder.com/200x150?text=Arnold+Palmer" },
//     { name: "Sparkling Apple Cider", image: "https://via.placeholder.com/200x150?text=Sparkling+Apple+Cider" },
//     { name: "Lemon Basil Spritzer", image: "https://via.placeholder.com/200x150?text=Lemon+Basil+Spritzer" },
//     { name: "Watermelon Lemonade", image: "https://via.placeholder.com/200x150?text=Watermelon+Lemonade" },
//     { name: "Ginger Beer Limeade", image: "https://via.placeholder.com/200x150?text=Ginger+Beer+Limeade" },
//     { name: "Pineapple Ginger Ale", image: "https://via.placeholder.com/200x150?text=Pineapple+Ginger+Ale" },
//     { name: "Rose Lemon Spritzer", image: "https://via.placeholder.com/200x150?text=Rose+Lemon+Spritzer" },
//     { name: "Blue Lagoon Mocktail", image: "https://via.placeholder.com/200x150?text=Blue+Lagoon+Mocktail" },
//     { name: "Virgin Sangria", image: "https://via.placeholder.com/200x150?text=Virgin+Sangria" },
//     { name: "Tropical Sunrise", image: "https://via.placeholder.com/200x150?text=Tropical+Sunrise" }
// ];

// // Load availability from localStorage
// const drinkAvailability = JSON.parse(localStorage.getItem("drinkAvailability")) || {};

// // Render drinks
// const drinkList = document.getElementById("drinkList");
// drinks.forEach(drink => {
//     const div = document.createElement("div");
//     div.classList.add("drink");

//     // Check availability status
//     if (drinkAvailability[drink.name] === false) {
//         div.classList.add("not-available");
//     } else {
//         div.classList.add("available");
//     }

//     // Add drink image
//     const img = document.createElement("img");
//     img.src = drink.image;
//     img.alt = drink.name;

//     // Add drink name
//     const h3 = document.createElement("h3");
//     h3.innerText = drink.name;

//     div.appendChild(img);
//     div.appendChild(h3);

//     // Toggle availability on click
//     div.addEventListener("click", () => {
//         const isAvailable = div.classList.contains("available");
//         div.classList.toggle("available", !isAvailable);
//         div.classList.toggle("not-available", isAvailable);
//         drinkAvailability[drink.name] = !isAvailable;

//         // Save to local storage
//         localStorage.setItem("drinkAvailability", JSON.stringify(drinkAvailability));
//     });

//     drinkList.appendChild(div);
// });


// const drinks = [
//     { name: "Virgin Mojito", image: "https://www.sustainablecooks.com/wp-content/uploads/2018/06/Classic-Virgin-Mojito-Recipe-2.jpg" },
//     { name: "Shirley Temple", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTS_9lXHhiU1RrbzHA-tghgsZ5r9vPlRmLhcwEaO2-7XHnudvQzrQIHSqzNatAkNhzAZWM&usqp=CAU" },
//     { name: "Virgin Pina Colada", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQy3taAFaJqUjUD-nDT_R3Wgkmr35lOs5VVBA&s" },
//     { name: "Cucumber Cooler", image: "https://www.homemadefoodjunkie.com/wp-content/uploads/2023/07/cucumber-cooler-drink-2.jpg" },
//     { name: "Nojito", image: "https://alekasgettogether.com/wp-content/uploads/2023/08/mojito-mocktail.jpg" },
//     { name: "Cranberry Spritzer", image: "https://cookmorphosis.com/wp-content/uploads/2022/10/vertical-easy-and-quick-cranberry-mock-tail-1.jpg" },
//     { name: "Mango Mule", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzj4wU3kE60w9TP5wvW-UqYpmMENwmeYMKfg&s" },
//     { name: "Virgin Mary", image: "https://foodbyjonister.com/wp-content/uploads/2021/07/VirginBloodyMary-867x1300.jpg" },
//     { name: "Citrus Fizz", image: "https://cocktail-society.com/wp-content/uploads/2025/01/Citrus-Fizz-Mocktail.jpg" },
//     { name: "Berry Blast", image: "https://i.vimeocdn.com/video/1358023096-968f3bc05f879d7d5497bf8c767abe4c8a9350d27f23b5d97e3e70a6327c20c1-d?f=webp" },
//     { name: "Arnold Palmer", image: "https://www.metropolitan-market.com/getmedia/0fc57f78-b4a1-4545-acf0-9580bdeb0a64/231025-155-R231008-Apple-Palmer-Mocktail-Metropolitan-Market.jpg" },
//     { name: "Sparkling Apple Cider", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf8NSidcaJ_ghZ2w_-SNVzL_oMZuFCWaS-EQ&s" },
//     { name: "Lemon Basil Spritzer", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_AiK53xfWHsSzpEfMo1pRn3S6choNSUVAMA&s" },
//     { name: "Watermelon Lemonade", image: "https://thedefineddish.com/wp-content/uploads/2020/07/2020-07-06-03.19.08.jpg" },
//     { name: "Ginger Beer Limeade", image: "https://greenheartlove.com/wp-content/uploads/2025/01/ginger-beer-mocktail-10-500x375.jpg" },
//     { name: "Pineapple Ginger Ale", image: "https://www.cupofzest.com/wp-content/uploads/2021/01/Pineapple-Ginger-Beer-Mocktail-Horizontal.jpg" },
//     { name: "Rose Lemon Spritzer", image: "https://www.halfbakedharvest.com/wp-content/uploads/2016/02/Rose-Lemon-Spriter-1.jpg" },
//     { name: "Blue Lagoon Mocktail", image: "https://savortheflavour.com/wp-content/uploads/2020/07/Blue-Lagoon-Mocktail-Tasty.jpg" },
//     { name: "Virgin Sangria", image: "https://www.simplywhisked.com/wp-content/uploads/2014/05/Virgin-Sangria-NEW-8.jpg" },
//     { name: "Tropical Sunrise", image: "https://www.allrecipes.com/thmb/zL0-Fqh_E_Z9vuMMhiV8hbNumTc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/222510-Tequila-Sunrise-Cocktail-ddmfs-4x3-0872-7ddefb6ec8ed40d0930e5b92f178e2cf.jpg" }
// ];


// // Load availability from localStorage
// const drinkAvailability = JSON.parse(localStorage.getItem("drinkAvailability")) || {};

// // Render drinks
// const drinkList = document.getElementById("drinkList");
// drinks.forEach((drink, index) => {
//     const div = document.createElement("div");
//     div.classList.add("drink");

//     // Check availability status
//     if (drinkAvailability[drink.name] === false) {
//         div.classList.add("not-available");
//     } else {
//         div.classList.add("available");
//     }

//     // Add drink image
//     const img = document.createElement("img");
//     img.src = drink.image;
//     img.alt = drink.name;

//     // Add drink name
//     const h3 = document.createElement("h3");
//     h3.innerText = drink.name;

//     // Add drink number
//     const number = document.createElement("div");
//     number.classList.add("drink-number");
//     number.innerText = index + 1; // Add 1 to start numbering from 1 instead of 0
//     div.appendChild(number);

//     // Add availability icon
//     const icon = document.createElement("div");
//     icon.classList.add("availability-icon");
//     icon.innerText = div.classList.contains("available") ? "✔" : "✖";
//     div.appendChild(icon);

//     div.appendChild(img);
//     div.appendChild(h3);

//     // Toggle availability on click
//     div.addEventListener("click", () => {
//         const isAvailable = div.classList.contains("available");
//         div.classList.toggle("available", !isAvailable);
//         div.classList.toggle("not-available", isAvailable);
//         drinkAvailability[drink.name] = !isAvailable;

//         // Update icon
//         icon.innerText = !isAvailable ? "✔" : "✖";
//         icon.style.backgroundColor = !isAvailable ? "#28a745" : "#dc3545";

//         // Save to local storage
//         localStorage.setItem("drinkAvailability", JSON.stringify(drinkAvailability));
//     });

//     drinkList.appendChild(div);
// });
const drinks = [
    { name: "Virgin Mojito", image: "https://www.sustainablecooks.com/wp-content/uploads/2018/06/Classic-Virgin-Mojito-Recipe-2.jpg" },
    { name: "Shirley Temple", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTS_9lXHhiU1RrbzHA-tghgsZ5r9vPlRmLhcwEaO2-7XHnudvQzrQIHSqzNatAkNhzAZWM&usqp=CAU" },
    { name: "Virgin Pina Colada", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQy3taAFaJqUjUD-nDT_R3Wgkmr35lOs5VVBA&s" },
    { name: "Cucumber Cooler", image: "https://www.homemadefoodjunkie.com/wp-content/uploads/2023/07/cucumber-cooler-drink-2.jpg" },
    { name: "Nojito", image: "https://alekasgettogether.com/wp-content/uploads/2023/08/mojito-mocktail.jpg" },
    { name: "Cranberry Spritzer", image: "https://cookmorphosis.com/wp-content/uploads/2022/10/vertical-easy-and-quick-cranberry-mock-tail-1.jpg" },
    { name: "Mango Mule", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzj4wU3kE60w9TP5wvW-UqYpmMENwmeYMKfg&s" },
    { name: "Virgin Mary", image: "https://foodbyjonister.com/wp-content/uploads/2021/07/VirginBloodyMary-867x1300.jpg" },
    { name: "Citrus Fizz", image: "https://cocktail-society.com/wp-content/uploads/2025/01/Citrus-Fizz-Mocktail.jpg" },
    { name: "Berry Blast", image: "https://i.vimeocdn.com/video/1358023096-968f3bc05f879d7d5497bf8c767abe4c8a9350d27f23b5d97e3e70a6327c20c1-d?f=webp" },
    { name: "Arnold Palmer", image: "https://www.metropolitan-market.com/getmedia/0fc57f78-b4a1-4545-acf0-9580bdeb0a64/231025-155-R231008-Apple-Palmer-Mocktail-Metropolitan-Market.jpg" },
    { name: "Sparkling Apple Cider", image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf8NSidcaJ_ghZ2w_-SNVzL_oMZuFCWaS-EQ&s" },
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

// Render drinks
const drinkList = document.getElementById("drinkList");
drinks.forEach((drink, index) => {
    const div = document.createElement("div");
    div.classList.add("swiper-slide", "drink");

    // Check availability status
    if (drinkAvailability[drink.name] === false) {
        div.classList.add("not-available");
    } else {
        div.classList.add("available");
    }

    // Add drink image
    const img = document.createElement("img");
    img.src = drink.image;
    img.alt = drink.name;
    img.loading = "lazy";

    // Add drink name
    const h3 = document.createElement("h3");
    h3.innerText = drink.name;

    // Add drink number
    const number = document.createElement("div");
    number.classList.add("drink-number");
    number.innerText = index + 1;

    // Add availability icon
    const icon = document.createElement("div");
    icon.classList.add("availability-icon");
    icon.innerText = div.classList.contains("available") ? "✔" : "✖";
    icon.style.backgroundColor = div.classList.contains("available") ? "#00ff99" : "#ff3366";

    div.appendChild(number);
    div.appendChild(icon);
    div.appendChild(img);
    div.appendChild(h3);

    // Toggle availability on click
    div.addEventListener("click", () => {
        const isAvailable = div.classList.contains("available");
        div.classList.toggle("available", !isAvailable);
        div.classList.toggle("not-available", isAvailable);
        drinkAvailability[drink.name] = !isAvailable;

        // Update icon
        icon.innerText = !isAvailable ? "✔" : "✖";
        icon.style.backgroundColor = !isAvailable ? "#00ff99" : "#ff3366";

        // Save to local storage
        localStorage.setItem("drinkAvailability", JSON.stringify(drinkAvailability));
    });

    drinkList.appendChild(div);
});

// Initialize Swiper
const swiper = new Swiper('.swiper-container', {
    slidesPerView: 3, // Show ~3 drinks
    spaceBetween: 8,
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    grabCursor: true,
    breakpoints: {
        721: {
            slidesPerView: 4,
            spaceBetween: 16,
        }
    }
});

// Revert to grid layout on desktop
if (window.innerWidth > 720) {
    document.querySelector('.swiper-wrapper').classList.add('drink-grid');
    document.querySelector('.swiper-container').classList.remove('swiper-container');
    swiper.destroy();
}

// Full-screen toggle
const fullscreenBtn = document.querySelector('.fullscreen-btn');
const enterIcon = document.querySelector('.enter-fullscreen');
const exitIcon = document.querySelector('.exit-fullscreen');

fullscreenBtn.addEventListener('click', () => {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().then(() => {
            enterIcon.style.display = 'none';
            exitIcon.style.display = 'block';
        }).catch(err => console.error('Fullscreen error:', err));
    } else {
        document.exitFullscreen().then(() => {
            enterIcon.style.display = 'block';
            exitIcon.style.display = 'none';
        }).catch(err => console.error('Exit fullscreen error:', err));
    }
});

// Initialize full-screen icon state
if (document.fullscreenElement) {
    enterIcon.style.display = 'none';
    exitIcon.style.display = 'block';
} else {
    enterIcon.style.display = 'block';
    exitIcon.style.display = 'none';
}