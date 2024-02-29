from typing import List, Mapping

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/query/mixed-type-params")
def get_mixed_mapping_mixed_type_query_params(
    query: int = Query(),
    mapping_query_str: Mapping[str, str] = Query({}),
    mapping_query_int: Mapping[str, int] = Query({}),
    sequence_mapping_queries: Mapping[str, List[int]] = Query({}),
):
    return {
        "query": query,
        "string_mapping": mapping_query_str,
        "mapping_query_int": mapping_query_int,
        "sequence_mapping_queries": sequence_mapping_queries,
    }
