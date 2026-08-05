document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector(".sg-header");
    var firstSection = document.getElementById("inicio");
    var menuButton = document.getElementById("menu-toggle");
    var menu = document.getElementById("menu-principal");
    var openIcon = document.getElementById("menu-icon-open");
    var closeIcon = document.getElementById("menu-icon-close");

    function syncHeaderEffect() {
        if (!header || !firstSection) {
            return;
        }

        var headerRect = header.getBoundingClientRect();
        var sectionRect = firstSection.getBoundingClientRect();
        var isTouchingHeader = sectionRect.top <= headerRect.bottom && sectionRect.bottom > headerRect.top;
        header.classList.toggle("sg-header--hero-touch", isTouchingHeader);
    }

    syncHeaderEffect();
    window.addEventListener("scroll", syncHeaderEffect, { passive: true });
    window.addEventListener("resize", syncHeaderEffect);

    if (!menuButton || !menu) {
        return;
    }

    function setMenuState(isOpen) {
        menu.classList.toggle("hidden", !isOpen);
        menuButton.setAttribute("aria-expanded", String(isOpen));
        menuButton.setAttribute("aria-label", isOpen ? "Fechar menu principal" : "Abrir menu principal");

        if (openIcon && closeIcon) {
            openIcon.classList.toggle("hidden", isOpen);
            closeIcon.classList.toggle("hidden", !isOpen);
        }
    }

    menuButton.addEventListener("click", function () {
        var isHidden = menu.classList.contains("hidden");
        setMenuState(isHidden);
    });

    menu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            if (window.innerWidth < 768) {
                setMenuState(false);
            }
        });
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth >= 768) {
            setMenuState(false);
        }
    });
});