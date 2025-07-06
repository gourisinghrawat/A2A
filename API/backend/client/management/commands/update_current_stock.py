import random
from django.core.management.base import BaseCommand
from client.models import ProductInventory  # Replace 'client' with your app name

class Command(BaseCommand):
    help = 'Update current stock based on safe stock ± random(-100 to 100)'

    def handle(self, *args, **kwargs):
        inventories = ProductInventory.objects.all()

        for inv in inventories:
            # Calculate new stock value
            fluctuation = random.randint(-100, 100)
            new_stock = inv.safe_stock + fluctuation+ inv.reorder_point * random.randint(0,1)
            new_stock = max(new_stock, 0)  # Ensure stock doesn't go below 0

            # Update and save
            inv.current_amount = new_stock
            inv.save()

            # Print for confirmation
            self.stdout.write(self.style.SUCCESS(
                f"✅ {inv.product.name}: current stock set to {inv.current_amount} (safe={inv.safe_stock}, Δ={fluctuation})"
            ))
