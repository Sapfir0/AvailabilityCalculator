import { injectable } from "inversify";
import { action, makeObservable, observable } from "mobx";
import { Bufferization, TravelMode } from "../typing";

@injectable()
export class MapStore {
    maxDuration = '10';
    travelMode = TravelMode[TravelMode.walking] 
    bufferization = Bufferization[Bufferization.isochrones]

    constructor() {
        makeObservable(this, {
            setMaxDuration: action,
            setTravelMode: action,
            setBufferizationMode: action,
            maxDuration: observable,
            travelMode: observable,
            bufferization: observable,
        })
    }

    setTravelMode = (travelMode: string) => {
        this.travelMode = travelMode 
    }

    setBufferizationMode = (bufferization: string) => {
        this.bufferization = bufferization 
    }

    setMaxDuration = (maxDuration: string) => {
        this.maxDuration = maxDuration
    }
}