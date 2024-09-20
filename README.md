# Conduit

Conduit is an application that acts as a bridge between Azure DevOps and Grafana, allowing you to display project details in a beautiful dashboard.

## Instructions
- Place docs/ParentTask1Sprint86Dump.json docs/Sprint86Dump.json docs/SprintsDump.json in correct places to run the bridge with example dump
- Install [Infinity Datasource](https://grafana.com/docs/plugins/yesoreyeram-infinity-datasource/latest/) as per the instructions
- You can use `uv` to install requirements by running `uv sync` against `uv.lock` else plain old requirements.txt works
- Start the api server : `uv run conduit/main.py`
- Start grafana service and open grafana locally.
- Import dashboard by uploading the dashboard json export

> [!NOTE]
> There are TODO comments in the main script to use example json dumps. Remove them once the sprintlist api endpoint works. Rest should work outside the box
> The server has certain endpoints which query someother endpoints of its own. Could be better optimized by storing or caching.

## API Endpoints Documentation

### 1. `/sprintlist`
- **Method:** GET
- **Description:** Returns a JSON object with a key `value` and the value is a list of sprint objects.
- **Response Example:**
    ```json
    {
        "value": [
            {
            "attributes": {
                "finishDate": "2021-06-13T00:00:00Z",
                "startDate": "2021-05-31T00:00:00Z",
                "timeFrame": "past"
            },
            "id": "...",
            "name": "Sprint007",
            "path": "...",
            "url": "..."
            },
        ]
    }
    ```

### 2. `/parentItems`
- **Method:** GET
- **Description:** Returns a JSON object with a key `parent` and the value is a list of parent item objects.
- **Query Parameters:**
    - `sprint` (required): The name of the sprint.
- **Response Example:**
    ```json
    {
        "parent": [
            {
            "id": 2539400,
            "url": "..."
            },
            {
            "id": 3581941,
            "url": "..."
            }
        ]
    }
    ```

### 3. `/parentTask`
- **Method:** GET
- **Description:** Returns a JSON object containing the details of a parent task.
- **Query Parameters:**
    - `sprint` (required): The name of the sprint.
    - `parentID` (required): The ID of the parent task.
- **Response Example:**
    ```json
    {
    "AssignedTo": "LastNameUser1, FirstNameUser1",
    "Custom.TargetVersion": "20.00.00.00",
    "System.State": "Committed",
    "System.Title": "..."
    }
    ```

## Features

- Fetch data from Azure DevOps
- Transform and aggregate data
- Display data in Grafana dashboard

## Tasks
- [x] Fetch RSS Feed and parse to display in grafana
![rss feed](docs/assets/rss_feed.png)
- [x] Display Json Dumps
![Json Dump](docs/assets/example_dashboard.png)
