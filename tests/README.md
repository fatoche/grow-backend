# Tests

This directory contains all tests for the GROW backend application.

## Structure

```
tests/
├── unit/           # Unit tests (mirror app/ structure)
├── integration/    # Integration tests (mirror app/ structure)
│   └── test_api/
│       └── test_bed_routes.py
└── conftest.py     # Shared fixtures
```

## Running Tests

### Install Test Dependencies

```bash
mamba env update --file environment.yaml
```

### Run All Tests

```bash
pytest
```

### Run Only Integration Tests

```bash
pytest tests/integration/
```

### Run Only Unit Tests

```bash
pytest tests/unit/
```

### Run Specific Test File

```bash
pytest tests/integration/test_api/test_bed_routes.py
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

## Test Database Setup

Integration tests require a test database. By default, tests use:

- Database: `grow_test_db`
- User: `grow_user`
- Password: `grow_password`
- Port: `5434`

You can override this by setting the `TEST_DATABASE_URL` environment variable:

```bash
export TEST_DATABASE_URL="postgresql://user:password@localhost:5434/test_db"
pytest
```

## Writing Tests

### Integration Tests

Integration tests should:

- Use the `client` fixture for HTTP requests
- Use the `clean_database` fixture to ensure a clean state
- Use the `override_database_url` fixture to use the test database
- Test the full request/response cycle
- Be placed in `tests/integration/` mirroring the `app/` structure

Example:

```python
def test_create_beds(client, clean_database, override_database_url):
    response = client.post("/garden/beds", json={...})
    assert response.status_code == 200
```

### Unit Tests

Unit tests should:

- Test individual functions/methods in isolation
- Mock external dependencies
- Be placed in `tests/unit/` mirroring the `app/` structure
