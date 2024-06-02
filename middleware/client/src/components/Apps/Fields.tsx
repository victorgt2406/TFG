import { useEffect, useState } from "react";
import { AccordionContent } from "../../@shadcn/components/ui/accordion";
import { Label } from "../../@shadcn/components/ui/label";
import { Switch } from "../../@shadcn/components/ui/switch";
import mdwApi from "../../utils/mdwApi";
import type { Key } from "lucide-react";

type FieldProps = {
    name: string;
    on: boolean;
    onChange: (on: boolean) => void;
};

function Field({ name, on, onChange }: FieldProps) {
    return (
        <div className="flex items-center space-x-2 my-1">
            <Switch
                id={`field-${name}`}
                onCheckedChange={onChange}
                defaultChecked={on}
            />
            <Label htmlFor={`field-${name}`}>{name}</Label>
        </div>
    );
}

type MyProps = {
    name: string;
    ignoreFields: string[];
    setIgnoreFields: (fields: string[]) => void;
};

export default function Fields({ name, ignoreFields, setIgnoreFields }: MyProps) {
    const [fields, setFields] = useState<string[]>([]);

    useEffect(() => {
        async function loadAppFields() {
            const response = await mdwApi.get("/search/fields/" + name);
            
            if (response.status === 200) {
                const fields = response.data as string[];
                setFields(fields);
            }
        }
        loadAppFields();
    }, [fields]);

    const fieldComponents = fields.map((field, index) => (
        <Field
            name={field}
            on={!ignoreFields.includes(field)}
            key={index}
            onChange={(on: boolean) => {
                if (!on) {
                    setIgnoreFields([...new Set([...ignoreFields, field])]);
                } else {
                    setIgnoreFields(ignoreFields.filter((ignoreField) => ignoreField !== field));
                }
            }}
        />
    ));

    return <AccordionContent className="p-2">{fieldComponents}</AccordionContent>;
}
