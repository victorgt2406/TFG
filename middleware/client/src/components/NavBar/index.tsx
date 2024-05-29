import DarkModeButton from "./DarkModeSelect";
import Settings from "./Settings";
import AppsSelect from "./AppsSelect";
import HomeButton from "./HomeButton";


export default  function NavBar() {
    return (
        <div className="flex flex-row-reverse w-full text-xs p-2">
            <Settings className="ms-2"/>
            <DarkModeButton className="ms-2"/>
            <AppsSelect className="ms-2"/>
            <HomeButton className="me-auto"/>
        </div>
    )
}

