import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../../@shadcn/components/ui/select";
import handleDarkMode, { getDarkModeCookie, type DarkModeType } from "../../utils/handleDarkMode";

export default function DarkModeButton() {
    const defaultTheme = getDarkModeCookie();
    return (
        <Select
            onValueChange={(value) => handleDarkMode(value as DarkModeType)}
            defaultValue={defaultTheme}
        >
            <SelectTrigger>
                <SelectValue placeholder="Theme" />
            </SelectTrigger>
            <SelectContent>
                <SelectItem value="light">Light</SelectItem>
                <SelectItem value="dark">Dark</SelectItem>
                <SelectItem value="system">System</SelectItem>
            </SelectContent>
        </Select>
    );
}
