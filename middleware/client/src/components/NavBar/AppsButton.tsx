import { buttonVariants } from "../../@shadcn/components/ui/button";

export default function AppsButton({ className }: { className?: string }) {
    return (
        <a className={buttonVariants({ variant: "outline" }) + " " + className} href="/apps">
            <i className="bi bi-gear-fill"></i>
        </a>
    );
}
