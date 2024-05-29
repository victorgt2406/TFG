import { atom } from 'nanostores';
import { getAppName } from './handleApp';
import { getTheme, type ThemeType } from './handleTheme';

const globalAppName = atom<string | undefined>(undefined)
const globalTheme = atom<ThemeType>("system")

export {globalAppName, globalTheme};