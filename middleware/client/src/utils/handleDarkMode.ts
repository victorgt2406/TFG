const COOKIE_DARKMODE = "darkMode";
import Cookies from "js-cookie";

type DarkModeType = "dark" | "light" | "system";

export default function handleDarkMode(theme: DarkModeType) {
    Cookies.set(COOKIE_DARKMODE, theme);
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
            const cookieTheme: string | undefined = Cookies.get(COOKIE_DARKMODE);
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

function getDarkModeCookie(): DarkModeType {
    return Cookies.get(COOKIE_DARKMODE) as DarkModeType;
}

export { getDarkModeCookie, COOKIE_DARKMODE };

export type { DarkModeType };
