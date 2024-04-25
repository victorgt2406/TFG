import { ScrollArea } from "../../@shadcn/components/ui/scroll-area";
import type { LsmResponseType } from "../../models/LsmResponse";
import mdwApi from "../../utils/mdwApi";
import Input from "./Input";
import Output from "./Output";

export default function () {

    async function handleMessage(message:string){
        console.log(message)
        const response = await mdwApi.post("/chat/", {
            message,
        });
        if(response.status === 200){
            const lsmResponse:LsmResponseType = response.data
            console.log(response.data)
        }
        // console.log(response);
    }

    return (
        <>
            <ScrollArea>
                <section className="flex justify-center">
                    <Output className="my-1 container p-0" />
                </section>
            </ScrollArea>
            <section className="container mt-1 mb-2 w-full p-0">
                <Input handleMessage={handleMessage} />
            </section>
        </>
    );
}
