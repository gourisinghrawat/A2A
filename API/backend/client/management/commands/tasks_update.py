# client/management/commands/run_inventory_tasks.py
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command('update_reorder_points')

