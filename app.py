import os
import json
from flask import Flask, render_template, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

#global dictionary to cache the matches
matches = {}

# Configurable paths for user and content data
app.config['USERS_FILE'] = 'data/users.json'
app.config['CONTENT_FILE'] = 'data/content.json'

def load_json_data(file_path):
    """Loads JSON data from a specified file with error handling.

    Args:
        file_path (str): The path to the JSON file to load.

    Returns:
        dict or list: The JSON data parsed into a dictionary or list.

    Raises:
        FileNotFoundError: If the file does not exist.
        JSONDecodeError: If there is an error decoding the JSON.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON from file {file_path}: {e.msg}", e.doc, e.pos)

def load_users(file_path=None):
    """Loads user data from a JSON file.

    Args:
        file_path (str, optional): The path to the JSON file containing user data. Defaults to None.

    Returns:
        list: A list of user dictionaries.

    Raises:
        ValueError: If required fields are missing or if there are duplicate user names.
    """
    if file_path is None:
        file_path = app.config['USERS_FILE']
    
    users = load_json_data(file_path)

    seen_names = set()
    for user in users:
        if 'name' not in user or not user['name']:
            raise ValueError(f"User missing 'name' or 'name' is empty: {user}")
        if user['name'] in seen_names:
            raise ValueError(f"Duplicate user name found: {user['name']}")
        seen_names.add(user['name'])

        if 'interests' not in user or not isinstance(user['interests'], list):
            raise ValueError(f"User '{user['name']}' has invalid or missing 'interests'.")
        
        for interest in user['interests']:
            if 'type' not in interest or not interest['type']:
                raise ValueError(f"Interest missing 'type' or 'type' is empty for user '{user['name']}'.")
            if 'value' not in interest or not interest['value']:
                raise ValueError(f"Interest missing 'value' or 'value' is empty for user '{user['name']}'.")
            if 'threshold' not in interest or not isinstance(interest['threshold'], (int, float)):
                raise ValueError(f"Interest missing 'threshold' or 'threshold' is not a number for user '{user['name']}'.")

    return users

def load_content(file_path=None):
    """Loads content data from a JSON file.

    Args:
        file_path (str, optional): The path to the JSON file containing content data. Defaults to None.

    Returns:
        list: A list of content dictionaries.

    Raises:
        ValueError: If required fields are missing, if content IDs are duplicated, or if tags are invalid.
    """
    if file_path is None:
        file_path = app.config['CONTENT_FILE']
    
    content = load_json_data(file_path)

    seen_ids = set()
    for item in content:
        # Check for 'id'
        if 'id' not in item or not item['id']:
            raise ValueError(f"Content item missing 'id' or 'id' is empty: {item}")

        # Check for 'title'
        if 'title' not in item or not item['title']:
            raise ValueError(f"Content item missing 'title' or 'title' is empty for content '{item.get('id', 'Unknown')}'")

        # Check for 'content'
        if 'content' not in item or not item['content']:
            raise ValueError(f"Content item missing 'content' or 'content' is empty for content '{item.get('id', 'Unknown')}'")

        # Ensure 'id' is unique
        if item['id'] in seen_ids:
            raise ValueError(f"Duplicate content ID found: {item['id']}")
        seen_ids.add(item['id'])

        # Check for 'tags'
        if 'tags' not in item or not isinstance(item['tags'], list):
            raise ValueError(f"Content item '{item['id']}' has invalid or missing 'tags'.")

        # Validate each tag
        for tag in item['tags']:
            if 'type' not in tag or not tag['type']:
                raise ValueError(f"Tag missing 'type' or 'type' is empty for content '{item['id']}'.")
            if 'value' not in tag or not tag['value']:
                raise ValueError(f"Tag missing 'value' or 'value' is empty for content '{item['id']}'.")
            if 'threshold' not in tag or not isinstance(tag['threshold'], (int, float)):
                raise ValueError(f"Tag missing 'threshold' or 'threshold' is not a number for content '{item['id']}'.")

    return content

def index_content_by_tags(content):
    """Indexes content by tags for efficient lookup.

    Args:
        content (list): A list of content dictionaries.

    Returns:
        dict: A dictionary mapping each (type, value) pair to a list of content items.
    """
    content_by_tags = {}
    for item in content:
        for tag in item['tags']:
            key = (tag['type'], tag['value'])
            if key not in content_by_tags:
                content_by_tags[key] = []
            content_by_tags[key].append(item)
    return content_by_tags

def match_content_to_users(users, content):
    """Matches content to users based on their interests.

    Args:
        users (list): A list of user dictionaries, each containing 'name' and 'interests'.
        content (list): A list of content dictionaries, each containing 'id', 'tags', etc.

    Returns:
        dict: A dictionary mapping each user name to a list of matching content items.
    """
    content_by_tags = index_content_by_tags(content)
    matches = {user['name']: [] for user in users}


    for user in users:
        seen_content_ids = set()
        for interest in user['interests']:
            key = (interest['type'], interest['value'])
            if key in content_by_tags:
                for item in content_by_tags[key]:
                   if (item['id'] not in seen_content_ids and 
                        any(tag['type'] == interest['type'] and 
                            tag['value'] == interest['value'] and 
                            tag['threshold'] >= interest['threshold'] for tag in item['tags'])):
                        matches[user['name']].append(item)
                        seen_content_ids.add(item['id'])

    return matches


@app.route('/')
def index():
    """Renders the main page with the user selection and content table.

    Returns:
        str: Rendered HTML of the main page.
    """
    global matches
    if not matches:
        users = load_users()
        content = load_content()
        matches = match_content_to_users(users, content)
    first_user_with_content = next((user['name'] for user in users if matches[user['name']]), users[0]['name'])
    return render_template('index.html', matches=matches, users=users, selected_user=first_user_with_content)


@app.route('/user_content', methods=['GET'])
def user_content():
    """Handles AJAX requests for user-specific content.

    Returns:
        Response: JSON response containing the content that matches the selected user's interests.
    """
    global matches
    if not matches:
        users = load_users()
        content = load_content()
        matches = match_content_to_users(users, content)
    
    selected_user = request.args.get('user')

    if selected_user in matches:
        user_matches = matches[selected_user]
    else:
        user_matches = []

    return jsonify(user_matches)

if __name__ == '__main__':
    app.run(debug=True)
