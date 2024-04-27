import { useRef } from "react";
import { Button } from "../../@shadcn/components/ui/button";
import { Input } from "../../@shadcn/components/ui/input";
import { Label } from "../../@shadcn/components/ui/label";
import { TextareaAuto } from "../TextareaAuto";
import mdwApi from "../../utils/mdwApi";
import type { AppModel } from "../../models/App";

export default function () {
    const nameRef = useRef(null);
    const descriptionRef = useRef(null);

    // async function handleCreateApp(){
    //     const content:AppModel = {

    //     }
    //     mdwApi.post("/app/",content)
    // }

    return (
        <>
            <div className="items-center gap-1.5">
                <Label>Name</Label>
                <Input type="text" placeholder="Name" ref={nameRef}/>
            </div>
            <div className="items-center gap-1.5">
                <Label>Description</Label>
                <TextareaAuto ref={descriptionRef} placeholder="Description" className="w-full"/>
            </div>
            <Button variant="default" className="mt-4">Create App</Button>
        </>
    );
}
