import { useRef } from "react";
import { Button } from "../../@shadcn/components/ui/button";
import { Input } from "../../@shadcn/components/ui/input";
import { Label } from "../../@shadcn/components/ui/label";
import { TextareaAuto } from "../TextareaAuto";
import UploadButton from "./UploadButton";
import { toast } from "sonner";
import type { AppModel } from "../../models/App";

type MyProps = {
    // handleCreate: (name: string, description?: string) => void;
    handleCreate: (content: AppModel) => void;
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
            descriptionRef.current && descriptionRef.current.value !== "" ? descriptionRef.current.value : undefined;
        if (name) {
            handleCreate({ name, description });
            if (nameRef.current) nameRef.current.value = "";
            if (descriptionRef.current) descriptionRef.current.value = "";
        }
    }

    async function handleImportApp(filename: string, data: string) {
        try {
            const app: AppModel = JSON.parse(data);
            if (app) {
                handleCreate(app);
                toast.info("Application created");
            }
        } catch {
            toast.error("Error importing the application");
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
                <TextareaAuto ref={descriptionRef} placeholder="Description" className="w-full" />
            </div>
            <div className="grid grid-cols-4 gap-4 mt-4">
                <Button variant="default" className="me-4 col-span-3" onClick={handleCreateApp}>
                    Create App
                </Button>
                <UploadButton
                    variant="secondary"
                    className="col-span-1"
                    handleUploadData={handleImportApp}
                    id={"import-app"}
                >                    
                    Import app
                    <i className="bi bi-filetype-json ms-1"/>
                    <i className="bi bi-arrow-up"/>
                </UploadButton>
            </div>
        </>
    );
}
