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
    const [darkModeValue, setDarkModeValue] = useState<ThemeType>("system");

    useEffect(() => {
        setDarkModeValue(getTheme());
    }, []);
    return (
        <div className={`w-28 ${className}`}>
            <Select
                onValueChange={(value: ThemeType) => {
                    handleTheme(value);
                    setDarkModeValue(value);
                }}
                value={darkModeValue}
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
