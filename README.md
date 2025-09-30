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

- **PostgreSQL Implementation**: `SQLBedRepository` (currently used)
- **Alternative**: Easy to add MongoDB, SQLite, or other database implementations

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL database (accessible via DATABASE_URL)

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

Create a `local.env` file with your PostgreSQL connection string:

```
DATABASE_URL="postgresql://username:password@localhost:5432/grow_db"
```

### Database Setup

After setting up your environment variables, run the database migrations:

```bash
# Initialize the database with the schema
alembic upgrade head
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

### Tables

#### beds

```sql
CREATE TABLE beds (
    id SERIAL PRIMARY KEY,
    length INTEGER NOT NULL,
    width INTEGER NOT NULL,
    index INTEGER NOT NULL UNIQUE
);
```

#### plant_families

```sql
CREATE TABLE plant_families (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    nutrition_requirements TEXT NOT NULL,
    rotation_time INTEGER NOT NULL
);
```

#### bed_plant_family (junction table)

```sql
CREATE TABLE bed_plant_family (
    bed_id INTEGER REFERENCES beds(id),
    plant_family_id INTEGER REFERENCES plant_families(id),
    PRIMARY KEY (bed_id, plant_family_id)
);
```

**Field Descriptions:**

- `beds.id`: Auto-incrementing primary key
- `beds.index`: User-readable bed number (1-based, sequential, unique)
- `beds.length`: Length of the bed in centimeters
- `beds.width`: Width of the bed in centimeters
- `plant_families.name`: Name of the plant family (unique)
- `plant_families.nutrition_requirements`: Text description of nutritional needs
- `plant_families.rotation_time`: Time in months before rotating crops

## Adding a New Database

The application currently uses PostgreSQL. To add support for a different database:

1. Create a new repository class implementing `BedRepository`
2. Update `dependencies.py` to use the new repository
3. The service layer remains unchanged

Example for adding SQLite support:

```python
class SQLiteBedRepository(BedRepository):
    # Implement all abstract methods
    pass
```
