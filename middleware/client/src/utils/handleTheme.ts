const GLOBAL_THEME = "theme";
import Cookies from "js-cookie";

type ThemeType = "dark" | "light" | "system";

export default function handleTheme(theme: ThemeType) {
    localStorage.setItem(GLOBAL_THEME, theme);
    // Cookies.set(COOKIE_DARKMODE, theme);
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
            const cookieTheme: string | undefined = Cookies.get(GLOBAL_THEME);
            if (cookieTheme === "system") {
                applyTheme(updatedTheme);
            } else {
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

function getTheme(): ThemeType {
    // return Cookies.get(COOKIE_DARKMODE) as DarkModeType;
    const theme = localStorage.getItem(GLOBAL_THEME);
    if (theme) {
        return theme as ThemeType;
    } else return "system";
}

export { getTheme, GLOBAL_THEME };

export type { ThemeType };
