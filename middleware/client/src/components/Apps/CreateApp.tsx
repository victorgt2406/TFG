import { useRef } from "react";
import { Button } from "../../@shadcn/components/ui/button";
import { Input } from "../../@shadcn/components/ui/input";
import { Label } from "../../@shadcn/components/ui/label";
import { TextareaAuto } from "../TextareaAuto";
import mdwApi from "../../utils/mdwApi";
import type { AppModel } from "../../models/App";
import { toast } from "sonner";

export default function () {
    const nameRef = useRef<HTMLInputElement>(null);
    const descriptionRef = useRef<HTMLTextAreaElement>(null);

    async function handleCreateApp() {
        const name =
            nameRef.current && nameRef.current.value.trim() !== ""
                ? nameRef.current.value.trim().toLowerCase()
                : undefined;
        const description =
            descriptionRef.current && descriptionRef.current.value !== ""
                ? descriptionRef.current.value
                : undefined;
        if (name) {
            const content: AppModel = {
                name,
                description,
            };
            const response = await mdwApi.post("/apps/", content);
            console.log(response)
            toast("App created")
        }
    }

    return (
        <>
            <div className="items-center gap-1.5">
                <Label>Name</Label>
                <Input type="text" placeholder="Name" ref={nameRef} />
            </div>
            <div className="items-center gap-1.5">
                <Label>Description</Label>
                <TextareaAuto
                    ref={descriptionRef}
                    placeholder="Description"
                    className="w-full"
                />
            </div>
            <Button variant="default" className="mt-4" onClick={()=>handleCreateApp()}>
                Create App
            </Button>
        </>
    );
}
