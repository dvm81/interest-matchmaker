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

    # Mock data for each file
    mock_data = {
        "valid_users": [
            {
                "name": "John Doe",
                "interests": [
                    {"type": "instrument", "value": "VOD.L", "threshold": 0.5},
                    {"type": "country", "value": "UK", "threshold": 0.24}
                ]
            }
        ],
        "invalid_users_duplicate_name": [
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
        ],
        "invalid_users_missing_fields": [
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
        ],
        "valid_content": [
            {
                "id": "123",
                "title": "Some title",
                "content": "Some content about UK",
                "tags": [
                    {"type": "country", "value": "UK", "threshold": 0.25}
                ]
            }
        ],
        "invalid_content_duplicate_id": [
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
        ],
        "invalid_content_missing_id": [
            {
                "title": "Some title",
                "content": "Some content about UK",
                "tags": [
                    {"type": "country", "value": "UK", "threshold": 0.25}
                ]
            }
        ],
        "invalid_content_missing_title": [
            {
                "id": "123",
                "content": "Some content about UK",
                "tags": [
                    {"type": "country", "value": "UK", "threshold": 0.25}
                ]
            }
        ],
        "invalid_content_missing_content": [
            {
                "id": "123",
                "title": "Some title",
                "tags": [
                    {"type": "country", "value": "UK", "threshold": 0.25}
                ]
            }
        ],
        "invalid_content_missing_value": [
            {
                "id": "123",
                "title": "Some title",
                "content": "Some content about UK",
                "tags": [
                    {"type": "country", "threshold": 0.25}  # Missing 'value'
                ]
            }
        ]
    }

    # Create the JSON test files
    for filename, data in mock_data.items():
        with open(test_files[filename], "w") as f:
            json.dump(data, f)

    yield test_files

    # Teardown: remove test files
    for file in test_files.values():
        if os.path.exists(file):
            os.remove(file)

def test_load_valid_users(test_data):
    """Test loading valid users data.

    This test ensures that the `load_users` function correctly loads valid user data
    from a JSON file.

    Args:
        test_data (dict): Paths to the test JSON files.
    """
    users = load_users(test_data["valid_users"])
    assert isinstance(users, list), "Users data should be a list."
    assert len(users) == 1, "There should be one user loaded."
    user = users[0]
    assert user["name"] == "John Doe", "The user's name should be 'John Doe'."
    assert "interests" in user, "User should have 'interests' key."
    assert isinstance(user["interests"], list), "'interests' should be a list."
    assert len(user["interests"]) == 2, "User should have two interests."
    assert "type" in user["interests"][0], "Each interest should have a 'type'."
    assert "value" in user["interests"][0], "Each interest should have a 'value'."
    assert "threshold" in user["interests"][0], "Each interest should have a 'threshold'."

def test_load_invalid_users_duplicate_name(test_data):
    """Test loading invalid users data with duplicate names.

    This test ensures that the `load_users` function raises a `ValueError` when encountering
    duplicate user names.

    Args:
        test_data (dict): Paths to the test JSON files.
    """
    with pytest.raises(ValueError, match="Duplicate user name found"):
        load_users(test_data["invalid_users_duplicate_name"])

def test_load_invalid_users_missing_fields(test_data):
    """Test loading invalid users data with missing fields.

    This test ensures that the `load_users` function raises a `ValueError` when user data
    is missing required fields.

    Args:
        test_data (dict): Paths to the test JSON files.
    """
    with pytest.raises(ValueError, match="Interest missing 'threshold' or 'threshold' is not a number for user 'John Doe'"):
        load_users(test_data["invalid_users_missing_fields"])

def test_load_valid_content(test_data):
    """Test loading valid content data.

    This test ensures that the `load_content` function correctly loads valid content data
    from a JSON file.

    Args:
        test_data (dict): Paths to the test JSON files.
    """
    content = load_content(test_data["valid_content"])
    assert isinstance(content, list), "Content data should be a list."
    assert len(content) == 1, "There should be one content item loaded."
    item = content[0]
    assert item["id"] == "123", "The content ID should be '123'."
    assert "title" in item, "Content should have a 'title'."
    assert "content" in item, "Content should have 'content' field."
    assert "tags" in item, "Content should have 'tags'."
    assert isinstance(item["tags"], list), "'tags' should be a list."
    assert len(item["tags"]) == 1, "Content should have one tag."
    assert "type" in item["tags"][0], "Each tag should have a 'type'."
    assert "value" in item["tags"][0], "Each tag should have a 'value'."
    assert "threshold" in item["tags"][0], "Each tag should have a 'threshold'."

@pytest.mark.parametrize("invalid_content_key,error_message", [
    ("invalid_content_duplicate_id", "Duplicate content ID found"),
    ("invalid_content_missing_id", "Content item missing 'id' or 'id' is empty"),
    ("invalid_content_missing_title", "Content item missing 'title' or 'title' is empty"),
    ("invalid_content_missing_content", "Content item missing 'content' or 'content' is empty"),
    ("invalid_content_missing_value", "Tag missing 'value' or 'value' is empty for content '123'")
])
def test_load_invalid_content(test_data, invalid_content_key, error_message):
    """Parametrized test for loading invalid content data with various issues.

    This test uses parametrization to run multiple checks for different invalid content
    scenarios. It ensures that the `load_content` function raises the appropriate `ValueError`
    for each type of invalid content.

    Args:
        test_data (dict): Paths to the test JSON files.
        invalid_content_key (str): The key to the specific invalid content JSON file.
        error_message (str): The expected error message for the invalid content scenario.
    """
    with pytest.raises(ValueError, match=error_message):
        load_content(test_data[invalid_content_key])
