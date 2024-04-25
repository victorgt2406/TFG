import { ScrollArea } from "../../@shadcn/components/ui/scroll-area";
import Input from "./Input";
import Output from "./Output";

export default function () {
    return (
        <div className="flex flex-col my-2 p-2 h-full">
            <ScrollArea className="h-[400px]">
                <Output />
            </ScrollArea>
            <div className="absolute bottom-0 pb-2 w-full">
                <Input />
            </div>
        </div>
    );
}
