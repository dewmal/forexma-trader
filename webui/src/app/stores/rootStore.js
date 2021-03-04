import {
    createContext
} from "preact";
import {
    DashboardPageUiState
} from "./ui/DashboardPageUiState";


export const globalContext = createContext();

export const GlobalProvider = ({ children }) => {
    const uiStore = new DashboardPageUiState();

    return (
        <globalContext.Provider value={{ uiStore }}>
            {children}
        </globalContext.Provider>
    );
};