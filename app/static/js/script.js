/* ==================== ANIMAÇÃO DE SCROLL ==================== */
// Para elementos com atributo data-anime
const animeItems = document.querySelectorAll("[data-anime]");

const animeScroll = () => {
    const windowHeight = window.innerHeight;
    const windowTop = window.scrollY;
    
    animeItems.forEach((element) => {
        const elementTop = element.offsetTop;
        const elementVisible = 150;
        
        if (windowTop + windowHeight > elementTop + elementVisible) {
            element.classList.add("animate");
        } else {
            // Opcional: remove a classe se quiser que repita
            // element.classList.remove("animate");
        }
    });
}

// Executa ao carregar
animeScroll();

// Executa ao scrollar
window.addEventListener("scroll", animeScroll);