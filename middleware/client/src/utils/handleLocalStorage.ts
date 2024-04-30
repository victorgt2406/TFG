
export default function handleLocalStorage(key:string, setValue:(value?:string)=>void){
    console.log("listener loaded", key)
    function localStorageListener (event:StorageEvent){
        console.log("listener")
        if (event.key === key) {
            const newValue = event.newValue || undefined
            setValue(newValue)
        }
    }
    window.addEventListener('storage', localStorageListener);
    return () => {
        window.removeEventListener('storage', localStorageListener);
    };
}
