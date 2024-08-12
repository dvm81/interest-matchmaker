# Interest Matchmaker

## Overview

Interest Matchmaker is a web application that matches users with content based on their interests. The application allows users to select from a dropdown of users and view content that aligns with their specified interests. The content is displayed in a table with pagination and search functionality.

## Features
- **User Selection**: Select a user from a dropdown list.
- **Content Matching**: View content that matches the selected user's interests.
- **Search**: Filter matched content using a search box.
- **Pagination**: Navigate through content using pagination controls.

## Prerequisites

- **Python 3.7+**
- **Flask** (Python web framework)
- **Jinja2** (for templating, comes with Flask)

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/dvm81/interest-matchmaker.git
cd interest-matchmaker
```

### Step 2: Set Up a Virtual Environment (in your favorite manner)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Prepare the Data Files (optional)
- If you want to use your own json files: place `users.json` and `content.json` files in the `data/` directory.
- These files should contain the users and content data in JSON format.
- There are already sample `users.json` and `content.json` files and the app will work with them. 

### Step 5: Run the Application
```bash
flask run
```
- The application will be available at `http://127.0.0.1:5000/`.

### Step 6: Access the Application
- Open your web browser and navigate to `http://127.0.0.1:5000/` to use the Interest Matchmaker.

### Matching Logic
### Matching Logic Explanation


#### 1. **index_content_by_tags(content) Function**

This function creates an **inverted index** that maps content tags to the content items that contain them. The idea is to preprocess the content so that when matching users to content, we can quickly find relevant content items based on the user's interests.

**Steps:**

1. **Initialize an Empty Dictionary (`content_by_tags`)**:
   - This dictionary will hold keys that are tuples representing a tag's type and value (e.g., `('topic', 'sports')`) and values that are lists of content items associated with those tags.

2. **Iterate Over Each Content Item**:
   - For each content item in the list, iterate over its tags.

3. **Generate a Key for Each Tag**:
   - Each tag has a `type` and a `value`. These are combined into a tuple, which serves as the key in the `content_by_tags` dictionary.

4. **Add the Content Item to the Corresponding List in the Dictionary**:
   - If the key already exists in the dictionary, the content item is appended to the existing list.
   - If the key doesn't exist, a new list is created with the content item as its first entry.

5. **Return the Dictionary**:
   - The resulting dictionary maps each unique `(type, value)` pair to a list of content items that have that tag.

**Example Output:**

If we have content items tagged with `('country', 'UK')` and `('topic', 'sports')`, the dictionary might look like this:

```python
{
    ('country', 'UK'): [content_item_1, content_item_2],
    ('topic', 'sports'): [content_item_3, content_item_4],
}
```

This preprocessing step allows for efficient lookups when matching content to users.

#### 2. **match_content_to_users(users, content) Function**

This function matches users to content based on their interests using the inverted index created by `index_content_by_tags`.

**Steps:**

1. **Create the Inverted Index**:
   - The `content_by_tags` dictionary is created by calling `index_content_by_tags(content)`.

2. **Initialize an Empty Dictionary (`matches`)**:
   - This dictionary will hold user names as keys and lists of matching content items as values.

3. **Iterate Over Each User**:
   - For each user, initialize an empty set `seen_content_ids` to keep track of content items that have already been matched for that user (to avoid duplicates).

4. **Iterate Over Each Interest of the User**:
   - For each interest (which has a `type`, `value`, and `threshold`), generate a key (`(interest['type'], interest['value'])`) to look up in the `content_by_tags` dictionary.

5. **Check for Matching Content Items**:
   - If the key exists in `content_by_tags`, retrieve the list of content items associated with that tag.
   - For each content item in this list:
     - Check if the content item's ID has already been seen for this user (using `seen_content_ids`).
     - If not, check if the content item’s tag threshold meets or exceeds the user's interest threshold.
     - If both conditions are met, add the content item to the user's list of matches and mark the content item ID as seen.

6. **Return the Matches Dictionary**:
   - The resulting `matches` dictionary maps each user's name to a list of content items that match their interests.

**Example Output:**

If a user named "John" is interested in the "UK" (`('country', 'UK')`), and there are two content items that match this interest, the output might look like this:

```python
{
    "John": [content_item_1, content_item_2]
}
```

### Summary of Matching Logic

- **Preprocessing (index_content_by_tags):**
  - The content is indexed by tags to create an inverted index, allowing for efficient lookups when matching users to content.

- **Matching (match_content_to_users):**
  - For each user, their interests are used to query the inverted index. Content items that meet the threshold criteria and haven’t already been matched are added to the user's list of matches.

### Time Complexity Analysis

- **index_content_by_tags:** **O(n * m)**, where `n` is the number of content items and `m` is the average number of tags per content item. This is because each tag of every content item is processed to build the inverted index.

- **match_content_to_users:** **O(u * i * k)**, where `u` is the number of users, `i` is the number of interests per user, and `k` is the number of content items associated with each interest in the inverted index. The complexity arises because, for each user interest, a lookup is performed in the index, and each matching content item is checked against the user's threshold.

This approach optimizes the matching process by using the inverted index to reduce the need for repeated searches through all content, making it efficient for large datasets.

### Running all the tests 
```bash
pytest -v
```
-v stands for "verbose" and will show each test being run along with the result.
-s will allow you to see the output from print statements within your tests.

Alternatively, running exclusively:
- the matching logic tests 
```bash
pytest tests/test_match_logic.py -v 
```
- data ingestion process tests 
```bash
pytest tests/test_data_ingest.py  -v 
```

### User Interface (UI) Structure
- Header (`<h1>`): Displays the title of the application.
- Left Panel (`<div class="left-panel">`): Contains a dropdown (`<select>`) to choose a user.
- Right Panel (`<div class="right-panel">`): Displays the matched content in a table. The table includes:
    - A search box to filter content.
    - A table with two columns: Title and Content.
    - Pagination buttons to navigate through content.

### JavaScript
- User Selection: When a user is selected, the content table is populated with matched content for that user.
- Search Functionality: The content table can be filtered using the search box, which searches through the titles and content.
- Pagination: Pagination buttons allow users to navigate through the list of matched content if there are more items than can be displayed on a single page.


### Styles (CSS)
- The application uses a simple CSS structure to style the layout, with a focus on a clean and user-friendly interface. The left panel and right panel are distinct sections, with light colors to separate them visually.

### Troubleshooting
- Data Issues: Ensure that `users.json` and `content.json` are correctly formatted and located in the `data/` directory.
- Server Issues: If the server doesn't start, check for errors in the terminal and ensure all dependencies are installed.

### License
This project is licensed under the MIT License. 

### Contact

For any questions or support, please contact [dimiter.milushev@gmail.com].