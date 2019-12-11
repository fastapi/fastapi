from starlette.testclient import TestClient

from openapi_callbacks.tutorial001 import app, invoice_notification

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/invoices/": {
            "post": {
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
                "summary": "Create Invoice",
                "operationId": "create_invoice_invoices__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Invoice"}
                        }
                    },
                    "required": True,
                },
                "callbacks": {
                    "invoice_notification": {
                        "/invoices/{$request.body.id}": {
                            "post": {
                                "summary": "Invoice Notification",
                                "operationId": "invoice_notification_invoices___request_body_id__post",
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
                    "customer": {"title": "Customer", "type": "string"},
                    "total": {"title": "Total", "type": "number"},
                    "title": {"title": "Title", "type": "string"},
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
