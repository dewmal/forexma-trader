import {
    makeAutoObservable
} from "mobx";
import moment from "moment";
import {
    createContext
} from "preact";

export class DashbboardPageUiState {

    currentTime;


    constructor() {
        makeAutoObservable(this);
        this.updateTime();
    }


    updateTime() {
        this.currentTime = moment.now()
        setTimeout(() => {
            this.updateTime()
        }, 1000);
    }


}
const DashboardPageUiContext = createContext(new DashbboardPageUiState());
export default DashboardPageUiContext;