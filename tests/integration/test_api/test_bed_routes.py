"""Integration tests for bed routes"""
import pytest
from fastapi.testclient import TestClient


class TestBedRoutes:
    """Integration tests for all bed-related API endpoints"""

    def test_create_beds(self, client: TestClient):
        """Test POST /garden/beds - Create multiple beds"""
        response = client.post(
            "/garden/beds",
            json={"numberOfBeds": 3, "length": 200, "width": 100}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "beds" in data
        assert "message" in data
        assert len(data["beds"]) == 3
        assert data["message"] == "Successfully created 3 beds"
        
        # Verify bed properties
        for i, bed in enumerate(data["beds"], start=1):
            assert bed["length"] == 200
            assert bed["width"] == 100
            assert bed["index"] == i
            assert "id" in bed
            assert bed["plant_families"] == []

    def test_create_beds_with_cleanup(self, client: TestClient):
        """Test POST /garden/beds/with-cleanup - Delete all and create new beds"""
        # First create some beds
        client.post(
            "/garden/beds",
            json={"numberOfBeds": 2, "length": 150, "width": 100}
        )
        
        # Now create with cleanup
        response = client.post(
            "/garden/beds/with-cleanup",
            json={"numberOfBeds": 3, "length": 300, "width": 200}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["beds"]) == 3
        assert data["message"] == "Successfully created 3 beds"
        
        # Verify old beds are gone and new beds start from index 1
        for i, bed in enumerate(data["beds"], start=1):
            assert bed["length"] == 300
            assert bed["width"] == 200
            assert bed["index"] == i
        
        # Verify only 3 beds exist in total
        all_beds_response = client.get("/garden/beds")
        assert len(all_beds_response.json()) == 3

    def test_get_all_beds(self, client: TestClient):
        """Test GET /garden/beds - Get all beds"""
        # Create some beds first
        client.post(
            "/garden/beds",
            json={"numberOfBeds": 2, "length": 250, "width": 150}
        )
        
        response = client.get("/garden/beds")
        
        assert response.status_code == 200
        beds = response.json()
        
        assert len(beds) == 2
        assert beds[0]["index"] == 1
        assert beds[1]["index"] == 2

    def test_get_all_beds_empty(self, client: TestClient):
        """Test GET /garden/beds - Get all beds when database is empty"""
        response = client.get("/garden/beds")
        
        assert response.status_code == 200
        beds = response.json()
        assert beds == []

    def test_get_bed_by_id(self, client: TestClient):
        """Test GET /garden/beds/{bed_id} - Get a specific bed by ID"""
        # Create a bed
        create_response = client.post(
            "/garden/beds",
            json={"numberOfBeds": 1, "length": 300, "width": 200}
        )
        bed_id = create_response.json()["beds"][0]["id"]
        
        # Get the bed by ID
        response = client.get(f"/garden/beds/{bed_id}")
        
        assert response.status_code == 200
        bed = response.json()
        
        assert bed["id"] == bed_id
        assert bed["length"] == 300
        assert bed["width"] == 200
        assert bed["index"] == 1
        assert bed["plant_families"] == []

    def test_get_bed_by_id_not_found(self, client: TestClient):
        """Test GET /garden/beds/{bed_id} - Bed not found returns 404"""
        response = client.get("/garden/beds/99999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_bed(self, client: TestClient):
        """Test PUT /garden/beds/{bed_id} - Update a bed"""
        # Create a bed
        create_response = client.post(
            "/garden/beds",
            json={"numberOfBeds": 1, "length": 200, "width": 100}
        )
        bed_id = create_response.json()["beds"][0]["id"]
        
        # Update the bed
        response = client.put(
            f"/garden/beds/{bed_id}",
            json={"length": 400, "width": 300}
        )
        
        assert response.status_code == 200
        updated_bed = response.json()
        
        assert updated_bed["id"] == bed_id
        assert updated_bed["length"] == 400
        assert updated_bed["width"] == 300
        assert updated_bed["index"] == 1  # Index shouldn't change
        assert updated_bed["plant_families"] == []

    def test_update_bed_not_found(self, client: TestClient):
        """Test PUT /garden/beds/{bed_id} - Update non-existent bed returns 404"""
        response = client.put(
            "/garden/beds/99999",
            json={"length": 400, "width": 300}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_delete_bed(self, client: TestClient):
        """Test DELETE /garden/beds/{bed_id} - Delete a specific bed"""
        # Create beds
        create_response = client.post(
            "/garden/beds",
            json={"numberOfBeds": 2, "length": 200, "width": 100}
        )
        bed_id = create_response.json()["beds"][0]["id"]
        
        # Delete the bed
        response = client.delete(f"/garden/beds/{bed_id}")
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify bed is gone
        get_response = client.get(f"/garden/beds/{bed_id}")
        assert get_response.status_code == 404
        
        # Verify other bed still exists
        all_beds = client.get("/garden/beds").json()
        assert len(all_beds) == 1

    def test_delete_bed_not_found(self, client: TestClient):
        """Test DELETE /garden/beds/{bed_id} - Delete non-existent bed returns 404"""
        response = client.delete("/garden/beds/99999")
        
        assert response.status_code == 404

    def test_delete_all_beds(self, client: TestClient):
        """Test DELETE /garden/beds/all - Delete all beds"""
        # Create some beds
        client.post(
            "/garden/beds",
            json={"numberOfBeds": 5, "length": 200, "width": 100}
        )
        
        # Delete all beds
        response = client.delete("/garden/beds/all")
        
        assert response.status_code == 200
        assert "5 beds" in response.json()["message"]
        
        # Verify all beds are gone
        all_beds = client.get("/garden/beds").json()
        assert len(all_beds) == 0

    def test_delete_all_beds_when_empty(self, client: TestClient):
        """Test DELETE /garden/beds/all - Delete all when database is empty"""
        response = client.delete("/garden/beds/all")
        
        assert response.status_code == 200
        assert "0 beds" in response.json()["message"]

    def test_create_beds_validation_error(self, client: TestClient):
        """Test POST /garden/beds - Validation error for invalid input"""
        # Test with negative dimensions
        response = client.post(
            "/garden/beds",
            json={"numberOfBeds": 1, "length": -100, "width": 50}
        )
        
        assert response.status_code == 422  # Validation error
        
        # Test with zero beds
        response = client.post(
            "/garden/beds",
            json={"numberOfBeds": 0, "length": 100, "width": 50}
        )
        
        assert response.status_code == 422

    def test_update_bed_validation_error(self, client: TestClient):
        """Test PUT /garden/beds/{bed_id} - Validation error for invalid dimensions"""
        # Create a bed
        create_response = client.post(
            "/garden/beds",
            json={"numberOfBeds": 1, "length": 200, "width": 100}
        )
        bed_id = create_response.json()["beds"][0]["id"]
        
        # Try to update with invalid dimensions
        response = client.put(
            f"/garden/beds/{bed_id}",
            json={"length": 0, "width": -50}
        )
        
        assert response.status_code == 422

    def test_bed_ordering(self, client: TestClient):
        """Test that beds are returned in correct order by index"""
        # Create multiple beds
        client.post(
            "/garden/beds",
            json={"numberOfBeds": 5, "length": 200, "width": 100}
        )
        
        # Get all beds
        response = client.get("/garden/beds")
        beds = response.json()
        
        # Verify ordering
        assert len(beds) == 5
        for i, bed in enumerate(beds, start=1):
            assert bed["index"] == i
