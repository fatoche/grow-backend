# GROW Backend

Backend API for the GROW garden planning application.

## Architecture

The backend follows a clean architecture pattern with the following layers:

1. **API Layer** (`app/api/`): FastAPI routes and HTTP handling
2. **Service Layer** (`app/services/`): Business logic
3. **Repository Layer** (`app/database/`): Database-agnostic interface
4. **Model Layer** (`app/models/`): Pydantic models for validation

### Database Abstraction

The application uses a database-agnostic interface (`BedRepository`) that allows easy switching between different databases:

- **MongoDB Implementation**: `MongoBedRepository` (currently used)
- **Future**: Easy to add PostgreSQL, SQLite, or other database implementations

## Setup

### Prerequisites

- Python 3.10+
- MongoDB cluster (accessible via MONGO_URI)

### Installation

1. **Using Conda (recommended):**

   ```bash
   conda env create -f environment.yaml
   conda activate grow-backend
   ```

2. **Using pip:**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `local.env` file with your MongoDB URI:

```
MONGO_URI="your_mongodb_connection_string"
```

## Running the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:

- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## API Endpoints

### Bed Management

- `POST /garden/beds` - Create multiple beds
- `POST /garden/beds/with-cleanup` - Delete all existing beds and create new ones
- `DELETE /garden/beds/all` - Delete all beds
- `GET /garden/beds` - Get all beds
- `GET /garden/beds/{bed_id}` - Get a specific bed
- `PUT /garden/beds/{bed_id}` - Update a bed
- `DELETE /garden/beds/{bed_id}` - Delete a bed

### Health Check

- `GET /` - Root endpoint
- `GET /health` - Health check

## Database Schema

### Beds Collection

```json
{
  "_id": "bed_12345678",
  "index": 1,
  "length": 200,
  "width": 120,
  "plant_families": []
}
```

**Field Descriptions:**

- `_id`: Unique identifier for the bed
- `index`: User-readable bed number (1-based, sequential)
- `length`: Length of the bed in centimeters
- `width`: Width of the bed in centimeters
- `plant_families`: Array of plant families (currently empty)

## Adding a New Database

To add support for a new database:

1. Create a new repository class implementing `BedRepository`
2. Update `dependencies.py` to use the new repository
3. The service layer remains unchanged

Example:

```python
class PostgresBedRepository(BedRepository):
    # Implement all abstract methods
    pass
```
