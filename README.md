# JustServers

A simple, efficient TUI for managing Minecraft servers locally over SSH.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration:**
    Edit `config.toml` to define your servers.
    ```toml
    [[servers]]
    name = "My Survival Server"
    jar_path = "/path/to/server.jar"
    working_dir = "/path/to/server_folder"
    min_mem = "2G"
    max_mem = "4G"
    ```

3.  **Run:**
    ```bash
    python main.py
    ```

## Features

-   **Multi-server management:** Switch between servers in the sidebar.
-   **Live Console:** View logs and send commands in real-time.
-   **Process Control:** Start and Stop servers safely.
-   **Resource Efficient:** Lightweight TUI built on Textual.

## Requirements

-   Python 3.8+
-   Java (installed and in PATH)
