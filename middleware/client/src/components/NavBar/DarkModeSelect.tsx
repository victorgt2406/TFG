import { useEffect, useState } from "react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../../@shadcn/components/ui/select";
import handleDarkMode, {
    getDarkModeCookie,
    type DarkModeType,
} from "../../utils/handleDarkMode";

export default function DarkModeButton() {
    const [darkModeValue, setDarkModeValue] = useState<DarkModeType | undefined>(
        undefined
    );

    useEffect(() => {
        setDarkModeValue(getDarkModeCookie());
    }, []);
    return (
        <div className="w-28 mx-2">
            <Select
                onValueChange={(value:DarkModeType) => {
                    handleDarkMode(value);
                    setDarkModeValue(value);
                }}
                value={darkModeValue}
            >
                <SelectTrigger>
                    <SelectValue placeholder="Theme" />
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
