import pytest
import os
import json
from app import load_users, load_content

@pytest.fixture(scope='module')
def test_data():
    """Fixture to set up and tear down test data files.

    This fixture creates mock JSON files for valid and invalid user and content data.
    After the tests run, it cleans up by deleting these files.

    Yields:
        dict: Paths to the user and content JSON files.
    """
    test_files = {
        "valid_users": "test_valid_users.json",
        "invalid_users_duplicate_name": "test_invalid_users_duplicate_name.json",
        "invalid_users_missing_fields": "test_invalid_users_missing_fields.json",
        "valid_content": "test_valid_content.json",
        "invalid_content_duplicate_id": "test_invalid_content_duplicate_id.json",
        "invalid_content_missing_id": "test_invalid_content_missing_id.json",
        "invalid_content_missing_title": "test_invalid_content_missing_title.json",
        "invalid_content_missing_content": "test_invalid_content_missing_content.json",
        "invalid_content_missing_value": "test_invalid_content_missing_value.json"
    }

    # Valid users JSON
    valid_users = [
        {
            "name": "John Doe",
            "interests": [
                {"type": "instrument", "value": "VOD.L", "threshold": 0.5},
                {"type": "country", "value": "UK", "threshold": 0.24}
            ]
        }
    ]
    with open(test_files["valid_users"], "w") as f:
        json.dump(valid_users, f)

    # Invalid users JSON (duplicate name)
    invalid_users_duplicate_name = [
        {
            "name": "John Doe",
            "interests": [
                {"type": "instrument", "value": "VOD.L", "threshold": 0.5}
            ]
        },
        {
            "name": "John Doe",  # Duplicate name
            "interests": [
                {"type": "country", "value": "UK", "threshold": 0.24}
            ]
        }
    ]
    with open(test_files["invalid_users_duplicate_name"], "w") as f:
        json.dump(invalid_users_duplicate_name, f)

    # Invalid users JSON (missing required fields)
    invalid_users_missing_fields = [
        {
            "name": "John Doe",
            "interests": [
                {"type": "instrument", "value": "VOD.L"}  # Missing 'threshold'
            ]
        },
        {
            "interests": [  # Missing 'name'
                {"type": "country", "value": "UK", "threshold": 0.24}
            ]
        }
    ]
    with open(test_files["invalid_users_missing_fields"], "w") as f:
        json.dump(invalid_users_missing_fields, f)

    # Valid content JSON
    valid_content = [
        {
            "id": "123",
            "title": "Some title",
            "content": "Some content about UK",
            "tags": [
                {"type": "country", "value": "UK", "threshold": 0.25}
            ]
        }
    ]
    with open(test_files["valid_content"], "w") as f:
        json.dump(valid_content, f)

    # Invalid content JSON (duplicate ID)
    invalid_content_duplicate_id = [
        {
            "id": "123",
            "title": "Some title",
            "content": "Some content about UK",
            "tags": [
                {"type": "country", "value": "UK", "threshold": 0.25}
            ]
        },
        {
            "id": "123",  # Duplicate ID
            "title": "Another title",
            "content": "Some content about US",
            "tags": [
                {"type": "country", "value": "US", "threshold": 0.3}
            ]
        }
    ]
    with open(test_files["invalid_content_duplicate_id"], "w") as f:
        json.dump(invalid_content_duplicate_id, f)

    # Invalid content JSON (missing 'id')
    invalid_content_missing_id = [
        {
            "title": "Some title",
            "content": "Some content about UK",
            "tags": [
                {"type": "country", "value": "UK", "threshold": 0.25}
            ]
        }
    ]
    with open(test_files["invalid_content_missing_id"], "w") as f:
        json.dump(invalid_content_missing_id, f)

    # Invalid content JSON (missing 'title')
    invalid_content_missing_title = [
        {
            "id": "123",
            "content": "Some content about UK",
            "tags": [
                {"type": "country", "value": "UK", "threshold": 0.25}
            ]
        }
    ]
    with open(test_files["invalid_content_missing_title"], "w") as f:
        json.dump(invalid_content_missing_title, f)

    # Invalid content JSON (missing 'content')
    invalid_content_missing_content = [
        {
            "id": "123",
            "title": "Some title",
            "tags": [
                {"type": "country", "value": "UK", "threshold": 0.25}
            ]
        }
    ]
    with open(test_files["invalid_content_missing_content"], "w") as f:
        json.dump(invalid_content_missing_content, f)

    # Invalid content JSON (missing 'value' in tags)
    invalid_content_missing_value = [
        {
            "id": "123",
            "title": "Some title",
            "content": "Some content about UK",
            "tags": [
                {"type": "country", "threshold": 0.25}  # Missing 'value'
            ]
        }
    ]
    with open(test_files["invalid_content_missing_value"], "w") as f:
        json.dump(invalid_content_missing_value, f)

    yield test_files

    # Teardown: remove test files
    for file in test_files.values():
        if os.path.exists(file):
            os.remove(file)

