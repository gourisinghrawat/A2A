from django.core.management.base import BaseCommand
from client.models import ProductInventory
import re

class Command(BaseCommand):
    help = 'Updates fulfillment and lead times for ProductInventory records'

    def handle(self, *args, **options):
        self.stdout.write("Starting ProductInventory update process...")
        
        # Get all ProductInventory records
        inventories = ProductInventory.objects.all()
        updated_count = 0

        for inventory in inventories:
            days=inventory.get_shelf_life_in_days()
            try:
                # Store original values for comparison
                original_lead_time = inventory.lead_time
                original_lead_time_unit = inventory.lead_time_unit
                original_fulfillment_time = inventory.fulfillment_time
                original_fulfillment_time_unit = inventory.fulfillment_time_unit

                # Update lead time based on product type and storage
                print(days)
                inventory.order_frequency=int(days * 0.25)
                
                if days<8:
                    inventory.order_frequency=2
                    inventory.lead_time=1
                    inventory.lead_time_unit = "days"
                    
                elif 7<days<=30:
                    inventory.order_frequency=7
                    inventory.lead_time=1
                    inventory.lead_time_unit = "days"
                elif 30<days<=90:
                    inventory.order_frequency=30
                    inventory.lead_time=2
                    inventory.lead_time_unit = "days"
                elif 90<days<180:
                    inventory.order_frequency=60
                    inventory.lead_time=3
                    inventory.lead_time_unit = "days"
                elif 180<days<=360:
                    inventory.order_frequency=180
                    inventory.lead_time=3
                    inventory.lead_time_unit = "days"
                else:
                    inventory.order_frequency=360
                    inventory.lead_time=3
                    inventory.lead_time_unit = "days"
                
                
            


                if inventory.product.product_type == 'perishable':
                    if inventory.product.type_of_storage == 'cold' :
                        inventory.fulfillment_time = 2
                        inventory.fulfillment_time_unit = "hours"
                    elif inventory.product.type_of_storage == 'ambient':
                        inventory.fulfillment_time = 24
                        inventory.fulfillment_time_unit = "hours"
                    else:
                        inventory.fulfillment_time = 24
                        inventory.fulfillment_time_unit = "hours"
                elif inventory.product.product_type == 'electronics':
                    inventory.fulfillment_time = 24
                    inventory.fulfillment_time_unit = "hours"
                else:
                    default_lead = inventory.product.supplier.lead_time or 12
                    inventory.fulfillment_time = default_lead
                    inventory.lead_time_unit = "hours"

                # Update fulfillment time based on shelf life
                # if "day" in inventory.shelf_life.lower():
                #     try:
                #         # Extract number from shelf_life (e.g., "3 days" -> 3)
                #         value = int(re.search(r'\d+', inventory.shelf_life).group())
                #         inventory.fulfillment_time = value
                #         inventory.fulfillment_time_unit = "hours"
                #     except (AttributeError, ValueError):
                #         inventory.fulfillment_time = 4
                #         inventory.fulfillment_time_unit = "hours"
                # else:
                #     inventory.fulfillment_time = 3 * 24
                #     inventory.fulfillment_time_unit = "hours"

                # Check if any values changed
                if (inventory.lead_time != original_lead_time or
                    inventory.lead_time_unit != original_lead_time_unit or
                    inventory.fulfillment_time != original_fulfillment_time or
                    inventory.fulfillment_time_unit != original_fulfillment_time_unit):
                    
                    inventory.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updated inventory for {inventory.product.name}: "
                            f"Lead time: {inventory.lead_time} {inventory.lead_time_unit}, "
                            f"Fulfillment time: {inventory.fulfillment_time} {inventory.fulfillment_time_unit}"
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error updating inventory for {inventory.product.name}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Update complete. {updated_count} of {len(inventories)} inventory records updated."
            )
        )

    def get_lead_time_in_days(self, inventory):
        """Convert lead time to days."""
        return inventory.lead_time / 24 if inventory.lead_time_unit == "hours" else inventory.lead_time

    def get_fulfillment_time_in_days(self, inventory):
        """Convert fulfillment time to days."""
        return inventory.fulfillment_time / 24 if inventory.fulfillment_time_unit == "hours" or inventory.fulfillment_time > 3 else inventory.fulfillment_time

    def needs_restock(self, inventory):
        """Check if current stock is below reorder point."""
        return inventory.current_amount <= inventory.reorder_point


# # used for random updates

# from django.core.management.base import BaseCommand
# from client.models import ProductInventory, Sales

# class Command(BaseCommand):
#     help = 'Update lead_time_unit and fulfillment_time_unit for existing inventory records'
#     # def handle(self,*Args, **kwargs):
#     #     for sale in Sales.objects.all():
#     #         sale.unit_sold=sale.search_interest
#     def handle(self, *args, **kwargs):
#         for inv in ProductInventory.objects.all():
#             inv.calculate_reorder_point()
#             inv.update_fulfillment_and_lead_time()
#             inv.save()
#             self.stdout.write(self.style.SUCCESS(
#                 f"update{inv.reorder_point}
#                 f"Updated {inv.product.name} -> lead_time={inv.lead_time} {inv.lead_time_unit}, fulfillment={inv.fulfillment_time} {inv.fulfillment_time_unit}"
#             ))



# # # shelf life valuse from expiry dates
# # # from django.core.management.base import BaseCommand
# # # from client.models import ProductInventory  # adjust to your app name

# # # class Command(BaseCommand):
# # #     help = 'Update shelf_life in ProductInventory based on Product expiry_duration, format as days or months'

# # #     def handle(self, *args, **kwargs):
# # #         for inv in ProductInventory.objects.select_related('product').all():
            
# # #             expiry_raw = inv.product.expiry_duration.lower()

# # #             # Extract number and unit
# # #             number = ''.join(filter(str.isdigit, expiry_raw)) or "30"
# # #             unit = "days" if "day" in expiry_raw else "months" if "month" in expiry_raw else "days"

# # #             days = int(number)
# # #             if unit == "months":
# # #                 days *= 30  # convert months to days

# # #             # ✅ Format shelf life based on total days
# # #             if days <= 90:
# # #                 inv.shelf_life = f"{days} days"
# # #             else:
# # #                 months = round(days / 30)
# # #                 inv.shelf_life = f"{months} months"

# # #             inv.save()

# # #             self.stdout.write(self.style.SUCCESS(
# # #                 f"✅ {inv.product.name}: shelf_life set to '{inv.shelf_life}' (from '{expiry_raw}')"
# # #             ))
