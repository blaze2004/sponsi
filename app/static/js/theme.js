const toggleTheme=() => {
    const darkModeEnabled=document.documentElement.classList.toggle('dark');

    const elements=document.querySelectorAll('[class*="dark:"]');

    elements.forEach((element) => {
        const classes=element.classList;

        classes.forEach((cls) => {
            if (cls.startsWith('dark:')) {
                const baseClass=cls.replace('dark:', '');
                if (darkModeEnabled) {
                    element.classList.add(baseClass);
                } else {
                    element.classList.remove(baseClass);
                }
            }
        });
    });

    if (darkModeEnabled) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
}

const getSystemTheme=() => {
    return window.matchMedia('(prefers-color-scheme: dark)').matches? 'dark':'light'
}
document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

if (localStorage.getItem('theme')) {
    if (localStorage.getItem('theme')==='dark')
        toggleTheme();
} else {
    if (getSystemTheme()==='dark')
        toggleTheme();
}
