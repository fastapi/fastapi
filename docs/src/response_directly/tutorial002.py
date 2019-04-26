from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()


@app.get("/legacy/")
def get_legacy_data():
    data = """
    <?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    <Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")
