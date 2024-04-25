import { ScrollArea } from "../../@shadcn/components/ui/scroll-area";
import Input from "./Input";
import Output from "./Output";

export default function () {
    return (
        <div className="flex flex-col my-2">
            <div className="flex-auto">
                <ScrollArea className="h-[500px]">
                    <Output />
                </ScrollArea>
            </div>
            <div className="mt-2">
                <Input />
            </div>
        </div>
    );
}
