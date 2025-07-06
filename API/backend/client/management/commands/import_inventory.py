from django.core.management.base import BaseCommand
from client.models import Product, ProductInventory, Sales
from datetime import timedelta, date
from client.utils import calculate_reorder_point
import numpy as np

class Command(BaseCommand):
    help = "Populate ProductInventory with reorder point and current stock"

    def handle(self, *args, **kwargs):
        today = date.today()
        last_30_days = today - timedelta(days=30)

        for product in Product.objects.select_related("supplier").all():
            supplier = product.supplier
            lead_time = supplier.lead_time or 5

            # Last 30 days of units sold
            recent_sales = Sales.objects.filter(product=product, date__gte=last_30_days).order_by("date")
            units_per_day = [s.units_sold for s in recent_sales]
            print(units_per_day)

            # Reorder point using statistical method
            reorder_point = calculate_reorder_point(
                units_sold_list=units_per_day,
                lead_time_days=lead_time,
                z_score=1.65  # 95% service level
            )

            # Current stock = max search interest
            max_search = Sales.objects.filter(product=product).order_by("-search_interest").first()
            current_amount = max_search.search_interest if max_search else 0

            safety_stock = max(10, int(np.mean(units_per_day or [1]) * 2))

            inventory, created = ProductInventory.objects.get_or_create(
                product=product,
                defaults={
                    "current_amount": current_amount,
                    "safe_stock": safety_stock,
                    "lead_time": lead_time,
                    "fulfillment_time": 2,
                    "reorder_point": reorder_point
                }
            )

            if not created:
                inventory.current_amount = current_amount
                inventory.safe_stock = safety_stock
                inventory.lead_time = lead_time
                inventory.reorder_point = reorder_point
                inventory.save()

        self.stdout.write(self.style.SUCCESS("✅ Inventory populated with reorder points and current amounts."))