def test_load_valid_users(test_data):
    """Test loading valid users data.

    This test ensures that the `load_users` function correctly loads valid user data from a JSON file.

    Args:
        test_data (dict): Paths to the test JSON files.
    """
    users = load_users(test_data["valid_users"])
    assert isinstance(users, list), "Users data should be a list."
    assert len(users) == 1, "There should be one user loaded."
    assert users[0]["name"] == "John Doe", "The user's name should be 'John Doe'."

def test_load_invalid_users_duplicate_name(test_data):
    """Test loading invalid users data (duplicate name).

    This test ensures that the `load_users` function raises a `ValueError` when encountering duplicate user names.

    Args:
        test_data (dict): Paths to the test JSON files.
    """
    with pytest.raises(ValueError, match="Duplicate user name found"):
        load_users(test_data["invalid_users_duplicate_name"])

def test_load_invalid_users_missing_fields(test_data):
    """Test loading invalid users data (missing required fields).

    This test ensures that the `load_users` function raises a `ValueError` when user data is missing required fields.

    Args:
        test_data (dict): Paths to the test JSON files.
    """
    with pytest.raises(ValueError, match="Interest missing 'threshold' or 'threshold' is not a number for user 'John Doe'"):
        load_users(test_data["invalid_users_missing_fields"])

def test_load_valid_content(test_data):
    """Test loading valid content data.

    This test ensures that the `load_content` function correctly loads valid content data from a JSON file.

    Args:
        test_data (dict): Paths to the test JSON files.
    """
    content = load_content(test_data["valid_content"])
    assert isinstance(content, list), "Content data should be a list."
    assert len(content) == 1, "There should be one content item loaded."
    assert content[0]["id"] == "123", "The content ID should be '123'."

def test_load_invalid_content_duplicate_id(test_data):
    """Test loading invalid content data (duplicate ID).

    This test ensures that the `load_content` function raises a `ValueError` when encountering duplicate content IDs.

    Args:
        test_data (dict): Paths to the test JSON files.
    """
    with pytest.raises(ValueError, match="Duplicate content ID found"):
        load_content(test_data["invalid_content_duplicate_id"])

def test_load_invalid_content_missing_id(test_data):
    """Test loading content with missing 'id' field."""
    with pytest.raises(ValueError, match="Content item missing 'id' or 'id' is empty"):
        load_content(test_data["invalid_content_missing_id"])

def test_load_invalid_content_missing_title(test_data):
    """Test loading content with missing 'title' field."""
    with pytest.raises(ValueError, match="Content item missing 'title' or 'title' is empty"):
        load_content(test_data["invalid_content_missing_title"])

def test_load_invalid_content_missing_content(test_data):
    """Test loading content with missing 'content' field."""
    with pytest.raises(ValueError, match="Content item missing 'content' or 'content' is empty"):
        load_content(test_data["invalid_content_missing_content"])

def test_load_invalid_content_missing_value(test_data):
    """Test loading content with missing 'value' in 'tags'."""
    with pytest.raises(ValueError, match="Tag missing 'value' or 'value' is empty for content '123'"):
        load_content(test_data["invalid_content_missing_value"])
