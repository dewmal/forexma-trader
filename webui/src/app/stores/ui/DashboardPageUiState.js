import {
    makeAutoObservable
} from "mobx";
import moment from "moment";
import io from "socket.io-client";

export class DashbboardPageUiState {

    currentTime;
    marketStatus = {
        close: 0,
        date: null,
        unix: null,
        asset: null
    };
    socket;

    constructor() {
        makeAutoObservable(this);
        this.startSocket();
    }

    startSocket() {
        this.socket = io("ws://127.0.0.1:7979", {
            transports: ["websocket"],
            jsonp: true,
            forceNew: true,
        });
    }


    readSocket() {
        this.socket.on("HistoryDataReadingAgent", (evt) => {
            const newStatus = evt.body.message;
            this.changeAssetPrice(newStatus)
        });
    }

    changeAssetPrice(status) {
        this.marketStatus = status;
        this.currentTime = moment.now();
    }



}