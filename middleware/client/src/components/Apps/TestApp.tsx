import { useState } from "react";
import { AccordionContent } from "../../@shadcn/components/ui/accordion";
import { Input } from "../../@shadcn/components/ui/input";
import type { AppModel } from "../../models/App";
import { Label } from "../../@shadcn/components/ui/label";
import { Button } from "../../@shadcn/components/ui/button";
import handleLlm from "../../utils/handleLlm";
import handleSearch from "../../utils/handleSearch";
import stringToTerms from "../../utils/stringToTerrms";
import Markdown from "react-markdown";
import remarkGfm from 'remark-gfm'
import 'github-markdown-css'
import createConclusionQuery from "../../utils/createConclusionQuery";

export default function TestApp({
    conclusions: conclusionsContext,
    terms: termsContext,
    ignore_fields,
    name
}: Required<Pick<AppModel, "conclusions" | "terms" | "ignore_fields" | "name">>) {
    const [msg, setMsg] = useState("");
    const [terms, setTerms] = useState("");
    const [conclusion, setConclusion] = useState("");
    const [docs, setDocs] = useState<any[]>([]);
    
    const [termsTesting, setTermsTesting] = useState(false);
    const [docsTesting, setDocsTesting] = useState(false);
    const [conclusionTesting, setConclusionTesting] = useState(false);

    const docsString = "```json\n"+JSON.stringify(docs,null, 4)+"\n```"

    async function handleTerms() {
        setTermsTesting(true);
        const response = await handleLlm([...termsContext, {role: "user", content: msg}])
        if (response) {
            setTerms(response)
        }
        setTermsTesting(false);
    }

    async function handleDocs() {
        setDocsTesting(true);
        const cleanTerms = stringToTerms(terms);
        const cleanTermsString = cleanTerms.join(" ");
        const response =  await handleSearch(name, cleanTermsString, ignore_fields);
        if(response){
            setDocs(response)
        }
        setDocsTesting(false);
    }

    async function handleConclusion() {
        setConclusionTesting(true);
        // const response = await handleLlm([...conclusionsContext, {role: "user", content: `**Docs**: ${JSON.stringify(docs,null, 4)}\n**User Message**: "${msg}"`}])
        const response = await handleLlm([...conclusionsContext, {role: "user", content: createConclusionQuery(msg, docs)}])
        if (response) {
            setConclusion(response)
        }
        setConclusionTesting(false);
    }


    return (
        <AccordionContent className="p-2">
            <div className="w-full grid grid-cols-5 gap-1.5 mb-2">
                <div className="items-center gap-1.5 col-span-4">
                    <Label>Message</Label>
                    <Input
                        type="text"
                        placeholder="User message..."
                        value={msg}
                        onChange={(e) => setMsg(e.target.value)}
                    />
                </div>
                <Button className="mt-[18.56px] min-w-[55px]" variant="secondary" onClick={handleTerms} disabled={termsTesting}>
                    Get Terms <i className={`ms-2 bi ${termsTesting ? "bi-arrow-clockwise animate-spin" : "bi-send"}`}></i>
                </Button>
            </div>
            <div className="items-center gap-1.5 col-span-4 my-2">
                <Label>Terms</Label>
                <Input
                    type="text"
                    placeholder="Terms from the message..."
                    value={terms}
                    onChange={(e) => setTerms(e.target.value)}
                />
            </div>
            <div className="w-full grid grid-cols-5 gap-1.5 my-2 items-center">
                <h3 className="text-large font-semibold col-span-4">Documents</h3>
                <Button variant="secondary" onClick={handleDocs} disabled={docsTesting}>
                    Get documents
                    <i className={`ms-2 bi ${docsTesting ? "bi-arrow-clockwise animate-spin" : "bi-send"}`}></i>
                </Button>
            </div>
            <Markdown remarkPlugins={[remarkGfm]} className="markdown-body">
                {"```json\n"+JSON.stringify(docs,null, 4)+"\n```"}
            </Markdown>
            <div className="w-full grid grid-cols-5 gap-1.5 my-2 items-center">
                <h3 className="text-large font-semibold col-span-4">Conclusion</h3>
                <Button variant="secondary" disabled={conclusionTesting} onClick={handleConclusion}>
                    Get conclusion
                    <i className={`ms-2 bi ${conclusionTesting ? "bi-arrow-clockwise animate-spin" : "bi-send"}`}></i>
                </Button>
            </div>
            <Markdown remarkPlugins={[remarkGfm]} className="markdown-body">
                {conclusion}
            </Markdown>
        </AccordionContent>
    );
}
