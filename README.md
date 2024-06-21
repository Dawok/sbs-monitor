# SBS monitor

This Python script monitors SBS Inkigayo photos board for new posts and sends notifications to Discord via a webhook with details about the new posts.

## Features

- Monitors SBS Inkigayo for new posts.
- Extracts and sends details of new posts to a discord webhook.
- Stores and tracks checked post numbers to avoid duplicate notifications.
- Filters posts by title using a configurable regex pattern.

## Prerequisites

- Python 3.x
- Required Python packages: `requests`, `beautifulsoup4`

Install the required packages using pip:
```bash
pip install requests beautifulsoup4
```
## Setup

1. Clone the repository.

2. Install the required Python libraries:
    ```sh
    pip install requests beautifulsoup4
    ```

3. Create a `config.json` file in the same directory as the script, and configure it with your settings. Here's an example configuration:
    ```json
    {
        "API_URL": "https://api.board.sbs.co.kr/bbs/V2.0/basic/board/lists?callback=boardListCallback_inkigayo_pt01&offset=0&limit=16&action_type=callback&board_code=inkigayo_pt01",
        "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/your_webhook_url",
        "CHECK_INTERVAL": 3600,
        "CHECKED_FILE": "checked.json",
        "TITLE_FILTER_REGEX": "."
    }
    ```

    - `API_URL`: The API URL from SBS, changing this should not be needed.
    - `DISCORD_WEBHOOK_URL`: Your Discord webhook URL.
    - `CHECK_INTERVAL`: Time in seconds between checks.
    - `CHECKED_FILE`: File to store checked board numbers.
    - `TITLE_FILTER_REGEX`: Regex pattern to filter post titles. Default is `.` which matches any title.


4. Run the script:
    ```sh
    python monitor.py
    ```


