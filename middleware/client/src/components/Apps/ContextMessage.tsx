import { useRef, useState } from "react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../../@shadcn/components/ui/select";
import type { LlmRoleType } from "../../models/LlmRole";
import { TextareaAuto } from "../TextareaAuto";
import { Button } from "../../@shadcn/components/ui/button";
import type { LlmMessageType } from "../../models/LlmMessage";
import { toast } from "sonner";

type MyProps = LlmMessageType & {
    handleUpdateContent: (content?: LlmMessageType) => Promise<void>;
};

export default function ContextMessage({
    role: defaultRole,
    content: defaultContent,
    handleUpdateContent,
}: MyProps) {
    const [role, setRole] = useState<LlmRoleType>(defaultRole);
    const contentRef = useRef<HTMLTextAreaElement>(null);

    async function handleSave() {
        const content = contentRef.current ? contentRef.current?.value : "";
        await handleUpdateContent({
            role,
            content,
        });
        console.log("save")
    }

    async function handleDelete() {
        await handleUpdateContent(undefined);
        console.log("delete")
    }

    return (
        <>
            <div className="flex mb-3">
                <Select
                    onValueChange={(value) => {
                        setRole(value as LlmRoleType);
                    }}
                    value={role}
                >
                    <SelectTrigger>
                        <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value={"user"}>User</SelectItem>
                        <SelectItem value={"assistant"}>Assistant</SelectItem>
                        <SelectItem value={"system"}>System</SelectItem>
                    </SelectContent>
                </Select>
                <Button className="mx-2" onClick={handleSave}>
                    <i className="bi bi-floppy"></i>
                </Button>
                <Button variant="destructive" onClick={handleDelete}>
                    <i className="bi bi-trash3"></i>
                </Button>
            </div>
            <TextareaAuto ref={contentRef} defaultValue={defaultContent} />
        </>
    );
}
