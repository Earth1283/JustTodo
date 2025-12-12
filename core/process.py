import asyncio
import subprocess
from typing import Optional, AsyncGenerator
from pathlib import Path

def is_server_running(process: Optional[asyncio.subprocess.Process]) -> bool:
    """Asks \"Are you alive?\" to the server proc"""
    return process is not None and process.returncode is None


async def start_server(
    jar_path: str, working_dir: str, min_mem: str = "2G", max_mem: str = "4G"
) -> Optional[asyncio.subprocess.Process]:
    """
    Starts the Java process asynchronously.
    Returns the Process object if started successfully, else None.
    """
    # Construct the command list (safe, no shell=True injection risks)
    cmd = [
        "java",
        f"-Xms{min_mem}",
        f"-Xmx{max_mem}",
        "-jar",
        jar_path,
        "nogui",
    ]

    try:
        # stdin=PIPE allows us to write commands
        # stdout=PIPE allows us to read logs
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=Path(working_dir),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge error logs into standard output
        )
        return process
    except FileNotFoundError:
        # Java not installed or path wrong
        return None


async def stop_server(process: Optional[asyncio.subprocess.Process]):
    """
    Gracefully stops the server.
    """
    # 1. Check if it's already dead or None
    if process is None or process.returncode is not None:
        return

    # Now we know process is running
    await write_command(process, "stop")

    try:
        await asyncio.wait_for(process.wait(), timeout=30.0)
    except asyncio.TimeoutError:
        process.kill()


async def write_command(process: Optional[asyncio.subprocess.Process], command: str):
    """
    Sends a command to the Minecraft console (stdin).
    """
    # Check both process existence AND stdin pipe existence
    if process is None or process.stdin is None:
        return

    try:
        process.stdin.write(f"{command}\n".encode())
        await process.stdin.drain()
    except BrokenPipeError:
        # Server crashed or closed unexpectedly
        pass


async def stream_logs(
    process: Optional[asyncio.subprocess.Process],
) -> AsyncGenerator[str, None]:
    """
    Yields log lines.
    """
    # Check process AND stdout pipe
    if process is None or process.stdout is None:
        return

    async for line in process.stdout:
        yield line.decode("utf-8", errors="replace").strip()
