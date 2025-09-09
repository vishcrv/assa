from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.align import Align
from rich import box

class Dashboard:
    """
    Professional terminal dashboard for ASSA.
    Responsibilities:
    - show live status (current site, speed, paused/scrolling)
    - display key controls
    - display session summary at the end
    """
    def __init__(self):
        self.console = Console()
        self.panel = None      # stores current panel content
        self.live = None       # single Live instance

    def show_status(self, site_index, total_sites, url, speed, status):
        """
        Render live status panel with professional terminal aesthetic
        """
        # create status information with clean formatting
        status_info = Table.grid(padding=(0, 2))
        status_info.add_column(style="white", justify="left", min_width=12)
        status_info.add_column(style="cyan", justify="left")
        
        # truncates URL if long
        display_url = url if len(url) <= 80 else url[:77] + "..."
        
        status_info.add_row("SITE:", f"{site_index}/{total_sites}")
        status_info.add_row("URL:", display_url)
        status_info.add_row("SPEED:", speed.upper())
        status_info.add_row("STATUS:", status.upper())
        
        # create controls table
        controls = Table.grid()
        controls.add_column(style="dim white")
        controls.add_row("\nKEY BINDINGS:")
        controls.add_row("[1] Slow   [2] Medium   [3] Fast")
        controls.add_row("[p] Pause/Resume   [n] Next   [b] Prev   [q] Quit")
        
        # combine status and controls
        main_content = Table.grid()
        main_content.add_column()
        main_content.add_row(status_info)
        main_content.add_row(controls)
        
        panel = Panel(
            main_content,
            title="[bold white]ASSA[/bold white]",
            border_style="white",
            box=box.ROUNDED,
            expand=True
        )

        # initialize live only once
        if self.live is None:
            self.live = Live(panel, refresh_per_second=4)
            self.live.start()
        else:
            self.live.update(panel)

    def show_summary(self, records):
        """
        Display session summary with professional formatting
        """
        if self.live:
            self.live.stop()  # stop live panel to prevent duplicate frames

        # clear and show completion message
        self.console.clear()
        
        header_text = Text("SESSION COMPLETED", style="bold white")
        header_panel = Panel(
            Align.center(header_text),
            border_style="green",
            box=box.ROUNDED
        )
        self.console.print(header_panel)
        self.console.print()

        if not records:
            self.console.print(Panel(
                "[dim white]No sites were visited during this session.[/dim white]",
                border_style="yellow"
            ))
            return

        # create professional table
        table = Table(
            title="SESSION SUMMARY",
            title_style="bold white",
            border_style="white",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold white"
        )
        table.add_column("#", style="cyan", width=4, justify="center")
        table.add_column("URL", style="white", min_width=40)
        table.add_column("DURATION", style="green", width=12, justify="center")

        for i, record in enumerate(records, 1):
            # truncate URL for better display
            display_url = record['url'] if len(record['url']) <= 60 else record['url'][:57] + "..."
            table.add_row(str(i), display_url, record['time_spent'])

        self.console.print(table)
        self.console.print()
        
        # final message
        final_msg = Panel(
            "[dim white]thank you for using ASSA - automated search scrolling agent[/dim white]",
            border_style="dim white"
        )
        self.console.print(final_msg)
