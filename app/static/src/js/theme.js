const applyTheme=(theme) => {

    const darkModeEnabled=theme==='dark';
    const lightModeEnabled=!darkModeEnabled;

    if (darkModeEnabled) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }

    const darkElements=document.querySelectorAll('[class*="dark:"]');
    const lightElements=document.querySelectorAll('[class*="light:"]');

    darkElements.forEach((element) => {
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

    lightElements.forEach((element) => {
        const classes=element.classList;

        classes.forEach((cls) => {
            if (cls.startsWith('light:')) {
                const baseClass=cls.replace('light:', '');
                if (lightModeEnabled) {
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
const toggleTheme=() => {
    console.log('toggleTheme');
    const darkModeEnabled=document.documentElement.classList.contains('dark');
    applyTheme(darkModeEnabled? 'light':'dark');
}

const getSystemTheme=() => {
    return window.matchMedia('(prefers-color-scheme: dark)').matches? 'dark':'light'
}

document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

if (localStorage.getItem('theme')) {
    applyTheme(localStorage.getItem('theme'));
} else {
    applyTheme(getSystemTheme());
}
