"""
User interface utilities for InsightVM tools.

This module provides consistent UI elements including:
- Colored output
- Progress bars
- Interactive menus
- Confirmation prompts
- Formatted tables
"""

import sys
from enum import Enum
from typing import List, Optional, Any

try:
    from rich.console import Console  # type: ignore
    from rich.progress import (  # type: ignore
        Progress,
        SpinnerColumn,
        TextColumn
    )
    from rich.table import Table  # type: ignore
    from rich.panel import Panel  # type: ignore
    from rich.prompt import Prompt, Confirm  # type: ignore
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from src.rapid7.config import get_config


class Color(Enum):
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'


class UI:
    """
    User interface helper class.

    Provides methods for colored output, progress indicators,
    and interactive prompts with fallback support when rich is unavailable.
    """

    def __init__(self):
        """Initialize UI helper."""
        self.config = get_config()
        self.colored = self.config.get_preference('colored_output', True)

        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None

    def print_success(self, message: str) -> None:
        """
        Print success message in green.

        Args:
            message: Message to print
        """
        if RICH_AVAILABLE and self.console:
            self.console.print(f"[green]✓[/green] {message}")
        elif self.colored:
            print(f"{Color.GREEN.value}✓ {message}{Color.RESET.value}")
        else:
            print(f"✓ {message}")

    def print_error(self, message: str) -> None:
        """
        Print error message in red.

        Args:
            message: Message to print
        """
        if RICH_AVAILABLE and self.console:
            self.console.print(f"[red]✗[/red] {message}", file=sys.stderr)
        elif self.colored:
            print(
                f"{Color.RED.value}✗ {message}{Color.RESET.value}",
                file=sys.stderr
            )
        else:
            print(f"✗ {message}", file=sys.stderr)

    def print_warning(self, message: str) -> None:
        """
        Print warning message in yellow.

        Args:
            message: Message to print
        """
        if RICH_AVAILABLE and self.console:
            self.console.print(f"[yellow]⚠[/yellow] {message}")
        elif self.colored:
            print(f"{Color.YELLOW.value}⚠ {message}{Color.RESET.value}")
        else:
            print(f"⚠ {message}")

    def print_info(self, message: str) -> None:
        """
        Print info message in blue.

        Args:
            message: Message to print
        """
        if RICH_AVAILABLE and self.console:
            self.console.print(f"[blue]ℹ[/blue] {message}")
        elif self.colored:
            print(f"{Color.BLUE.value}ℹ {message}{Color.RESET.value}")
        else:
            print(f"ℹ {message}")

    def print_header(self, title: str) -> None:
        """
        Print formatted header.

        Args:
            title: Header title
        """
        if RICH_AVAILABLE and self.console:
            self.console.print(
                Panel(title, style="bold cyan", expand=False)
            )
        else:
            print("\n" + "=" * 80)
            print(f"  {title}")
            print("=" * 80)

    def print_separator(self) -> None:
        """Print a visual separator."""
        if RICH_AVAILABLE and self.console:
            self.console.print("[dim]" + "-" * 80 + "[/dim]")
        else:
            print("-" * 80)

    def print_table(
        self,
        title: str,
        headers: List[str],
        rows: List[List[Any]]
    ) -> None:
        """
        Print formatted table.

        Args:
            title: Table title
            headers: Column headers
            rows: Table rows
        """
        if RICH_AVAILABLE and self.console:
            table = Table(title=title, show_header=True, header_style="bold")
            for header in headers:
                table.add_column(header)
            for row in rows:
                table.add_row(*[str(cell) for cell in row])
            self.console.print(table)
        else:
            # Simple ASCII table fallback
            print(f"\n{title}")
            print("-" * 80)

            # Calculate column widths
            col_widths = [len(h) for h in headers]
            for row in rows:
                for i, cell in enumerate(row):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

            # Print headers
            header_row = " | ".join(
                h.ljust(w) for h, w in zip(headers, col_widths)
            )
            print(header_row)
            print("-" * len(header_row))

            # Print rows
            for row in rows:
                print(" | ".join(
                    str(cell).ljust(w)
                    for cell, w in zip(row, col_widths)
                ))

    def confirm(
        self,
        message: str,
        default: bool = False
    ) -> bool:
        """
        Ask for confirmation.

        Args:
            message: Confirmation prompt message
            default: Default value if user just presses Enter

        Returns:
            True if confirmed, False otherwise
        """
        if RICH_AVAILABLE:
            return Confirm.ask(message, default=default)
        else:
            suffix = " [Y/n]: " if default else " [y/N]: "
            response = input(message + suffix).strip().lower()

            if not response:
                return default

            return response in ['y', 'yes']

    def prompt(
        self,
        message: str,
        default: Optional[str] = None
    ) -> str:
        """
        Prompt for input.

        Args:
            message: Prompt message
            default: Default value if user just presses Enter

        Returns:
            User input string
        """
        if RICH_AVAILABLE:
            return Prompt.ask(message, default=default)
        else:
            suffix = f" [{default}]: " if default else ": "
            response = input(message + suffix).strip()
            return response if response else (default or "")

    def select_menu(
        self,
        title: str,
        options: List[str],
        allow_back: bool = True
    ) -> Optional[int]:
        """
        Display selection menu.

        Args:
            title: Menu title
            options: List of menu options
            allow_back: Whether to show "Back" option

        Returns:
            Selected option index (0-based) or None if back was selected
        """
        self.print_header(title)

        # Add back option if requested
        display_options = options.copy()
        if allow_back:
            display_options.append("← Back")

        # Display options
        for i, option in enumerate(display_options, 1):
            print(f"  {i}. {option}")

        print()

        while True:
            try:
                choice = input("Select an option (number): ").strip()

                if not choice:
                    continue

                num = int(choice)

                # Check if "Back" was selected
                if allow_back and num == len(display_options):
                    return None

                if 1 <= num <= len(options):
                    return num - 1
                else:
                    self.print_error(
                        f"Please enter a number between 1 and "
                        f"{len(display_options)}"
                    )
            except ValueError:
                self.print_error("Please enter a valid number")
            except (KeyboardInterrupt, EOFError):
                print()
                return None

    def progress_bar(
        self,
        description: str,
        total: Optional[int] = None
    ):
        """
        Create a progress bar context manager.

        Args:
            description: Progress description
            total: Total steps (None for indeterminate)

        Returns:
            Progress context manager

        Example:
            >>> ui = UI()
            >>> with ui.progress_bar("Processing", 100) as progress:
            ...     for i in range(100):
            ...         progress.update(1)
            ...         # do work
        """
        if RICH_AVAILABLE and self.config.get_preference(
            'show_progress_bars',
            True
        ):
            return Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            )
        else:
            # Simple fallback progress indicator
            return SimpleProgressBar(description, total, self)


class SimpleProgressBar:
    """Simple progress bar fallback when rich is not available."""

    def __init__(
        self,
        description: str,
        total: Optional[int],
        ui: UI
    ):
        """
        Initialize simple progress bar.

        Args:
            description: Progress description
            total: Total steps
            ui: UI instance
        """
        self.description = description
        self.total = total
        self.ui = ui
        self.current = 0

    def __enter__(self):
        """Enter context manager."""
        print(f"{self.description}...", end='', flush=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        if exc_type is None:
            print(" Done!")
        else:
            print(" Failed!")
        return False

    def update(self, advance: int = 1):
        """
        Update progress.

        Args:
            advance: Number of steps to advance
        """
        self.current += advance
        if self.total:
            percent = (self.current / self.total) * 100
            print(
                f"\r{self.description}... {percent:.0f}%",
                end='',
                flush=True
            )
        else:
            print('.', end='', flush=True)


def create_ui() -> UI:
    """
    Create UI instance.

    Returns:
        UI instance
    """
    return UI()
