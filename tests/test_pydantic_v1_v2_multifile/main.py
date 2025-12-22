import warnings

from fastapi import FastAPI

from . import modelsv1, modelsv2, modelsv2b

app = FastAPI()

with warnings.catch_warnings(record=True):
    warnings.simplefilter("always")

    @app.post("/v1-to-v2/item")
    def handle_v1_item_to_v2(data: modelsv1.Item) -> modelsv2.Item:
        return modelsv2.Item(
            new_title=data.title,
            new_size=data.size,
            new_description=data.description,
            new_sub=modelsv2.SubItem(new_sub_name=data.sub.name),
            new_multi=[modelsv2.SubItem(new_sub_name=s.name) for s in data.multi],
        )

    @app.post("/v2-to-v1/item")
    def handle_v2_item_to_v1(data: modelsv2.Item) -> modelsv1.Item:
        return modelsv1.Item(
            title=data.new_title,
            size=data.new_size,
            description=data.new_description,
            sub=modelsv1.SubItem(name=data.new_sub.new_sub_name),
            multi=[modelsv1.SubItem(name=s.new_sub_name) for s in data.new_multi],
        )

    @app.post("/v1-to-v2/item-to-list")
    def handle_v1_item_to_v2_list(data: modelsv1.Item) -> list[modelsv2.Item]:
        converted = modelsv2.Item(
            new_title=data.title,
            new_size=data.size,
            new_description=data.description,
            new_sub=modelsv2.SubItem(new_sub_name=data.sub.name),
            new_multi=[modelsv2.SubItem(new_sub_name=s.name) for s in data.multi],
        )
        return [converted, converted]

    @app.post("/v1-to-v2/list-to-list")
    def handle_v1_list_to_v2_list(data: list[modelsv1.Item]) -> list[modelsv2.Item]:
        result = []
        for item in data:
            result.append(
                modelsv2.Item(
                    new_title=item.title,
                    new_size=item.size,
                    new_description=item.description,
                    new_sub=modelsv2.SubItem(new_sub_name=item.sub.name),
                    new_multi=[
                        modelsv2.SubItem(new_sub_name=s.name) for s in item.multi
                    ],
                )
            )
        return result

    @app.post("/v1-to-v2/list-to-item")
    def handle_v1_list_to_v2_item(data: list[modelsv1.Item]) -> modelsv2.Item:
        if data:
            item = data[0]
            return modelsv2.Item(
                new_title=item.title,
                new_size=item.size,
                new_description=item.description,
                new_sub=modelsv2.SubItem(new_sub_name=item.sub.name),
                new_multi=[modelsv2.SubItem(new_sub_name=s.name) for s in item.multi],
            )
        return modelsv2.Item(
            new_title="", new_size=0, new_sub=modelsv2.SubItem(new_sub_name="")
        )

    @app.post("/v2-to-v1/item-to-list")
    def handle_v2_item_to_v1_list(data: modelsv2.Item) -> list[modelsv1.Item]:
        converted = modelsv1.Item(
            title=data.new_title,
            size=data.new_size,
            description=data.new_description,
            sub=modelsv1.SubItem(name=data.new_sub.new_sub_name),
            multi=[modelsv1.SubItem(name=s.new_sub_name) for s in data.new_multi],
        )
        return [converted, converted]

    @app.post("/v2-to-v1/list-to-list")
    def handle_v2_list_to_v1_list(data: list[modelsv2.Item]) -> list[modelsv1.Item]:
        result = []
        for item in data:
            result.append(
                modelsv1.Item(
                    title=item.new_title,
                    size=item.new_size,
                    description=item.new_description,
                    sub=modelsv1.SubItem(name=item.new_sub.new_sub_name),
                    multi=[
                        modelsv1.SubItem(name=s.new_sub_name) for s in item.new_multi
                    ],
                )
            )
        return result

    @app.post("/v2-to-v1/list-to-item")
    def handle_v2_list_to_v1_item(data: list[modelsv2.Item]) -> modelsv1.Item:
        if data:
            item = data[0]
            return modelsv1.Item(
                title=item.new_title,
                size=item.new_size,
                description=item.new_description,
                sub=modelsv1.SubItem(name=item.new_sub.new_sub_name),
                multi=[modelsv1.SubItem(name=s.new_sub_name) for s in item.new_multi],
            )
        return modelsv1.Item(title="", size=0, sub=modelsv1.SubItem(name=""))

    @app.post("/v2-to-v1/same-name")
    def handle_v2_same_name_to_v1(
        item1: modelsv2.Item, item2: modelsv2b.Item
    ) -> modelsv1.Item:
        return modelsv1.Item(
            title=item1.new_title,
            size=item2.dup_size,
            description=item1.new_description,
            sub=modelsv1.SubItem(name=item1.new_sub.new_sub_name),
            multi=[modelsv1.SubItem(name=s.dup_sub_name) for s in item2.dup_multi],
        )

    @app.post("/v2-to-v1/list-of-items-to-list-of-items")
    def handle_v2_items_in_list_to_v1_item_in_list(
        data1: list[modelsv2.ItemInList], data2: list[modelsv2b.ItemInList]
    ) -> list[modelsv1.ItemInList]:
        item1 = data1[0]
        item2 = data2[0]
        return [
            modelsv1.ItemInList(name1=item1.name2),
            modelsv1.ItemInList(name1=item2.dup_name2),
        ]
