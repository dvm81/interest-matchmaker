import pytest
import os
import json
from app import app, load_users, load_content, match_content_to_users

# Add the project root directory to the Python path to ensure imports work correctly.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="module")
def test_client():
    """Fixture to set up the Flask test client.

    This fixture initializes the Flask application in testing mode and provides a test client
    that can be used to make requests to the app's routes.

    Yields:
        FlaskClient: A Flask test client for sending requests to the app.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module")
def test_data():
    """Fixture to set up and tear down test data files.

    This fixture creates temporary JSON files containing user and content data for testing purposes.
    After the tests are run, the files are deleted.

    Yields:
        tuple: A tuple containing the file paths for the users and content test JSON files.
    """
    users_file = "test_users.json"
    content_file = "test_content.json"

    # Test data for users
    valid_users = [
        {
            "name": "John Doe",
            "interests": [
                {"type": "instrument", "value": "VOD.L", "threshold": 0.5},
                {"type": "country", "value": "UK", "threshold": 0.24}
            ]
        },
        {
            "name": "Alice Johnson",
            "interests": [
                {"type": "topic", "value": "art", "threshold": 0.5}
            ]
        },
        {
            "name": "Bob Smith",
            "interests": [
                {"type": "topic", "value": "sports", "threshold": 0.6}
            ]
        }
    ]

    # Test data for content
    valid_content = [
        {
            "id": "123",
            "title": "Some title",
            "content": "Some content about UK",
            "tags": [
                {"type": "country", "value": "UK", "threshold": 0.25}
            ]
        },
        {
            "id": "124",
            "title": "Art Exhibition",
            "content": "Modern art trends",
            "tags": [
                {"type": "topic", "value": "art", "threshold": 0.4}
            ]
        },
        {
            "id": "125",
            "title": "Football World Cup",
            "content": "World Cup sports events",
            "tags": [
                {"type": "topic", "value": "sports", "threshold": 0.6}
            ]
        },
        {
            "id": "126",
            "title": "Sports Update",
            "content": "Latest sports news",
            "tags": [
                {"type": "topic", "value": "sports", "threshold": 0.6}
            ]
        }
    ]

    # Write test data to JSON files
    with open(users_file, "w") as f:
        json.dump(valid_users, f)

    with open(content_file, "w") as f:
        json.dump(valid_content, f)

    # Set the app config to use the test files
    app.config['USERS_FILE'] = users_file
    app.config['CONTENT_FILE'] = content_file

    # Provide the test data file paths to the tests
    yield users_file, content_file

    # Teardown: Remove the test files after tests are complete
    os.remove(users_file)
    os.remove(content_file)

def test_user_content_route_single_match(test_client, test_data):
    """Test the user content route with a user who has a single match.

    This test ensures that when a user has a single matching content item, the API returns it correctly.

    Args:
        test_client (FlaskClient): The Flask test client provided by the fixture.
        test_data (tuple): The test data file paths provided by the fixture.
    """
    response = test_client.get('/user_content', query_string={'user': 'John Doe'})
    assert response.status_code == 200, "User content route should return a 200 status code."
    data = json.loads(response.data)

    # Debugging information
    print("Data returned for John Doe:", data)

    # Assertions to verify correct behavior
    assert isinstance(data, list), "Response should be a list."
    assert len(data) == 1, "John Doe should have one matching content."
    assert data[0]['id'] == "123", "The matching content ID should be '123'."

def test_user_content_route_multiple_matches(test_client, test_data):
    """Test the user content route with a user who has multiple matches.

    This test checks that the API correctly returns multiple matching content items for a user.

    Args:
        test_client (FlaskClient): The Flask test client provided by the fixture.
        test_data (tuple): The test data file paths provided by the fixture.
    """
    response = test_client.get('/user_content', query_string={'user': 'Bob Smith'})
    assert response.status_code == 200, "User content route should return a 200 status code."
    data = json.loads(response.data)

    # Debugging information
    print("Data returned for Bob Smith:", data)

    # Assertions to verify correct behavior
    assert isinstance(data, list), "Response should be a list."
    assert len(data) == 2, "Bob Smith should have two matching content items."
    matched_ids = {content['id'] for content in data}
    assert matched_ids == {"125", "126"}, "Bob Smith's matching content IDs should be '125' and '126'."

def test_user_content_route_no_matches(test_client, test_data):
    """Test the user content route with a user who has no matches.

    This test ensures that when a user has no matching content, the API returns an empty list.

    Args:
        test_client (FlaskClient): The Flask test client provided by the fixture.
        test_data (tuple): The test data file paths provided by the fixture.
    """
    response = test_client.get('/user_content', query_string={'user': 'Alice Johnson'})
    assert response.status_code == 200, "User content route should return a 200 status code."
    data = json.loads(response.data)

    # Debugging information
    print("Data returned for Alice Johnson:", data)

    # Assertions to verify correct behavior
    assert isinstance(data, list), "Response should be a list."
    assert len(data) == 0, "Alice Johnson should have no matching content."

def test_match_content_to_users(test_data):
    """Test the content matching logic to ensure users get correct content.

    This test verifies that the `match_content_to_users` function correctly matches content to users
    based on their interests.

    Args:
        test_data (tuple): The test data file paths provided by the fixture.
    """
    users_file, content_file = test_data
    users = load_users()
    content = load_content()
    matches = match_content_to_users(users, content)

    # Debugging information
    print("Matches for users:", matches)

    # Test for John Doe (single match)
    assert "John Doe" in matches, "John Doe should be in the matches."
    assert len(matches["John Doe"]) == 1, "John Doe should have 1 match."
    assert matches["John Doe"][0]['id'] == "123", "John Doe's matching content ID should be '123'."

    # Test for Alice Johnson (no matches)
    assert "Alice Johnson" in matches, "Alice Johnson should be in the matches."
    assert len(matches["Alice Johnson"]) == 0, "Alice Johnson should have no matches."

    # Test for Bob Smith (multiple matches)
    assert "Bob Smith" in matches, "Bob Smith should be in the matches."
    assert len(matches["Bob Smith"]) == 2, "Bob Smith should have 2 matches."
    bob_smith_ids = {content['id'] for content in matches["Bob Smith"]}
    assert bob_smith_ids == {"125", "126"}, "Bob Smith's matching content IDs should be '125' and '126'."

def test_error_handling_missing_user(test_client, test_data):
    """Test the error handling for a user that does not exist.

    This test ensures that the API returns an empty list when a non-existent user is requested.

    Args:
        test_client (FlaskClient): The Flask test client provided by the fixture.
        test_data (tuple): The test data file paths provided by the fixture.
    """
    response = test_client.get('/user_content', query_string={'user': 'Nonexistent User'})
    assert response.status_code == 200, "User content route should return a 200 status code."
    data = json.loads(response.data)

    # Debugging information
    print("Data returned for Nonexistent User:", data)

    # Assertions to verify correct behavior
    assert isinstance(data, list), "Response should be a list."
    assert len(data) == 0, "Nonexistent User should have no matching content."

def test_error_handling_invalid_route(test_client):
    """Test error handling for accessing an invalid route.

    This test ensures that the application correctly returns a 404 status code when an invalid
    route is accessed.

    Args:
        test_client (FlaskClient): The Flask test client provided by the fixture.
    """
    response = test_client.get('/invalid_route')
    assert response.status_code == 404, "Invalid route should return a 404 status code."
