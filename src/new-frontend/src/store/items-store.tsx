import { create } from "zustand";
import { ItemCreate, ItemOut, ItemsService } from "../client";

interface ItemsStore { 
    items: ItemOut[];
    getItems: () => Promise<void>;
    addItem: (item: ItemCreate) => Promise<void>;
    deleteItem: (id: number) => Promise<void>;
}

export const useItemsStore = create<ItemsStore>((set) => ({
    items: [],
    getItems: async () => {
        const itemsResponse = await ItemsService.readItems({ skip: 0, limit: 10 });
        set({ items: itemsResponse });
    },
    addItem: async (item: ItemCreate) => {
        const itemResponse = await ItemsService.createItem({ requestBody: item});
        set((state) => ({ items: [...state.items, itemResponse] }));
    },
    deleteItem: async (id: number) => {
        await ItemsService.deleteItem({ id });
        set((state) => ({ items: state.items.filter((item) => item.id !== id) }));
    }
}));