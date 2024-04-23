import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../@shadcn/components/ui/select";
import handleDarkMode from "../utils/handleDarkMode";

export default function DarkModeButton() {
    return (
        <Select onValueChange={(value)=>handleDarkMode(value as "dark" | "light" | "system")}>
            <SelectTrigger>
                <SelectValue placeholder="Theme" />
            </SelectTrigger>
            <SelectContent>
                <SelectItem value="light" onSelect={()=>handleDarkMode("light")}>Light</SelectItem>
                <SelectItem value="dark" onSelect={()=>alert("hey")}>Dark</SelectItem>
                <SelectItem value="system" onSelect={()=>handleDarkMode("system")}>System</SelectItem>
            </SelectContent>
        </Select>
    );
}
