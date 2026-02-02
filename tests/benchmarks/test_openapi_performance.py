"""
Benchmark tests for OpenAPI schema generation performance.

This module tests OpenAPI schema generation with large numbers of routes
and Pydantic models to identify performance bottlenecks and verify
optimizations.

Run with: pytest tests/benchmarks/test_openapi_performance.py -v
Or with profiling: pytest tests/benchmarks/test_openapi_performance.py -v -s
"""

import time
from collections.abc import Iterator
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional, Union
from uuid import UUID

import pytest
from fastapi import Depends, FastAPI, Path, Query
from fastapi.openapi._profiling import ProfilingContext
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


# =============================================================================
# Pydantic Models (50+ unique models with nested structures)
# =============================================================================


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    ARCHIVED = "archived"


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


class ContactInfo(BaseModel):
    email: str
    phone: Optional[str] = None
    address: Optional[Address] = None


class BaseEntity(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None


class User(UserBase, BaseEntity):
    is_active: bool = True
    role: str = "user"
    contact: Optional[ContactInfo] = None


class UserWithProfile(User):
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    social_links: dict[str, str] = Field(default_factory=dict)


class Tag(BaseModel):
    name: str
    color: Optional[str] = None


class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    sku: str


class ProductCreate(ProductBase):
    category_id: int
    tags: list[str] = Field(default_factory=list)


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class Product(ProductBase, BaseEntity):
    category: Optional[Category] = None
    tags: list[Tag] = Field(default_factory=list)
    status: StatusEnum = StatusEnum.ACTIVE
    inventory_count: int = 0


class OrderItem(BaseModel):
    product_id: UUID
    quantity: int = Field(..., ge=1)
    unit_price: float
    discount: float = 0.0


class OrderBase(BaseModel):
    customer_id: UUID
    shipping_address: Address
    billing_address: Optional[Address] = None


class OrderCreate(OrderBase):
    items: list[OrderItem]
    notes: Optional[str] = None


class Order(OrderBase, BaseEntity):
    items: list[OrderItem]
    status: StatusEnum = StatusEnum.PENDING
    total_amount: float
    tax_amount: float
    shipping_cost: float


class PaymentMethod(BaseModel):
    type: str
    last_four: str
    expiry_month: int
    expiry_year: int


class Payment(BaseEntity):
    order_id: UUID
    amount: float
    method: PaymentMethod
    status: StatusEnum


class Review(BaseEntity):
    product_id: UUID
    user_id: UUID
    rating: int = Field(..., ge=1, le=5)
    title: str
    content: str
    helpful_count: int = 0


class Notification(BaseEntity):
    user_id: UUID
    title: str
    message: str
    is_read: bool = False
    priority: PriorityEnum = PriorityEnum.MEDIUM


class AuditLog(BaseEntity):
    action: str
    entity_type: str
    entity_id: UUID
    user_id: UUID
    changes: dict[str, Any]


class Settings(BaseModel):
    theme: str = "light"
    language: str = "en"
    notifications_enabled: bool = True
    email_preferences: dict[str, bool] = Field(default_factory=dict)


class Analytics(BaseModel):
    page_views: int
    unique_visitors: int
    bounce_rate: float
    avg_session_duration: float
    top_pages: list[str]


class Report(BaseEntity):
    name: str
    type: str
    parameters: dict[str, Any]
    data: Analytics
    generated_by: UUID


class Webhook(BaseEntity):
    url: str
    events: list[str]
    is_active: bool = True
    secret: Optional[str] = None


class ApiKey(BaseEntity):
    name: str
    key_prefix: str
    scopes: list[str]
    expires_at: Optional[datetime] = None


class RateLimit(BaseModel):
    requests_per_minute: int
    requests_per_hour: int
    requests_per_day: int


class Subscription(BaseEntity):
    user_id: UUID
    plan: str
    status: StatusEnum
    rate_limits: RateLimit
    features: list[str]


class Invoice(BaseEntity):
    subscription_id: UUID
    amount: float
    status: StatusEnum
    due_date: datetime
    paid_at: Optional[datetime] = None


class Team(BaseEntity):
    name: str
    description: Optional[str] = None
    members: list[UUID]
    owner_id: UUID


class Project(BaseEntity):
    name: str
    description: Optional[str] = None
    team_id: UUID
    status: StatusEnum
    priority: PriorityEnum


class Task(BaseEntity):
    title: str
    description: Optional[str] = None
    project_id: UUID
    assignee_id: Optional[UUID] = None
    status: StatusEnum
    priority: PriorityEnum
    due_date: Optional[datetime] = None


class Comment(BaseEntity):
    task_id: UUID
    user_id: UUID
    content: str
    parent_id: Optional[UUID] = None


class Attachment(BaseEntity):
    task_id: UUID
    filename: str
    file_url: str
    file_size: int
    mime_type: str


class PaginatedResponse(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
    has_more: bool


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[dict[str, Any]] = None


class HealthCheck(BaseModel):
    status: str
    version: str
    uptime: float
    components: dict[str, str]


# =============================================================================
# Dependencies
# =============================================================================


def get_current_user() -> User:
    return User(
        id="00000000-0000-0000-0000-000000000001",
        username="testuser",
        email="test@example.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def get_pagination(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> dict[str, int]:
    return {"page": page, "page_size": page_size}


CurrentUser = Annotated[User, Depends(get_current_user)]
Pagination = Annotated[dict[str, int], Depends(get_pagination)]


# =============================================================================
# Create Large Application with 100+ Routes
# =============================================================================


def create_large_app() -> FastAPI:
    """Create a FastAPI app with 100+ routes and 50+ models."""
    app = FastAPI(
        title="Large Benchmark API",
        description="API for benchmarking OpenAPI generation",
        version="1.0.0",
    )

    # User routes (10 routes)
    @app.get("/users", response_model=list[User], tags=["Users"])
    def list_users(pagination: Pagination):
        return []

    @app.post("/users", response_model=User, tags=["Users"])
    def create_user(user: UserCreate):
        pass

    @app.get("/users/{user_id}", response_model=UserWithProfile, tags=["Users"])
    def get_user(user_id: UUID = Path(...)):
        pass

    @app.put("/users/{user_id}", response_model=User, tags=["Users"])
    def update_user(user_id: UUID, user: UserUpdate):
        pass

    @app.delete("/users/{user_id}", tags=["Users"])
    def delete_user(user_id: UUID):
        pass

    @app.get("/users/{user_id}/settings", response_model=Settings, tags=["Users"])
    def get_user_settings(user_id: UUID):
        pass

    @app.put("/users/{user_id}/settings", response_model=Settings, tags=["Users"])
    def update_user_settings(user_id: UUID, settings: Settings):
        pass

    @app.get(
        "/users/{user_id}/notifications",
        response_model=list[Notification],
        tags=["Users"],
    )
    def get_user_notifications(user_id: UUID, pagination: Pagination):
        return []

    @app.get("/users/me", response_model=UserWithProfile, tags=["Users"])
    def get_current_user_profile(current_user: CurrentUser):
        return current_user

    @app.get("/users/search", response_model=list[User], tags=["Users"])
    def search_users(
        q: str = Query(..., min_length=1),
        pagination: Pagination = None,
    ):
        return []

    # Product routes (15 routes)
    @app.get("/products", response_model=list[Product], tags=["Products"])
    def list_products(
        category_id: Optional[int] = None,
        status: Optional[StatusEnum] = None,
        pagination: Pagination = None,
    ):
        return []

    @app.post("/products", response_model=Product, tags=["Products"])
    def create_product(product: ProductCreate, current_user: CurrentUser):
        pass

    @app.get("/products/{product_id}", response_model=Product, tags=["Products"])
    def get_product(product_id: UUID):
        pass

    @app.put("/products/{product_id}", response_model=Product, tags=["Products"])
    def update_product(product_id: UUID, product: ProductUpdate):
        pass

    @app.delete("/products/{product_id}", tags=["Products"])
    def delete_product(product_id: UUID):
        pass

    @app.get(
        "/products/{product_id}/reviews",
        response_model=list[Review],
        tags=["Products"],
    )
    def get_product_reviews(product_id: UUID, pagination: Pagination):
        return []

    @app.post(
        "/products/{product_id}/reviews", response_model=Review, tags=["Products"]
    )
    def create_product_review(
        product_id: UUID,
        rating: int = Query(..., ge=1, le=5),
        title: str = Query(...),
        content: str = Query(...),
        current_user: CurrentUser = None,
    ):
        pass

    @app.get("/products/featured", response_model=list[Product], tags=["Products"])
    def get_featured_products():
        return []

    @app.get("/products/search", response_model=list[Product], tags=["Products"])
    def search_products(
        q: str = Query(...),
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        pagination: Pagination = None,
    ):
        return []

    @app.get(
        "/products/categories", response_model=list[Category], tags=["Products"]
    )
    def list_categories():
        return []

    @app.post("/products/categories", response_model=Category, tags=["Products"])
    def create_category(category: Category):
        pass

    @app.get(
        "/products/categories/{category_id}",
        response_model=Category,
        tags=["Products"],
    )
    def get_category(category_id: int):
        pass

    @app.get("/products/tags", response_model=list[Tag], tags=["Products"])
    def list_tags():
        return []

    @app.post("/products/tags", response_model=Tag, tags=["Products"])
    def create_tag(tag: Tag):
        pass

    @app.get(
        "/products/{product_id}/related",
        response_model=list[Product],
        tags=["Products"],
    )
    def get_related_products(product_id: UUID):
        return []

    # Order routes (12 routes)
    @app.get("/orders", response_model=list[Order], tags=["Orders"])
    def list_orders(
        status: Optional[StatusEnum] = None,
        pagination: Pagination = None,
        current_user: CurrentUser = None,
    ):
        return []

    @app.post("/orders", response_model=Order, tags=["Orders"])
    def create_order(order: OrderCreate, current_user: CurrentUser):
        pass

    @app.get("/orders/{order_id}", response_model=Order, tags=["Orders"])
    def get_order(order_id: UUID):
        pass

    @app.put("/orders/{order_id}/status", response_model=Order, tags=["Orders"])
    def update_order_status(order_id: UUID, status: StatusEnum):
        pass

    @app.delete("/orders/{order_id}", tags=["Orders"])
    def cancel_order(order_id: UUID):
        pass

    @app.get(
        "/orders/{order_id}/payments", response_model=list[Payment], tags=["Orders"]
    )
    def get_order_payments(order_id: UUID):
        return []

    @app.post("/orders/{order_id}/payments", response_model=Payment, tags=["Orders"])
    def create_payment(order_id: UUID, method: PaymentMethod):
        pass

    @app.get(
        "/orders/{order_id}/invoice", response_model=Invoice, tags=["Orders"]
    )
    def get_order_invoice(order_id: UUID):
        pass

    @app.get("/orders/stats", response_model=Analytics, tags=["Orders"])
    def get_order_stats(
        start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ):
        pass

    @app.get("/orders/recent", response_model=list[Order], tags=["Orders"])
    def get_recent_orders(limit: int = Query(10, ge=1, le=50)):
        return []

    @app.get(
        "/orders/{order_id}/tracking", response_model=dict[str, Any], tags=["Orders"]
    )
    def get_order_tracking(order_id: UUID):
        return {}

    @app.post("/orders/{order_id}/refund", response_model=Payment, tags=["Orders"])
    def request_refund(order_id: UUID, reason: str = Query(...)):
        pass

    # Team/Project routes (20 routes)
    @app.get("/teams", response_model=list[Team], tags=["Teams"])
    def list_teams(pagination: Pagination):
        return []

    @app.post("/teams", response_model=Team, tags=["Teams"])
    def create_team(name: str, description: Optional[str] = None):
        pass

    @app.get("/teams/{team_id}", response_model=Team, tags=["Teams"])
    def get_team(team_id: UUID):
        pass

    @app.put("/teams/{team_id}", response_model=Team, tags=["Teams"])
    def update_team(team_id: UUID, name: Optional[str] = None):
        pass

    @app.delete("/teams/{team_id}", tags=["Teams"])
    def delete_team(team_id: UUID):
        pass

    @app.get(
        "/teams/{team_id}/members", response_model=list[User], tags=["Teams"]
    )
    def get_team_members(team_id: UUID):
        return []

    @app.post("/teams/{team_id}/members", tags=["Teams"])
    def add_team_member(team_id: UUID, user_id: UUID):
        pass

    @app.delete("/teams/{team_id}/members/{user_id}", tags=["Teams"])
    def remove_team_member(team_id: UUID, user_id: UUID):
        pass

    @app.get(
        "/teams/{team_id}/projects", response_model=list[Project], tags=["Teams"]
    )
    def get_team_projects(team_id: UUID, pagination: Pagination):
        return []

    @app.post(
        "/teams/{team_id}/projects", response_model=Project, tags=["Teams"]
    )
    def create_project(team_id: UUID, name: str, description: Optional[str] = None):
        pass

    @app.get("/projects/{project_id}", response_model=Project, tags=["Projects"])
    def get_project(project_id: UUID):
        pass

    @app.put("/projects/{project_id}", response_model=Project, tags=["Projects"])
    def update_project(
        project_id: UUID,
        name: Optional[str] = None,
        status: Optional[StatusEnum] = None,
    ):
        pass

    @app.delete("/projects/{project_id}", tags=["Projects"])
    def delete_project(project_id: UUID):
        pass

    @app.get(
        "/projects/{project_id}/tasks", response_model=list[Task], tags=["Projects"]
    )
    def get_project_tasks(
        project_id: UUID,
        status: Optional[StatusEnum] = None,
        pagination: Pagination = None,
    ):
        return []

    @app.post("/projects/{project_id}/tasks", response_model=Task, tags=["Projects"])
    def create_task(
        project_id: UUID,
        title: str,
        description: Optional[str] = None,
        priority: PriorityEnum = PriorityEnum.MEDIUM,
    ):
        pass

    @app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
    def get_task(task_id: UUID):
        pass

    @app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
    def update_task(
        task_id: UUID,
        title: Optional[str] = None,
        status: Optional[StatusEnum] = None,
        priority: Optional[PriorityEnum] = None,
    ):
        pass

    @app.delete("/tasks/{task_id}", tags=["Tasks"])
    def delete_task(task_id: UUID):
        pass

    @app.get(
        "/tasks/{task_id}/comments", response_model=list[Comment], tags=["Tasks"]
    )
    def get_task_comments(task_id: UUID):
        return []

    @app.post("/tasks/{task_id}/comments", response_model=Comment, tags=["Tasks"])
    def add_task_comment(task_id: UUID, content: str):
        pass

    # Subscription/Billing routes (10 routes)
    @app.get("/subscriptions", response_model=list[Subscription], tags=["Billing"])
    def list_subscriptions(current_user: CurrentUser):
        return []

    @app.post("/subscriptions", response_model=Subscription, tags=["Billing"])
    def create_subscription(plan: str, current_user: CurrentUser):
        pass

    @app.get(
        "/subscriptions/{subscription_id}",
        response_model=Subscription,
        tags=["Billing"],
    )
    def get_subscription(subscription_id: UUID):
        pass

    @app.put(
        "/subscriptions/{subscription_id}",
        response_model=Subscription,
        tags=["Billing"],
    )
    def update_subscription(subscription_id: UUID, plan: str):
        pass

    @app.delete("/subscriptions/{subscription_id}", tags=["Billing"])
    def cancel_subscription(subscription_id: UUID):
        pass

    @app.get(
        "/subscriptions/{subscription_id}/invoices",
        response_model=list[Invoice],
        tags=["Billing"],
    )
    def get_subscription_invoices(subscription_id: UUID):
        return []

    @app.get("/invoices/{invoice_id}", response_model=Invoice, tags=["Billing"])
    def get_invoice(invoice_id: UUID):
        pass

    @app.post("/invoices/{invoice_id}/pay", response_model=Invoice, tags=["Billing"])
    def pay_invoice(invoice_id: UUID, method: PaymentMethod):
        pass

    @app.get("/billing/methods", response_model=list[PaymentMethod], tags=["Billing"])
    def list_payment_methods(current_user: CurrentUser):
        return []

    @app.post("/billing/methods", response_model=PaymentMethod, tags=["Billing"])
    def add_payment_method(method: PaymentMethod, current_user: CurrentUser):
        pass

    # API Management routes (10 routes)
    @app.get("/api-keys", response_model=list[ApiKey], tags=["API"])
    def list_api_keys(current_user: CurrentUser):
        return []

    @app.post("/api-keys", response_model=ApiKey, tags=["API"])
    def create_api_key(name: str, scopes: list[str], current_user: CurrentUser):
        pass

    @app.delete("/api-keys/{key_id}", tags=["API"])
    def revoke_api_key(key_id: UUID):
        pass

    @app.get("/webhooks", response_model=list[Webhook], tags=["API"])
    def list_webhooks(current_user: CurrentUser):
        return []

    @app.post("/webhooks", response_model=Webhook, tags=["API"])
    def create_webhook(url: str, events: list[str], current_user: CurrentUser):
        pass

    @app.get("/webhooks/{webhook_id}", response_model=Webhook, tags=["API"])
    def get_webhook(webhook_id: UUID):
        pass

    @app.put("/webhooks/{webhook_id}", response_model=Webhook, tags=["API"])
    def update_webhook(webhook_id: UUID, url: Optional[str] = None):
        pass

    @app.delete("/webhooks/{webhook_id}", tags=["API"])
    def delete_webhook(webhook_id: UUID):
        pass

    @app.post("/webhooks/{webhook_id}/test", tags=["API"])
    def test_webhook(webhook_id: UUID):
        pass

    @app.get("/rate-limits", response_model=RateLimit, tags=["API"])
    def get_rate_limits(current_user: CurrentUser):
        pass

    # Admin/Analytics routes (15 routes)
    @app.get("/admin/users", response_model=list[User], tags=["Admin"])
    def admin_list_users(
        status: Optional[str] = None, pagination: Pagination = None
    ):
        return []

    @app.get("/admin/audit-logs", response_model=list[AuditLog], tags=["Admin"])
    def get_audit_logs(
        entity_type: Optional[str] = None,
        user_id: Optional[UUID] = None,
        pagination: Pagination = None,
    ):
        return []

    @app.get("/admin/reports", response_model=list[Report], tags=["Admin"])
    def list_reports(pagination: Pagination):
        return []

    @app.post("/admin/reports", response_model=Report, tags=["Admin"])
    def create_report(name: str, type: str, parameters: dict[str, Any]):
        pass

    @app.get("/admin/reports/{report_id}", response_model=Report, tags=["Admin"])
    def get_report(report_id: UUID):
        pass

    @app.get("/admin/analytics", response_model=Analytics, tags=["Admin"])
    def get_analytics(
        start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ):
        pass

    @app.get(
        "/admin/analytics/users", response_model=dict[str, Any], tags=["Admin"]
    )
    def get_user_analytics():
        return {}

    @app.get(
        "/admin/analytics/products", response_model=dict[str, Any], tags=["Admin"]
    )
    def get_product_analytics():
        return {}

    @app.get(
        "/admin/analytics/orders", response_model=dict[str, Any], tags=["Admin"]
    )
    def get_order_analytics():
        return {}

    @app.get(
        "/admin/analytics/revenue", response_model=dict[str, Any], tags=["Admin"]
    )
    def get_revenue_analytics():
        return {}

    @app.get("/admin/settings", response_model=dict[str, Any], tags=["Admin"])
    def get_admin_settings():
        return {}

    @app.put("/admin/settings", response_model=dict[str, Any], tags=["Admin"])
    def update_admin_settings(settings: dict[str, Any]):
        return {}

    @app.get("/admin/notifications", response_model=list[Notification], tags=["Admin"])
    def get_system_notifications():
        return []

    @app.post("/admin/notifications", response_model=Notification, tags=["Admin"])
    def create_system_notification(title: str, message: str):
        pass

    @app.get(
        "/admin/notifications/broadcast", tags=["Admin"]
    )
    def broadcast_notification(title: str, message: str):
        pass

    # Health/Misc routes (8 routes)
    @app.get("/health", response_model=HealthCheck, tags=["System"])
    def health_check():
        pass

    @app.get("/health/ready", tags=["System"])
    def readiness_check():
        return {"status": "ready"}

    @app.get("/health/live", tags=["System"])
    def liveness_check():
        return {"status": "live"}

    @app.get("/version", tags=["System"])
    def get_version():
        return {"version": "1.0.0"}

    @app.get("/config", response_model=dict[str, Any], tags=["System"])
    def get_public_config():
        return {}

    @app.get("/features", response_model=list[str], tags=["System"])
    def get_feature_flags():
        return []

    @app.get("/metrics", tags=["System"])
    def get_metrics():
        return {}

    @app.get("/error", response_model=ErrorResponse, tags=["System"])
    def get_error_codes():
        pass

    return app


# =============================================================================
# Benchmark Tests
# =============================================================================


@pytest.fixture(scope="module")
def large_app() -> FastAPI:
    """Create the large app fixture."""
    return create_large_app()


@pytest.fixture(scope="module")
def client(large_app: FastAPI) -> Iterator[TestClient]:
    """Create test client fixture."""
    with TestClient(large_app) as c:
        yield c


class TestOpenAPIGeneration:
    """Tests for OpenAPI schema generation performance."""

    def test_large_app_route_count(self, large_app: FastAPI) -> None:
        """Verify the large app has 100+ routes."""
        routes = [r for r in large_app.routes if hasattr(r, "methods")]
        assert len(routes) >= 100, f"Expected 100+ routes, got {len(routes)}"

    def test_openapi_generation_baseline(self, large_app: FastAPI) -> None:
        """Test baseline OpenAPI generation time without optimization."""
        # Clear any cached schema
        large_app.openapi_schema = None

        # Measure generation time
        start = time.perf_counter()
        schema = large_app.openapi()
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Verify schema is valid
        assert "openapi" in schema
        assert "paths" in schema
        assert len(schema["paths"]) >= 50  # Many unique paths

        # Log timing
        print(f"\nOpenAPI generation time: {elapsed_ms:.2f}ms")
        print(f"Number of paths: {len(schema['paths'])}")
        print(f"Number of schemas: {len(schema.get('components', {}).get('schemas', {}))}")

    def test_openapi_generation_with_profiling(self, large_app: FastAPI) -> None:
        """Test OpenAPI generation with detailed profiling."""
        # Clear any cached schema
        large_app.openapi_schema = None

        with ProfilingContext() as ctx:
            schema = large_app.openapi()

        # Print profiling report
        print("\n")
        ctx.print_report()

        # Verify schema
        assert "openapi" in schema
        assert "paths" in schema

        # Get stats for analysis
        stats = ctx.get_stats()
        assert "get_openapi" in stats
        assert stats["get_openapi"].call_count == 1

    def test_openapi_caching_works(self, large_app: FastAPI) -> None:
        """Verify that OpenAPI caching prevents regeneration."""
        # Clear any cached schema
        large_app.openapi_schema = None

        # First generation
        start1 = time.perf_counter()
        schema1 = large_app.openapi()
        time1 = (time.perf_counter() - start1) * 1000

        # Second call should be cached
        start2 = time.perf_counter()
        schema2 = large_app.openapi()
        time2 = (time.perf_counter() - start2) * 1000

        # Verify caching (second call should be nearly instant)
        assert schema1 is schema2  # Same object
        assert time2 < time1 / 10  # At least 10x faster

        print(f"\nFirst call: {time1:.2f}ms")
        print(f"Cached call: {time2:.4f}ms")
        print(f"Speedup: {time1/time2:.1f}x")

    def test_openapi_schema_correctness(self, large_app: FastAPI) -> None:
        """Verify the generated schema is correct."""
        # Clear any cached schema
        large_app.openapi_schema = None
        schema = large_app.openapi()

        # Check structure
        assert schema["openapi"].startswith("3.")
        assert schema["info"]["title"] == "Large Benchmark API"
        assert schema["info"]["version"] == "1.0.0"

        # Check paths exist
        assert "/users" in schema["paths"]
        assert "/products" in schema["paths"]
        assert "/orders" in schema["paths"]

        # Check components/schemas exist
        schemas = schema.get("components", {}).get("schemas", {})
        assert "User" in schemas or "UserBase" in schemas
        assert "Product" in schemas or "ProductBase" in schemas

    def test_openapi_endpoint_response(self, client: TestClient) -> None:
        """Test the /openapi.json endpoint returns valid schema."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema


class TestOpenAPIPerformanceThresholds:
    """Tests with performance thresholds."""

    def test_generation_under_threshold(self, large_app: FastAPI) -> None:
        """OpenAPI generation should complete under threshold."""
        # Clear any cached schema
        large_app.openapi_schema = None

        # Multiple runs to get average
        times = []
        for _ in range(3):
            large_app.openapi_schema = None
            start = time.perf_counter()
            large_app.openapi()
            times.append((time.perf_counter() - start) * 1000)

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"\nGeneration times: {[f'{t:.2f}ms' for t in times]}")
        print(f"Average: {avg_time:.2f}ms, Min: {min_time:.2f}ms, Max: {max_time:.2f}ms")

        # Threshold: should complete in under 5 seconds for 100+ routes
        # This is a baseline - optimizations should improve this
        assert avg_time < 5000, f"Generation took {avg_time:.2f}ms, expected < 5000ms"
