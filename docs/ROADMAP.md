# Roadmap

Future enhancements and improvements for the FastAPI framework.

## Completed

All P0–P3 user stories from the original PRD are implemented. See [PRD.md](PRD.md) for details.

Key milestones achieved:
- Core routing with type hints and automatic validation
- Async support with first-class performance
- OAuth2, JWT, and security utilities
- FastAPI CLI and developer tooling
- Extensibility via custom components
- Comprehensive testing utilities
- Production deployment options

## Ideas (Unprioritized)

These are potential directions. None have user stories or acceptance criteria yet — they need to be scoped before work begins.

- **Improved Error Messages**: More helpful validation errors with suggestions
- **Typed Middleware**: Type-safe middleware definitions
- **Enhanced OpenAPI**: More detailed schema generation options
- **Plugin System**: Formal extension mechanism for third-party integrations
- **Native gRPC Support**: gRPC reflection and transcoding
- **GraphQL Integration**: More mature GraphQL schema generation
- **Better Type Inference**: Improved type hints for complex scenarios
- **Streaming Responses**: Native support for Server-Sent Events
- **HTTP/2 Support**: Push promises and header compression
- **Zero-Config Deployments**: Simplified production setup

## Won't Have

- **Built-in Database ORM**: Users should choose their own (SQLAlchemy, Prisma, etc.)
- **Built-in Authentication Provider**: Identity management is outside framework scope
- **Template Engine**: Use external libraries (Jinja2, etc.) directly
- **Full-Stack Framework**: FastAPI remains focused on APIs only

## Lessons Learned

From years of maintaining FastAPI as a community-driven framework:

1. **Good**: Type hints provide excellent developer experience and IDE support
2. **Good**: OpenAPI integration enables rich ecosystem (clients, docs, testing)
3. **Good**: Dependency injection promotes loose coupling and testability
4. **Issue**: Balancing new features with stability is challenging
5. **Fix**: Semantic versioning with clear deprecation paths
6. **Fix**: Comprehensive documentation with examples
