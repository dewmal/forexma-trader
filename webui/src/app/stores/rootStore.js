import {
    createContext
} from "preact";
import {
    DashbboardPageUiState
} from "./ui/DashboardPageUiState";


export const globalContext = createContext();

export const GlobalProvider = ({ children }) => {
    const uiStore = new DashbboardPageUiState();

    return (
        <globalContext.Provider value={{ uiStore }}>
            {children}
        </globalContext.Provider>
    );
};