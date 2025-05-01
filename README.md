# 🌳 Tree API

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![MongoDB](https://img.shields.io/badge/MongoDB-latest-success)
![License](https://img.shields.io/badge/license-MIT-orange)
![Deployment](https://img.shields.io/badge/deployed-render-blueviolet)

**A modern, high-performance API for managing hierarchical tree data structures**

[Live Demo](https://theary.onrender.com/docs) 

</div>

## 🚀 Features

- **RESTful Architecture**: Clean, intuitive endpoints for managing tree structures
- **Hierarchical Data**: Flexible parent-child relationships with unlimited nesting
- **Async Performance**: Built with async I/O for maximum throughput
- **API Key Security**: Protected endpoints with authentication
- **Comprehensive Testing**: Extensive test coverage with pytest
- **Docker Ready**: Containerized for consistent deployment across environments
- **Cloud Deployed**: Successfully deployed on Render with MongoDB Atlas

## 🛠️ Tech Stack

<div align="center">
<table>
  <tr>
    <td align="center" width="130">
      <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI logo" width="100"><br>
      <b>FastAPI</b>
    </td>
    <td align="center" width="130">
      <img src="https://webassets.mongodb.com/_com_assets/cms/mongodb_logo1-76twgcu2dm.png" alt="MongoDB logo" width="100"><br>
      <b>MongoDB</b>
    </td>
    <td align="center" width="130">
      <img src="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png" alt="Docker logo" width="100"><br>
      <b>Docker</b>
    </td>
  </tr>
</table>
</div>

## 🏁 Quick Start

### Prerequisites

- Docker
- Git
- The API's require a key for authentication, which is sent over secure email.

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/AdityaBandaru06/Theary.git
cd Theary

# Start the application using Docker Compose
docker compose up -d

# Build and start the service
docker compose up -d --build

# The API will be available at http://localhost:8000/docs
```

# 🌳 Tree Structure API

> *Elegant hierarchical data management through simple parent-child relationships*

## 📋 Node Types

| Type | Description |
|------|-------------|
| **Root Nodes** | Nodes with no parent. The system initializes with one default root node, but you can create additional root nodes as needed. |
| **Child Nodes** | Nodes connected to a parent node. These can be nested to create trees for different parent nodes. |

## 🧩 Data Structure

Each node contains:

```json
{
  "id": "Unique identifier (auto-generated)",
  "label": "Descriptive text name",
  "parentId": "ID of the parent node (null for root nodes)",
  "children": "Array of child nodes (populated when retrieving trees)"
}
```

## 🔨 Creating Nodes

### Create a Root Node:
```http
POST /api/tree
```
```json
{
  "label": "New Root Category"
}
```

### Create a Child Node:
```http
POST /api/tree
```
```json
{
  "label": "Child Item",
  "parentId": 1
}
```

## 🌿 Example Tree Structure

```
Root (id: 1)
├── Child A (id: 2)
│   ├── Grandchild A1 (id: 4)
│   └── Grandchild A2 (id: 5)
└── Child B (id: 3)
    └── Grandchild B1 (id: 6)
```

## ⚙️ Business Rules

### Node Creation:
- You can create nodes with or without a parent
- Providing an invalid parentId will result in a 404 error
- Root nodes are created by omitting the parentId field

### Tree Retrieval:
- The GET endpoint returns all trees with complete hierarchy
- Each node contains its full subtree of children
- Trees are efficiently constructed to avoid recursive database calls

---

This flexible structure allows for representing any hierarchical data, from simple lists to complex organizational charts, category trees, or file systems.

## 📘 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive Swagger documentation.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tree` | Retrieve all trees with nested children |
| POST | `/api/tree` | Create a new node with optional parent |
| GET | `/api/health` | Health check endpoint (no auth required) |

## 🧪 Testing

## Unit Tests
Individual components are tested in isolation to ensure each function and method works correctly.
## Integration Tests
End-to-end tests verify that components work together properly, testing the complete request/response cycle.

Run the comprehensive test suite:

```bash
# Run all tests
docker compose run test


## 🚀 Deployment

This application is currently deployed on Render with MongoDB Atlas integration.

### Live Demo

- **API Documentation**: [https://theary.onrender.com/docs](https://theary.onrender.com/docs)

### Deployment Platforms

- **Render** ✅: Currently deployed

### Render Configuration

The deployment was configured with the following setup:

1. Web Service type with automatic deployment from GitHub
2. Environment variables configured in the Render dashboard
3. Connected to a MongoDB Atlas cluster for persistent database storage

## 🔐 Environment Variables

Configure the application with these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | Authentication key (required) | None |
| `MONGODB_URL` | MongoDB connection string | mongodb://mongodb:27017 |
| `DATABASE_NAME` | Database name | tree_db |
| `TEST_DATABASE_NAME` | Test Database name | test_tree_db |



## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
