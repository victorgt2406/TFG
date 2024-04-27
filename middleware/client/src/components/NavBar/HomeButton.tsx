import { buttonVariants } from "../../@shadcn/components/ui/button";

export default function HomeButton({ className }: { className: string }) {
    return (
        <a
            className={buttonVariants({ variant: "outline" }) + " " + className}
            href="/"
        >
            <i className="bi bi-house-door-fill"></i>
        </a>
    );
}
