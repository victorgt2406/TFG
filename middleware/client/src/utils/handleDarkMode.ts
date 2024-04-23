export default function handleDarkMode(theme: "dark" | "light" | "system") {
    function applyTheme(theme:"dark"|"light"){
        document.documentElement.className = theme;
        console.log(`Theme changed to ${theme}`);
    }
    if (theme === "system") {
        const matchMedia = window.matchMedia("(prefers-color-scheme: dark)");
        const sysDark = matchMedia.matches;
        const sysTheme = sysDark ? "dark" : "light";
        applyTheme(sysTheme);
        // Listen system dark mode changes
        const handleDarkModeSystem = (e: MediaQueryListEvent) => {
            const updatedTheme = e.matches ? "dark" : "light";
            applyTheme(updatedTheme);
        };
        matchMedia.addEventListener("change", handleDarkModeSystem);
        return () => matchMedia.removeEventListener('change', handleDarkModeSystem);
    }
    else {
        applyTheme(theme);
    }

}
