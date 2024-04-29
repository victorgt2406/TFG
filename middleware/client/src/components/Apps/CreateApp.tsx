import { useRef } from "react";
import { Button } from "../../@shadcn/components/ui/button";
import { Input } from "../../@shadcn/components/ui/input";
import { Label } from "../../@shadcn/components/ui/label";
import { TextareaAuto } from "../TextareaAuto";

type MyProps = {
    handleCreate: (name: string, description?: string) => void;
};

export default function ({ handleCreate }: MyProps) {
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
            handleCreate(name, description);
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
            <Button
                variant="default"
                className="mt-4"
                onClick={handleCreateApp}
            >
                Create App
            </Button>
        </>
    );
}
