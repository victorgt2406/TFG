import { useEffect, useState } from "react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../../@shadcn/components/ui/select";
import handleTheme, { getTheme, type ThemeType } from "../../utils/handleTheme";

export default function DarkModeButton({ className }: { className?: string }) {
    const [theme, setTheme] = useState<ThemeType | undefined>(undefined);

    useEffect(() => {
        setTheme(getTheme());
    }, []);
    return (
        <div className={`w-28 ${className}`}>
            <Select
                onValueChange={(value: ThemeType) => {
                    handleTheme(value);
                    setTheme(value);
                }}
                value={theme}
            >
                <SelectTrigger>
                    <SelectValue placeholder={"Theme"} />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="light">
                        Light <i className="bi bi-brightness-high-fill"></i>
                    </SelectItem>
                    <SelectItem value="dark">
                        Dark <i className="bi bi-moon-stars-fill"></i>
                    </SelectItem>
                    <SelectItem value="system">
                        System <i className="bi bi-laptop"></i>
                    </SelectItem>
                </SelectContent>
            </Select>
        </div>
    );
}
