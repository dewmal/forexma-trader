import {
    createContext
} from "preact";
import {
    DashbboardPageUiState
} from "./ui/DashboardPageUiState";

export class RootStore {

    constructor() {
        this.dashboardUiState = new DashbboardPageUiState(this);
    }

}


export default createContext(new RootStore())