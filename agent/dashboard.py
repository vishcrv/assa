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
        Ultra-compact dynamic status display
        """
        w = self.console.size.width
        
        # Extract domain from URL for compact display
        try:
            if 'http' in url:
                domain = url.split('/')[2].replace('www.', '')
            else:
                domain = url[:15]
        except:
            domain = url[:15]
        
        # Ultra-compact single line status
        max_domain = max(10, w - 35)  # Dynamic domain length
        short_domain = domain[:max_domain] + "..." if len(domain) > max_domain else domain
        
        # Create compact status line
        status_line = f"[cyan]{site_index}/{total_sites}[/cyan] │ [white]{short_domain}[/white] │ [yellow]{speed[0].upper()}[/yellow] │ [green]{status[:4]}[/green]"
        
        # Dynamic controls based on width
        if w < 50:
            controls_line = "[dim]1/2/3 p n b q[/dim]"
        elif w < 70:
            controls_line = "[dim]1/2/3=Speed p=Pause n=Next b=Prev q=Quit[/dim]"
        else:
            controls_line = "[dim][1/2/3] Speed • [p] Pause • [n] Next • [b] Prev • [q] Quit[/dim]"
        
        # Minimal content
        content = f"{status_line}\n{controls_line}"
        
        panel = Panel(
            content,
            title="[bold]assa[/bold]" if w >= 40 else "[bold]AR[/bold]",
            border_style="cyan",
            box=box.MINIMAL,
            expand=True,
            padding=(0, 1)
        )

        # Initialize or update live display with minimal overhead
        if self.live is None:
            self.live = Live(panel, refresh_per_second=15, console=self.console, auto_refresh=True)
            self.live.start()
        else:
            self.live.update(panel)

    def show_summary(self, records):
        """
        Ultra-compact responsive summary
        """
        if self.live:
            self.live.stop()

        self.console.clear()

        # Header (minimal)
        header = Panel("[bold]SUMMARY[/bold]", border_style="green", box=box.MINIMAL, padding=(0,1))
        self.console.print(header)

        if not records:
            self.console.print(Panel("[dim]No sites visited[/dim]", border_style="yellow", box=box.MINIMAL, padding=(0,1)))
            return

        # Width-aware table
        w = self.console.size.width
        table = Table(box=box.MINIMAL, border_style="white", expand=True, show_header=True, header_style="bold")
        
        if w < 60:
            table.add_column("#", width=3, justify="center", style="cyan")
            table.add_column("SITE", style="white")
            table.add_column("TIME", width=8, justify="center", style="green")
            for i, r in enumerate(records, 1):
                url = r['url']
                domain = (url.split('/')[2] if '//' in url and len(url.split('/'))>2 else url).replace('www.', '')
                site = domain[:15] + "..." if len(domain) > 15 else domain
                table.add_row(str(i), site, r['time_spent'])
        else:
            table.add_column("#", width=4, justify="center", style="cyan")
            table.add_column("URL", style="white")
            table.add_column("DURATION", width=12, justify="center", style="green")
            max_url = max(30, w - 25)
            for i, r in enumerate(records, 1):
                url = r['url']
                site = url if len(url) <= max_url else url[:max_url-3] + "..."
                table.add_row(str(i), site, r['time_spent'])

        self.console.print(table)
        
        # Footer (minimal)
        footer = Panel("[dim]Done[/dim]", border_style="dim", box=box.MINIMAL, padding=(0,1))
        self.console.print(footer)
