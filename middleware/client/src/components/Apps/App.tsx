import { useRef, useState } from "react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../../@shadcn/components/ui/accordion";
import { Button } from "../../@shadcn/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../@shadcn/components/ui/card";
import type { AppModel } from "../../models/App";
import mdwApi from "../../utils/mdwApi";
import ContextMessages from "./ContextMessages";
import { toast } from "sonner";
import UploadDataButton from "./UploadDataButton";
import Fields from "./Fields";
import { Input } from "../../@shadcn/components/ui/input";
import { TextareaAuto } from "../TextareaAuto";
import { ScrollArea } from "../../@shadcn/components/ui/scroll-area";

type MyProps = Required<AppModel> & {
    handleDelete: () => void;
};

export default function App({
    name: defaultName,
    description: defaultDescription,
    terms: defaultTerms,
    conclusions: defaultConclusions,
    ignore_fields: defaultIgnoreFields,
    model,
    handleDelete,
}: MyProps) {
    const [isSaving, setSaving] = useState(false);
    const [isUploadingData, setUploadingData] = useState(false);
    const [terms, setTerms] = useState(defaultTerms);
    const [ignoreFields, setIgnoreFields] = useState(defaultIgnoreFields);
    const [conclusions, setConclusions] = useState(defaultConclusions);
    const [description, setDescription] = useState(defaultDescription);
    const [name, setName] = useState(defaultName);
    const [orig_name, setOrigName] = useState(defaultName);

    const textareaRef = useRef(null);

    async function handleSave() {
        setSaving(true);
        const app: AppModel = {
            orig_name: orig_name === name ? undefined : orig_name,
            name,
            description,
            terms,
            conclusions,
            ignore_fields: ignoreFields,
        };
        console.log({ ...app });
        const response = await mdwApi.patch("/apps/", app);
        setSaving(false);
        console.log(response);
        if (response.status === 200) toast.info("The app was successfully saved");
        else toast.warning("The app was successfully saved");

        setOrigName(name);
    }

    async function handleUploadData(filename: string, data: string) {
        // loader animation on
        setUploadingData(true);

        const formData = new FormData();
        const blobData = new Blob([data], { type: "text/plain" });

        formData.append("file", blobData, filename);

        try {
            const response = await mdwApi.post(`/apps/upload/${name}`, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            console.log(response);
            toast(`Uploaded ${response.data.total_docs} documents.`);
        } catch (error) {
            toast("Error uploading file");
            // console.error("Error uploading file:", error.response ? error.response.data : error.message);
        }
        // loader animation off
        setUploadingData(false);
    }

    return (
        <Card className="relative mt-2">
            <CardHeader className="">
                <div className="pt-5"></div>
                <Input
                    className="text-2xl font-semibold "
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <TextareaAuto
                    ref={textareaRef}
                    placeholder="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
            </CardHeader>
            <CardContent>
                <Accordion type="single" collapsible className="w-full">
                    <AccordionItem value="terms">
                        <AccordionTrigger>Terms</AccordionTrigger>
                        <ContextMessages
                            messages={terms}
                            setMessages={setTerms}
                            name={name}
                            model={model}
                            section="terms"
                        />
                    </AccordionItem>
                    <AccordionItem value="conclusion">
                        <AccordionTrigger>Conclusion</AccordionTrigger>
                        <ContextMessages
                            messages={conclusions}
                            setMessages={setConclusions}
                            name={name}
                            model={model}
                            section="conclusions"
                        />
                    </AccordionItem>
                    <AccordionItem value="fields">
                        <AccordionTrigger>Fields</AccordionTrigger>
                        <Fields name={name} ignoreFields={ignoreFields} setIgnoreFields={setIgnoreFields} />
                    </AccordionItem>
                </Accordion>
            </CardContent>
            <div className="absolute top-0 right-0 m-2 flex">
                <UploadDataButton handleUploadData={handleUploadData} className="h-8 w-25 me-3" variant={"secondary"}>
                    Upload data
                    <i
                        className={`ms-2 bi ${
                            isUploadingData ? "bi-arrow-clockwise animate-spin" : "bi-file-earmark-arrow-up-fill"
                        }`}
                    ></i>
                </UploadDataButton>
                <Button
                    className="h-8 w-8 me-1"
                    size="icon"
                    variant="secondary"
                    onClick={handleDelete}
                    disabled={isSaving}
                >
                    <i className="bi bi-trash3"></i>
                </Button>
                <Button className="h-8 w-8" size="icon" onClick={handleSave}>
                    <i className={`bi ${isSaving ? "bi-arrow-clockwise animate-spin" : "bi-floppy"}`}></i>
                </Button>
            </div>
        </Card>
    );
}
