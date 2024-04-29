import { useState } from "react";
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "../../@shadcn/components/ui/accordion";
import { Button } from "../../@shadcn/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "../../@shadcn/components/ui/card";
import type { AppModel } from "../../models/App";
import mdwApi from "../../utils/mdwApi";
import AppContent from "./AppContent";
import { toast } from "sonner";

type MyProps = Required<AppModel> & {
    handleDelete:()=>void
}

export default function App({
    name,
    description,
    terms: defaultTerms,
    conclusions: defaultConclusions,
    model,
    handleDelete
}: MyProps) {
    const [isSaving, setSaving] = useState(false);
    const [terms, setTerms] = useState(defaultTerms);
    const [conclusions, setConclusions] = useState(defaultConclusions);

    async function handleSave() {
        setSaving(true);
        const app: AppModel = {
            name,
            description,
            terms,
            conclusions,
        };
        console.log({ ...app });
        const response = await mdwApi.post("/apps/", {
            name,
            description,
            terms,
            conclusions,
        });
        setSaving(false);
        console.log(response);
        if (response.status === 200)
            toast.info("The app was successfully saved");
        else toast.warning("The app was successfully saved");
        
    }

    // async function handleDelete() {
    //     const response = await mdwApi.delete(`/apps/${name}`);
    //     console.log(response);
    // }

    return (
        <Card className="relative mt-2">
            <CardHeader className="pr-20">
                <CardTitle>{name}</CardTitle>
                <CardDescription>{description}</CardDescription>
            </CardHeader>
            <CardContent>
                <Accordion type="single" collapsible className="w-full">
                    <AccordionItem value="terms">
                        <AccordionTrigger>Terms</AccordionTrigger>
                        <AppContent
                            messages={terms}
                            setMessages={setTerms}
                            name={name}
                            model={model}
                            section="terms"
                        />
                    </AccordionItem>
                    <AccordionItem value="conclusion">
                        <AccordionTrigger>Conclusion</AccordionTrigger>
                        <AppContent
                            messages={conclusions}
                            setMessages={setConclusions}
                            name={name}
                            model={model}
                            section="conclusions"
                        />
                    </AccordionItem>
                </Accordion>
                {/* <AppContent conclusions={conclusions} terms={terms} /> */}
            </CardContent>
            <div className="absolute top-0 right-0 m-2">
                <Button
                    className="h-8 w-8 me-1"
                    size="icon"
                    onClick={handleSave}
                >
                    <i className={`bi ${isSaving?"bi-arrow-clockwise animate-spin":"bi-floppy"}`}></i>
                </Button>
                <Button
                    className="h-8 w-8"
                    size="icon"
                    variant="destructive"
                    onClick={handleDelete}
                    disabled={isSaving}
                >
                    <i className="bi bi-trash3"></i>
                </Button>
            </div>
        </Card>
    );
}
