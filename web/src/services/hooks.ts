import { useState } from "react";
import { container } from "../inversify/inversify.config";

export function useInject<T>(id: string | symbol): T {
    const [store, setStore] = useState(() => {
        return container.get<T>(id);
    });
    return store;
}