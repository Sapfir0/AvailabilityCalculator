import { injectable } from "inversify";
import { action, makeObservable, observable } from "mobx";
import { TravelMode } from "../typing";

@injectable()
export class MapStore {
    maxDuration = '10';
    travelMode = TravelMode[TravelMode.walking] 

    constructor() {
        makeObservable(this, {
            setMaxDuration: action,
            setTravelMode: action,
            maxDuration: observable,
            travelMode: observable,
        })
    }

    setTravelMode = (travelMode: string) => {
        this.travelMode = travelMode 
    }

    setMaxDuration = (maxDuration: string) => {
        this.maxDuration = maxDuration
    }
}