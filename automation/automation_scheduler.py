#!/usr/bin/env python3
"""
MASTER AUTOMATION SCHEDULER
Coordinates all automated SEO and outreach tasks.

Runs on schedule:
- Daily SEO Agent: 09:00 UTC
- Backlink Outreach: 10:00 UTC
- Weekly SEO Review: Monday 09:00 UTC
- Logs all execution with proof
"""

import os
import sys
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/automation_scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('automation_scheduler')

@dataclass
class AutomationTask:
    """Represents an automated task"""
    name: str
    script_path: str
    schedule: str  # "daily@09:00", "weekly@monday09:00", etc.
    enabled: bool = True
    last_run: str = ""
    last_status: str = "pending"  # pending, success, failed

class AutomationScheduler:
    """Master controller for all automation"""

    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.automation_dir = self.root / "automation"
        self.logs_dir = self.root / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.tasks_file = self.root / "automation" / "tasks.json"
        self.execution_log = self.logs_dir / "automation_execution.log"

        # Define all automation tasks
        self.tasks = {
            "daily_seo_agent": AutomationTask(
                name="Daily SEO Analysis",
                script_path=str(self.automation_dir / "daily_seo_agent.py"),
                schedule="daily@09:00",
                enabled=True
            ),
            "backlink_outreach": AutomationTask(
                name="Backlink Outreach",
                script_path=str(self.automation_dir / "backlink_outreach_engine.py"),
                schedule="daily@10:00",
                enabled=True
            ),
            "weekly_seo_review": AutomationTask(
                name="Weekly SEO Review",
                script_path=str(self.automation_dir / "weekly_seo_review.py"),
                schedule="weekly@monday09:00",
                enabled=True
            )
        }

        logger.info("Automation Scheduler initialized")

    def save_tasks_state(self):
        """Save tasks state to JSON"""
        tasks_data = {
            k: {
                'name': v.name,
                'script': v.script_path,
                'schedule': v.schedule,
                'enabled': v.enabled,
                'last_run': v.last_run,
                'last_status': v.last_status
            }
            for k, v in self.tasks.items()
        }

        self.tasks_file.write_text(json.dumps(tasks_data, indent=2))
        logger.info(f"Tasks state saved to {self.tasks_file}")

    def execute_task(self, task_name):
        """Execute a single automation task"""
        task = self.tasks.get(task_name)
        if not task:
            logger.error(f"Task not found: {task_name}")
            return False

        if not task.enabled:
            logger.info(f"Task disabled: {task_name}")
            return False

        logger.info(f"EXECUTING TASK: {task.name}")

        try:
            # Run the script
            result = subprocess.run(
                [sys.executable, task.script_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info(f"✅ SUCCESS: {task.name}")
                task.last_status = "success"
                return True
            else:
                logger.error(f"❌ FAILED: {task.name}")
                logger.error(f"stderr: {result.stderr}")
                task.last_status = "failed"
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"❌ TIMEOUT: {task.name}")
            task.last_status = "timeout"
            return False
        except Exception as e:
            logger.error(f"❌ ERROR: {task.name} - {e}")
            task.last_status = "error"
            return False
        finally:
            task.last_run = datetime.now().isoformat()
            self.save_tasks_state()

    def run_all_tasks(self):
        """Run all enabled tasks"""
        logger.info("=" * 70)
        logger.info("AUTOMATION SCHEDULER - FULL RUN")
        logger.info(f"Time: {datetime.now().isoformat()}")
        logger.info("=" * 70)

        results = {}
        for task_name, task in self.tasks.items():
            if task.enabled:
                success = self.execute_task(task_name)
                results[task_name] = "success" if success else "failed"

        # Generate summary
        successes = sum(1 for v in results.values() if v == "success")
        total = len(results)

        logger.info("=" * 70)
        logger.info(f"AUTOMATION RUN COMPLETE")
        logger.info(f"Results: {successes}/{total} tasks successful")
        logger.info("=" * 70)

        return results

    def get_status(self):
        """Get current status of all automations"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "tasks": {}
        }

        for task_name, task in self.tasks.items():
            status["tasks"][task_name] = {
                "name": task.name,
                "enabled": task.enabled,
                "schedule": task.schedule,
                "last_run": task.last_run,
                "last_status": task.last_status
            }

        return status

    def print_status(self):
        """Print human-readable status"""
        status = self.get_status()

        print("\n" + "=" * 70)
        print("AUTOMATION SCHEDULER STATUS")
        print("=" * 70)
        print(f"Current Time: {status['timestamp']}\n")

        for task_name, task_info in status['tasks'].items():
            enabled = "✅" if task_info['enabled'] else "❌"
            last_status = task_info['last_status']
            status_icon = {
                "success": "✅",
                "failed": "❌",
                "pending": "⏳",
                "timeout": "⏱️ ",
                "error": "⚠️ "
            }.get(last_status, "❓")

            print(f"{enabled} {task_info['name']}")
            print(f"   Schedule: {task_info['schedule']}")
            print(f"   Status: {status_icon} {last_status}")
            print(f"   Last Run: {task_info['last_run'] or 'Never'}")
            print()

        print("=" * 70 + "\n")

if __name__ == "__main__":
    scheduler = AutomationScheduler()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            scheduler.print_status()
        elif sys.argv[1] == "--run-all":
            scheduler.run_all_tasks()
        elif sys.argv[1].startswith("--run="):
            task_name = sys.argv[1].replace("--run=", "")
            scheduler.execute_task(task_name)
    else:
        # Default: run all tasks
        scheduler.run_all_tasks()
        scheduler.print_status()
