document.addEventListener("DOMContentLoaded", function () {
    var menuButton = document.getElementById("menu-toggle");
    var menu = document.getElementById("menu-principal");
    var openIcon = document.getElementById("menu-icon-open");
    var closeIcon = document.getElementById("menu-icon-close");

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