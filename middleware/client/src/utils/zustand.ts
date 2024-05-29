import { create } from "zustand";
import { getAppName } from "./handleApp";
import { getTheme, type ThemeType } from "./handleTheme";

type ZustandProps = {
    theme: ThemeType;
    setTheme: (theme: ThemeType) => void;
    app: string | undefined;
    setApp: (app: string | undefined) => void;
};

const useStore = create<ZustandProps>((set) => ({
    theme: getTheme(),
    setTheme: (theme) => set(() => ({ theme:theme })),
    app: getAppName(),
    setApp: (app) => set(() => ({ app:app })),
}));

export default useStore;
