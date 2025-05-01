# Tree API

A FastAPI application for managing hierarchical tree data structures using MongoDB.

## Features

- RESTful API for creating and retrieving tree nodes
- Hierarchical data representation with parent-child relationships
- MongoDB integration using Motor for async operations
- Comprehensive test suite with pytest
- Docker and Docker Compose setup for easy deployment

## Tech Stack

- FastAPI: Modern, fast web framework for building APIs
- MongoDB: NoSQL database for storing tree data
- Motor: Async MongoDB driver for Python
- Pytest: Testing framework
- Docker: Containerization

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Running the Application

1. Clone the repository:
   ```
   git clone <your-repository-url>
   cd tree-api
   ```

2. Start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

3. The API will be available at http://localhost:8000

### API Endpoints

- `GET /api/tree`: Get all trees with their nested children
- `POST /api/tree`: Create a new node with optional parent

### Running Tests

```
docker-compose run test
```

## Project Structure

```
.
├── app/                # Application code
│   ├── db.py           # Database connection and operations
│   ├── main.py         # FastAPI application entry point
│   ├── models.py       # Pydantic models for request/response
│   ├── routes.py       # API routes
│   └── tree_service.py # Business logic for tree operations
├── tests/              # Test suite
│   ├── integration/    # Integration tests
│   └── unit/           # Unit tests
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── .env                # Environment variables
```

## License

[Your chosen license]