document.querySelectorAll("[class*='hover:']").forEach(element => {
    element.addEventListener("mouseenter", () => {
        const hoverClasses=[...element.classList].filter(cls => cls.startsWith("hover:"));
        hoverClasses.forEach(hoverClass => {
            element.classList.add(hoverClass.replace("hover:", ""));
        });
    });

    element.addEventListener("mouseleave", () => {
        const hoverClasses=[...element.classList].filter(cls => cls.startsWith("hover:"));
        hoverClasses.forEach(hoverClass => {
            element.classList.remove(hoverClass.replace("hover:", ""));
        });
    });
});
