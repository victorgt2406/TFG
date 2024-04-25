import { ScrollArea } from "../../@shadcn/components/ui/scroll-area";
import Input from "./Input";
import Output from "./Output";

export default function () {
    return (
        <>
            <ScrollArea>
                <section className="flex justify-center">
                    <Output className="my-1 container p-0" />
                </section>
            </ScrollArea>
            <section className="container mt-1 mb-2 w-full p-0">
                <Input />
            </section>
        </>
    );
}
