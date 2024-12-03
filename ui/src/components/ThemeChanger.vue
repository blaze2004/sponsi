<template>
    <button class="btn btn-light dark:btn-dark" @click="toggleTheme">
        <img class="dark:d-none h-4 w-4" src="@/assets/icons/moon.svg" alt="moon icon" />
        <img class="light:d-none dark:d-inline h-4 w-4" src="@/assets/icons/sun.svg" alt="sun icon" />
    </button>
</template>

<script>
export default {
    data() {
        return {
            theme: localStorage.getItem('theme') || window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
        };
    },
    mounted() {
        this.applyTheme(this.theme);
    },
    methods: {
        applyTheme(theme) {
            const darkModeEnabled = theme === 'dark';
            const lightModeEnabled = !darkModeEnabled;

            if (darkModeEnabled) {
                document.documentElement.classList.add('dark');
                document.documentElement.dataset.bsTheme = 'dark';
            } else {
                document.documentElement.classList.remove('dark');
                document.documentElement.dataset.bsTheme = 'light';
            }

            const darkElements = document.querySelectorAll('[class*="dark:"]');
            const lightElements = document.querySelectorAll('[class*="light:"]');

            darkElements.forEach((element) => {
                const classes = element.classList;

                classes.forEach((cls) => {
                    if (cls.startsWith('dark:')) {
                        const baseClass = cls.replace('dark:', '');
                        if (darkModeEnabled) {
                            element.classList.add(baseClass);
                        } else {
                            element.classList.remove(baseClass);
                        }
                    }
                });
            });

            lightElements.forEach((element) => {
                const classes = element.classList;

                classes.forEach((cls) => {
                    if (cls.startsWith('light:')) {
                        const baseClass = cls.replace('light:', '');
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
        },
        toggleTheme() {
            const darkModeEnabled = document.documentElement.classList.contains('dark');
            this.applyTheme(darkModeEnabled ? 'light' : 'dark');
        },
    },
};
</script>
