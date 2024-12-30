#!/usr/bin/env python3

import curses
import os
import subprocess
import platform

def get_ssh_agents():
    """Retrieve a list of configured SSH agents for VS Code."""
    if platform.system() == "Windows":
        ssh_config_path = os.path.join(os.environ["USERPROFILE"], ".ssh", "config")
    else:
        ssh_config_path = os.path.expanduser("~/.ssh/config")
    
    agents = []

    if os.path.exists(ssh_config_path):
        with open(ssh_config_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("Host ") and not line.startswith("Host *"):
                    agents.append(line.split(" ")[1])

    return agents

def open_vscode_with_agent(agent):
    """Open VS Code with the selected SSH agent."""
    if platform.system() == "Windows":
        vscode_path = "C:\\Program Files\\Microsoft VS Code\\Code.exe"  # Replace this with the actual path to the `code` executable on Windows
    else:
        vscode_path = "/usr/local/bin/code"  # Replace this with the actual path to the `code` executable on macOS/Linux

    command = [vscode_path, "--new-window", "--remote", f"ssh-remote+{agent}"]
    subprocess.run(command)

def tui(stdscr):
    """TUI for selecting an SSH agent."""
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

    agents = get_ssh_agents()
    agents.append("Exit")  # Add the Exit option

    if not agents:
        stdscr.addstr(0, 0, "No SSH agents configured in ~/.ssh/config.")
        stdscr.refresh()
        stdscr.getch()
        return

    current_selection = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select an SSH agent to open VS Code:")

        for idx, agent in enumerate(agents):
            if idx == current_selection:
                stdscr.addstr(idx + 1, 0, f"> {agent}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, f"  {agent}")

        key = stdscr.getch()

        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(agents) - 1:
            current_selection += 1
        elif key in [10, 13]:  # Enter key
            selected_agent = agents[current_selection]
            if selected_agent == "Exit":
                break
            open_vscode_with_agent(selected_agent)
            break

if __name__ == "__main__":
    curses.wrapper(tui)
