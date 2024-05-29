import React, { useState } from "react";
import { Button } from "../../@shadcn/components/ui/button";

type MyProps = {
    handleUploadData: (filename: string, data: string) => Promise<void>;
    className: string;
    variant?: "link" | "default" | "destructive" | "outline" | "secondary" | "ghost" | null | undefined,
    children: React.ReactNode
};

export default function UploadDataButton({ handleUploadData, className, variant, children }: MyProps) {
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            const filename: string = file.name;
            const reader = new FileReader();
            reader.onload = async (e) => {
                const data: string = e.target?.result as string;
                await handleUploadData(filename, data);
            };
            reader.readAsText(file);
        }
    };
    const handleButtonClick = () => {
        document.getElementById("fileInput")!.click();
    };
    return (
        <div>
            <input type="file" id="fileInput" style={{ display: "none" }} onChange={handleFileChange} />
            <Button onClick={handleButtonClick} className={className} variant={variant}>
                {children}
            </Button>
        </div>
    );
}
