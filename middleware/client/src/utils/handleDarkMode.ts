const COOKIE = "darkMode";
import Cookies from 'js-cookie'

export default function handleDarkMode(theme: "dark" | "light" | "system") {
    Cookies.set(COOKIE, theme);
    function applyTheme(theme: "dark" | "light") {
        document.documentElement.className = theme;
    }
    if (theme === "system") {
        const matchMedia = window.matchMedia("(prefers-color-scheme: dark)");
        const sysDark = matchMedia.matches;
        const sysTheme = sysDark ? "dark" : "light";
        applyTheme(sysTheme);
        // Listen system dark mode changes
        const handleDarkModeSystem = (e: MediaQueryListEvent) => {
            const updatedTheme = e.matches ? "dark" : "light";
            const cookieTheme: string | undefined = Cookies.get(COOKIE);
            if (cookieTheme === "system") {
                applyTheme(updatedTheme);
            }
            else{
                matchMedia.removeEventListener("change", handleDarkModeSystem);
            }
        };
        matchMedia.addEventListener("change", handleDarkModeSystem);
        return () =>
            matchMedia.removeEventListener("change", handleDarkModeSystem);
    } else {
        applyTheme(theme);
    }
}
