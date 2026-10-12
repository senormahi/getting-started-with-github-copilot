import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(app_module, "activities", copy.deepcopy(INITIAL_ACTIVITIES))

    with TestClient(app_module.app) as test_client:
        yield test_client


def test_get_activities_returns_activity_data(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert activity_name in response.json()
    assert response.json()[activity_name]["participants"] == INITIAL_ACTIVITIES[activity_name]["participants"]


def test_signup_adds_participant_and_returns_updated_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new-student@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_rejects_duplicate_participant_without_mutation(client):
    # Arrange
    activity_name = "Chess Club"
    email = INITIAL_ACTIVITIES[activity_name]["participants"][0]
    participants_before = copy.deepcopy(app_module.activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"
    assert app_module.activities[activity_name]["participants"] == participants_before


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "new-student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = INITIAL_ACTIVITIES[activity_name]["participants"][0]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_returns_not_found_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_get_orders_returns_only_orders_for_customer(client):
    # Arrange
    customer_id = "customer-1001"

    # Act
    response = client.get("/orders", params={"customerId": customer_id})

    # Assert
    assert response.status_code == 200
    assert [order["orderId"] for order in response.json()] == ["order-1001", "order-1002"]
    assert all(order["customerId"] == customer_id for order in response.json())


def test_get_orders_returns_empty_list_when_customer_has_no_orders(client):
    # Arrange
    customer_id = "customer-with-no-orders"

    # Act
    response = client.get("/orders", params={"customerId": customer_id})

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_get_orders_requires_customer_id(client):
    # Arrange
    request_params = {}

    # Act
    response = client.get("/orders", params=request_params)

    # Assert
    assert response.status_code == 422