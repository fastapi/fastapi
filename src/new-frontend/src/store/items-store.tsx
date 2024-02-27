import { create } from 'zustand';
import { ItemCreate, ItemOut, ItemUpdate, ItemsService } from '../client';

interface ItemsStore {
    items: ItemOut[];
    getItems: () => Promise<void>;
    addItem: (item: ItemCreate) => Promise<void>;
    editItem: (id: number, item: ItemUpdate) => Promise<void>;
    deleteItem: (id: number) => Promise<void>;
    resetItems: () => void;
}

export const useItemsStore = create<ItemsStore>((set) => ({
    items: [],
    getItems: async () => {
        const itemsResponse = await ItemsService.readItems({ skip: 0, limit: 10 });
        set({ items: itemsResponse.data });
    },
    addItem: async (item: ItemCreate) => {
        const itemResponse = await ItemsService.createItem({ requestBody: item });
        set((state) => ({ items: [...state.items, itemResponse] }));
    },
    editItem: async (id: number, item: ItemUpdate) => {
        const itemResponse = await ItemsService.updateItem({ id: id, requestBody: item });
        set((state) => ({
            items: state.items.map((item) => (item.id === id ? itemResponse : item))
        }));
    },
    deleteItem: async (id: number) => {
        await ItemsService.deleteItem({ id });
        set((state) => ({ items: state.items.filter((item) => item.id !== id) }));
    },
    resetItems: () => {
        set({ items: [] });
    }
}));