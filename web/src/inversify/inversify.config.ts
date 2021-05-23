import { Container } from "inversify";
import 'reflect-metadata';
import { MapStore } from "../Map/MapStore";
import { TYPES } from "./types";

const container = new Container();

container.bind<MapStore>(TYPES.MapStore).to(MapStore).inSingletonScope();


export { container };
