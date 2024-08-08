const toggleButton=document.getElementById('theme-toggle');
const htmlElement=document.documentElement;

toggleButton.addEventListener('click', () => {
    if (htmlElement.classList.contains('dark')) {
        htmlElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        htmlElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
});


const savedTheme=localStorage.getItem('theme');
if (savedTheme==='dark') {
    htmlElement.classList.add('dark');
}