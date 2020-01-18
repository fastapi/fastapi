from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

app = FastAPI()


class Invoice(BaseModel):
    id: str
    title: str = None
    customer: str
    total: float


class InvoiceEvent(BaseModel):
    description: str
    paid: bool


class InvoiceEventReceived(BaseModel):
    ok: bool


invoices_callback_router = APIRouter(default_response_class=JSONResponse)


@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived,
)
def invoice_notification(body: InvoiceEvent):
    pass


subrouter = APIRouter()


@subrouter.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: HttpUrl = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}


app.include_router(subrouter)

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/invoices/": {
            "post": {
                "summary": "Create Invoice",
                "description": 'Create an invoice.\n\nThis will (let\'s imagine) let the API user (some external developer) create an\ninvoice.\n\nAnd this path operation will:\n\n* Send the invoice to the client.\n* Collect the money from the client.\n* Send a notification back to the API user (the external developer), as a callback.\n    * At this point is that the API will somehow send a POST request to the\n        external API with the notification of the invoice event\n        (e.g. "payment successful").',
                "operationId": "create_invoice_invoices__post",
                "parameters": [
                    {
                        "required": False,
                        "schema": {
                            "title": "Callback Url",
                            "maxLength": 2083,
                            "minLength": 1,
                            "type": "string",
                            "format": "uri",
                        },
                        "name": "callback_url",
                        "in": "query",
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Invoice"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "callbacks": {
                    "invoice_notification": {
                        "{$callback_url}/invoices/{$request.body.id}": {
                            "post": {
                                "summary": "Invoice Notification",
                                "operationId": "invoice_notification__callback_url__invoices___request_body_id__post",
                                "requestBody": {
                                    "required": True,
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/InvoiceEvent"
                                            }
                                        }
                                    },
                                },
                                "responses": {
                                    "200": {
                                        "description": "Successful Response",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "$ref": "#/components/schemas/InvoiceEventReceived"
                                                }
                                            }
                                        },
                                    },
                                    "422": {
                                        "description": "Validation Error",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "$ref": "#/components/schemas/HTTPValidationError"
                                                }
                                            }
                                        },
                                    },
                                },
                            }
                        }
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                    }
                },
            },
            "Invoice": {
                "title": "Invoice",
                "required": ["id", "customer", "total"],
                "type": "object",
                "properties": {
                    "id": {"title": "Id", "type": "string"},
                    "title": {"title": "Title", "type": "string"},
                    "customer": {"title": "Customer", "type": "string"},
                    "total": {"title": "Total", "type": "number"},
                },
            },
            "InvoiceEvent": {
                "title": "InvoiceEvent",
                "required": ["description", "paid"],
                "type": "object",
                "properties": {
                    "description": {"title": "Description", "type": "string"},
                    "paid": {"title": "Paid", "type": "boolean"},
                },
            },
            "InvoiceEventReceived": {
                "title": "InvoiceEventReceived",
                "required": ["ok"],
                "type": "object",
                "properties": {"ok": {"title": "Ok", "type": "boolean"}},
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_openapi():
    with client:
        response = client.get("/openapi.json")

        assert response.json() == openapi_schema


def test_get():
    response = client.post(
        "/invoices/", json={"id": "fooinvoice", "customer": "John", "total": 5.3}
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Invoice received"}


def test_dummy_callback():
    # Just for coverage
    invoice_notification({})
