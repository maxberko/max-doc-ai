#!/usr/bin/env python3
"""
Progress Feedback System

Provides visual feedback and progress indicators for long-running operations
"""

import sys
import time
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
import threading


@dataclass
class Step:
    """Represents a workflow step"""
    name: str
    status: str  # pending, in_progress, completed, skipped, failed
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    details: Optional[str] = None
    substeps: List['Step'] = None

    def __post_init__(self):
        if self.substeps is None:
            self.substeps = []


class ProgressTracker:
    """Track and display progress for multi-step workflows"""

    SYMBOLS = {
        'pending': '⏸️ ',
        'in_progress': '🔄',
        'completed': '✅',
        'skipped': '⏭️ ',
        'failed': '❌',
        'warning': '⚠️ '
    }

    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'red': '\033[91m',
        'cyan': '\033[96m'
    }

    def __init__(self, total_steps: int = 0, show_timestamps: bool = False):
        self.total_steps = total_steps
        self.current_step = 0
        self.steps: List[Step] = []
        self.show_timestamps = show_timestamps
        self.start_time = datetime.now()
        self._spinner_active = False
        self._spinner_thread = None

    def add_step(self, name: str, status: str = 'pending', details: str = None):
        """Add a new step to track"""
        step = Step(name=name, status=status, details=details)
        self.steps.append(step)
        if self.total_steps == 0:
            self.total_steps = len(self.steps)

    def start_step(self, step_name: str, details: str = None):
        """Mark a step as in progress"""
        step = self._find_step(step_name)
        if step:
            step.status = 'in_progress'
            step.start_time = datetime.now()
            if details:
                step.details = details
            self.current_step = self.steps.index(step) + 1

        self._print_step_status(step_name, 'in_progress', details)

    def complete_step(self, step_name: str, details: str = None):
        """Mark a step as completed"""
        step = self._find_step(step_name)
        if step:
            step.status = 'completed'
            step.end_time = datetime.now()
            if details:
                step.details = details

        duration = self._get_duration(step) if step else None
        self._print_step_status(step_name, 'completed', details, duration)

    def skip_step(self, step_name: str, reason: str = None):
        """Mark a step as skipped"""
        step = self._find_step(step_name)
        if step:
            step.status = 'skipped'
            step.details = reason

        self._print_step_status(step_name, 'skipped', reason)

    def fail_step(self, step_name: str, error: str = None):
        """Mark a step as failed"""
        step = self._find_step(step_name)
        if step:
            step.status = 'failed'
            step.end_time = datetime.now()
            step.details = error

        self._print_step_status(step_name, 'failed', error)

    def _find_step(self, step_name: str) -> Optional[Step]:
        """Find a step by name"""
        for step in self.steps:
            if step.name == step_name:
                return step
        # If not found, create it
        self.add_step(step_name)
        return self.steps[-1]

    def _get_duration(self, step: Step) -> Optional[str]:
        """Calculate step duration"""
        if step.start_time and step.end_time:
            delta = step.end_time - step.start_time
            seconds = delta.total_seconds()
            if seconds < 1:
                return f"{int(seconds * 1000)}ms"
            elif seconds < 60:
                return f"{seconds:.1f}s"
            else:
                minutes = int(seconds // 60)
                secs = int(seconds % 60)
                return f"{minutes}m {secs}s"
        return None

    def _print_step_status(self, step_name: str, status: str, details: str = None, duration: str = None):
        """Print step status with formatting"""
        symbol = self.SYMBOLS.get(status, '•')

        # Color based on status
        if status == 'completed':
            color = self.COLORS['green']
        elif status == 'in_progress':
            color = self.COLORS['cyan']
        elif status == 'skipped':
            color = self.COLORS['yellow']
        elif status == 'failed':
            color = self.COLORS['red']
        else:
            color = self.COLORS['reset']

        # Build output
        progress = f"[{self.current_step}/{self.total_steps}]" if self.total_steps > 0 else ""
        output = f"{color}{symbol} {progress} {step_name}{self.COLORS['reset']}"

        if details:
            output += f" {self.COLORS['dim']}{details}{self.COLORS['reset']}"

        if duration:
            output += f" {self.COLORS['dim']}({duration}){self.COLORS['reset']}"

        print(output)

    def print_summary(self):
        """Print final summary of all steps"""
        print("\n" + "=" * 70)
        print(f"{self.COLORS['bold']}📊 Workflow Summary{self.COLORS['reset']}")
        print("=" * 70)

        total_duration = (datetime.now() - self.start_time).total_seconds()

        # Count statuses
        completed = sum(1 for s in self.steps if s.status == 'completed')
        skipped = sum(1 for s in self.steps if s.status == 'skipped')
        failed = sum(1 for s in self.steps if s.status == 'failed')

        print(f"\n{self.COLORS['green']}✅ Completed: {completed}{self.COLORS['reset']}")
        if skipped > 0:
            print(f"{self.COLORS['yellow']}⏭️  Skipped: {skipped}{self.COLORS['reset']}")
        if failed > 0:
            print(f"{self.COLORS['red']}❌ Failed: {failed}{self.COLORS['reset']}")

        print(f"\n⏱️  Total time: {self._format_duration(total_duration)}")

        # Detailed breakdown
        print(f"\n{self.COLORS['bold']}Step Details:{self.COLORS['reset']}")
        for i, step in enumerate(self.steps, 1):
            symbol = self.SYMBOLS.get(step.status, '•')
            duration = self._get_duration(step)
            duration_str = f" ({duration})" if duration else ""

            print(f"  {i}. {symbol} {step.name}{duration_str}")
            if step.details:
                print(f"     {self.COLORS['dim']}{step.details}{self.COLORS['reset']}")

        print("\n" + "=" * 70 + "\n")

    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable form"""
        if seconds < 1:
            return f"{int(seconds * 1000)}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        else:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"

    def start_spinner(self, message: str):
        """Start an animated spinner for long operations"""
        self._spinner_active = True
        self._spinner_thread = threading.Thread(target=self._spin, args=(message,))
        self._spinner_thread.daemon = True
        self._spinner_thread.start()

    def stop_spinner(self):
        """Stop the spinner"""
        self._spinner_active = False
        if self._spinner_thread:
            self._spinner_thread.join()
        # Clear the line
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()

    def _spin(self, message: str):
        """Spinner animation"""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        while self._spinner_active:
            frame = frames[i % len(frames)]
            sys.stdout.write(f'\r{self.COLORS["cyan"]}{frame} {message}...{self.COLORS["reset"]}')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1


class StatusBox:
    """Display a status box with key information"""

    def __init__(self, title: str, width: int = 70):
        self.title = title
        self.width = width
        self.items = []

    def add_item(self, label: str, value: str, status: str = None):
        """Add an item to the status box"""
        self.items.append({
            'label': label,
            'value': value,
            'status': status
        })

    def print(self):
        """Print the status box"""
        colors = ProgressTracker.COLORS
        symbols = ProgressTracker.SYMBOLS

        print("\n" + "═" * self.width)
        print(f"{colors['bold']}{self.title.center(self.width)}{colors['reset']}")
        print("═" * self.width)

        for item in self.items:
            label = item['label']
            value = item['value']
            status = item['status']

            if status:
                symbol = symbols.get(status, '•')
                print(f"{symbol} {colors['bold']}{label}:{colors['reset']} {value}")
            else:
                print(f"  {colors['bold']}{label}:{colors['reset']} {value}")

        print("═" * self.width + "\n")


def demo():
    """Demo the progress tracker"""
    tracker = ProgressTracker(total_steps=7)

    # Add steps
    tracker.add_step("Research codebase", "pending")
    tracker.add_step("Classify feature", "pending")
    tracker.add_step("Capture screenshots", "pending")
    tracker.add_step("Upload to CDN", "pending")
    tracker.add_step("Create documentation", "pending")
    tracker.add_step("Sync to Pylon", "pending")
    tracker.add_step("Generate announcements", "pending")

    # Execute steps
    tracker.start_step("Research codebase", "Analyzing 247 files")
    time.sleep(1)
    tracker.complete_step("Research codebase", "Found 12 relevant files")

    tracker.start_step("Classify feature", "Analyzing file patterns")
    time.sleep(0.5)
    tracker.complete_step("Classify feature", "Detected: DATA_ENHANCEMENT (95% confidence)")

    tracker.skip_step("Capture screenshots", "No UI changes detected")
    tracker.skip_step("Upload to CDN", "No screenshots to upload")

    tracker.start_step("Create documentation", "Updating 4 files")
    time.sleep(1.5)
    tracker.complete_step("Create documentation", "Updated English + French docs")

    tracker.start_step("Sync to Pylon", "Syncing 2 articles")
    time.sleep(1)
    tracker.complete_step("Sync to Pylon", "Published successfully")

    tracker.start_step("Generate announcements", "Creating 6 variants")
    time.sleep(0.8)
    tracker.complete_step("Generate announcements", "All announcements ready")

    # Print summary
    tracker.print_summary()

    # Demo status box
    box = StatusBox("🚀 Release Configuration")
    box.add_item("Feature", "Manager Column CSV Exports")
    box.add_item("Type", "DATA_ENHANCEMENT", "completed")
    box.add_item("Screenshots", "Not needed", "skipped")
    box.add_item("Documentation", "Updated", "completed")
    box.add_item("Announcements", "6 variants created", "completed")
    box.print()


if __name__ == '__main__':
    demo()
