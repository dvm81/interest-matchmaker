# Interest Matchmaker

## Overview

Interest Matchmaker is a simple web application that matches users with content based on the users' interests. The application allows to select from a dropdown of users and view content that aligns with the users' specified interests. The content is displayed in a table with pagination and search functionality.

## Features
- **User Selection**: Select a user from a dropdown list.
- **Content Matching**: View content that matches the selected user's interests.
- **Search**: Filter matched content using a search box.
- **Pagination**: Navigate through matched content using pagination controls (15 content items per page).

## Prerequisites

- **Python 3.7+** (developed with Python 3.10.7)
- **Flask** (Python web framework)
- **Jinja2** (for templating, comes with Flask)

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/dvm81/interest-matchmaker.git
cd interest-matchmaker
```

### Step 2: Set Up a Virtual Environment (in your favorite manner, for example:)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Prepare the Data Files (optional)
- If you want to use your own json files: place your `users.json` and `content.json` files in the `data/` directory, replacing the exisitng ones.
- These files should contain the users and content data in JSON format.
- There are already sample `users.json` and `content.json` files  in `data/` and the app will work with them. 

### Step 5: Run the Application (from project root directoy)
```bash
flask run
```
- The application will be available at `http://127.0.0.1:5000/`.

### Step 6: Access the Application
- Open your web browser and navigate to `http://127.0.0.1:5000/` to use the Interest Matchmaker app.

## Matching Logic

### Summary of Matching Logic
The matching logic has a preprocessing step (inverted index creation) and a matching step. 
- **Preprocessing step (index_content_by_tags function):**
  - The content (list of dictionaries) is indexed by tags to create an **inverted index** (Python dictionary mapping (type,value) to list of content items), allowing for efficient lookups when matching users to content.
  - **Example Output:**
If we have content items tagged with `('country', 'UK')` and `('topic', 'sports')`, the dictionary might look like this:

```python
{
    ('country', 'UK'): [content_item_1, content_item_2],
    ('topic', 'sports'): [content_item_3, content_item_4],
}
```

- **Matching step (match_content_to_users function):**
  - For each user, their interests are used to query the inverted index. Content items that meet the threshold criteria and haven’t already been matched are added to the user's list of matches.
  - **Example Output:**

If a user named "John" is interested in the "UK" (`('country', 'UK')`), and there are two content items that match this interest (and threshold criteria is met), the output might look like this:

```python
{
    "John": [content_item_1, content_item_2]
}
```

### Time Complexity Analysis

- **index_content_by_tags:** **O(n * m)**, where `n` is the number of content items and `m` is the average number of tags per content item. 

- **match_content_to_users:** **O(u * i * k)**, where `u` is the number of users, `i` is the average number of interests per user, and `k` is the average number of content items associated with each interest in the inverted index. In the worst case scenario, `k` could approach `n` (total number of content items). 

### Space Complexity:
- **index_content_by_tags:** The space complexity is `O(n * m)` because all the tags and their associated content items are stoired in the inverted index.
- **match_content_to_users:** The space complexity here is `O(u * k)` for storing the matches, where `k` is the average number of content items matched per user, `u` is the number of users.

This approach optimizes the matching process by using the inverted index to reduce the need for repeated searches through all content, making it efficient for large datasets.

## Running the unit tests (pytest)
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

## User Interface (UI) Structure
- Header (`<h1>`): Displays the title of the application.
- Upper Panel (`<div class="left-panel">`): Contains a dropdown (`<select>`) to choose a user.
- Lower Panel (`<div class="right-panel">`): Displays the matched content in a table. The table includes:
    - A search box to filter content.
    - A table with two columns: Title and Content.
    - Pagination buttons to navigate through content.

### JavaScript
- User Selection: When a user is selected, the content table is populated with matched content for that user.
- Search Functionality: The content table can be filtered using the search box, which searches through the titles and content.
- Pagination: Pagination buttons allow users to navigate through the list of matched content if there are more items than can be displayed on a single page.


### Styles (CSS)
- The application uses a simple CSS structure to style the layout, with a focus on a clean and user-friendly interface. The left upper and lower panel are distinct sections, with light colors to separate them visually.

### Troubleshooting
- Data Issues: Ensure that `users.json` and `content.json` are correctly formatted and located in the `data/` directory.
- Server Issues: If the server doesn't start, check for errors in the terminal and ensure all dependencies are installed.

### License
This project is licensed under the MIT License. 

### Contact
For any questions or support, please contact [dimiter.milushev@gmail.com].