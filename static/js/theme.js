// static/js/theme.js

document.addEventListener('DOMContentLoaded', function() {
    const themeSwitch = document.getElementById('theme-switch-checkbox');
    const currentTheme = localStorage.getItem('theme');

    // Function to set the theme
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        if (theme === 'dark') {
            themeSwitch.checked = true;
        } else {
            themeSwitch.checked = false;
        }
    }

    // Initialize theme based on stored preference or system setting
    if (currentTheme) {
        setTheme(currentTheme);
    } else {
        // Check for system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            setTheme('dark');
        } else {
            setTheme('light');
        }
    }

    // Add event listener for the switch
    themeSwitch.addEventListener('change', function(e) {
        if (e.target.checked) {
            setTheme('dark');
        } else {
            setTheme('light');
        }
    });

    // Listen for changes in system preference
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        const newColorScheme = e.matches ? "dark" : "light";
        // Only change if user hasn't manually set a theme
        if (!localStorage.getItem('theme')) {
             setTheme(newColorScheme);
        }
    });
});
