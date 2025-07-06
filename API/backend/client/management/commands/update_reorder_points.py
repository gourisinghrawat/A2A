from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import date
from calendar import monthrange
from client.models import ProductInventory, Sales
from django.db.models import Sum
import numpy as np

class Command(BaseCommand):
    help = 'Calculates monthly reorder points for all products using same month of previous year'

    def handle(self, *args, **options):
        z_score = 1.65  # 95% service level
        current_month=now().month
        current_year = now().date().year
        previous_year = current_year - 1

        inventories = ProductInventory.objects.select_related('product__supplier')
        start_date=date(previous_year,current_month,1)
        end_day=monthrange(previous_year,current_month)[1]
        end_date=date(previous_year,current_month,end_day)
        self.stdout.write(f"\n📅 Month {current_month}: Using data from {start_date} to {end_date}")
        



        for inventory in inventories:
            sales_qs = Sales.objects.filter(product=inventory.product, date__range=(start_date, end_date))
                
            if not sales_qs.exists():
                self.stdout.write(self.style.WARNING(
                    f"No sales data for {inventory.product.name} in {start_date.strftime('%B %Y')}. Skipping."
                ))
                continue
            sales_by_day = sales_qs.values('date').annotate(daily_total=Sum('units_sold')).order_by('date')
            daily_units = [entry['daily_total'] for entry in sales_by_day]

            avg_daily_usage = sum(daily_units) / len(daily_units)
            std_dev_daily_usage = np.std(daily_units)
            print(avg_daily_usage)
            leadtime=inventory.lead_time
            safety_stock = z_score * std_dev_daily_usage * (inventory.order_frequency ** 0.5)
            # reorder_point = (avg_daily_usage * leadtime) + safety_stock
            reorder_point=(avg_daily_usage* (inventory.order_frequency-leadtime))+safety_stock
            inventory.safe_stock = int(round(safety_stock))
            inventory.reorder_point = int(round(reorder_point))
            inventory.save()

            self.stdout.write(self.style.SUCCESS(
                f"[{start_date.strftime('%b')}] {inventory.product.name} → ROP={inventory.reorder_point}, Safety Stock={inventory.safe_stock}"
            ))



        # 
        # for month in range(1, 13):  # Loop through January to December
        #     start_date = date(previous_year, month, 1)
        #     end_day = monthrange(previous_year, month)[1]
        #     end_date = date(previous_year, month, end_day)

        #     self.stdout.write(f"\n📅 Month {month}: Using data from {start_date} to {end_date}")

        #     for inventory in inventories:
        #         sales_qs = Sales.objects.filter(product=inventory.product, date__range=(start_date, end_date))
                
        #         if not sales_qs.exists():
        #             self.stdout.write(self.style.WARNING(
        #                 f"No sales data for {inventory.product.name} in {start_date.strftime('%B %Y')}. Skipping."
        #             ))
        #             continue

        #         sales_by_day = sales_qs.values('date').annotate(daily_total=Sum('units_sold')).order_by('date')
        #         daily_units = [entry['daily_total'] for entry in sales_by_day]

        #         avg_daily_usage = sum(daily_units) / len(daily_units)
        #         std_dev_daily_usage = np.std(daily_units)

        #         lead_time = inventory.lead_time or inventory.product.supplier.lead_time
        #         safety_stock = z_score * std_dev_daily_usage * (lead_time ** 0.5)
        #         print(avg_daily_usage)
        #         reorder_point = (avg_daily_usage * lead_time) + safety_stock

        #         # Optionally, store month-specific ROP/safety_stock somewhere else (e.g., ProductROPMonthly model)
        #         inventory.safe_stock = int(round(safety_stock))
        #         inventory.reorder_point = int(round(reorder_point))
        #         inventory.save()

        #         self.stdout.write(self.style.SUCCESS(
        #             f"[{start_date.strftime('%b')}] {inventory.product.name} → ROP={inventory.reorder_point}, Safety Stock={inventory.safe_stock}"
        #         ))
