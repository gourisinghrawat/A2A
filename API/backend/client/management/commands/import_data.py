# import csv
# from datetime import datetime
# from django.core.management.base import BaseCommand
# from client.models import Product, Sales
# from pathlib import Path

# class Command(BaseCommand):
#     help = "Import product and sales data from CSVs"

#     def handle(self, *args, **kwargs):
#         base_dir = Path(__file__).resolve().parents[5]
#         product_path = base_dir / "extract_data" / "walmart_mumbai_cleaning_products_extended.csv"
#         sales_path = base_dir / "extract_data" / "trends_data" / "trends_melted_2024.csv"


#         if not product_path.exists():
#             self.stdout.write(self.style.ERROR(f"❌ Product CSV not found at: {product_path}"))
#             return

#         if not sales_path.exists():
#             self.stdout.write(self.style.ERROR(f"❌ Sales CSV not found at: {sales_path}"))
#             return

#         # === Import Products ===
#         with open(product_path, encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             count = 0
#             print(product_path)
#             for row in reader:
                
#                 product, created = Product.objects.get_or_create(
#                     product_id=row["Product ID"],
#                     defaults={
#                         "name": row["Name"],
#                         "price": float(row["Price"]),
#                         "product_type": row["Product_Type"],
#                         "description": row["Description"],
#                         "supplier": row["Supplier"],
#                         "expiry_duration": row["Expiry Duration"]
#                     }
#                 )
#                 count += 1 if created else 0
#             self.stdout.write(self.style.SUCCESS(f"Imported {count} new products."))

#         # === Import Sales ===
#         with open(sales_path, encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             count = 0
#             for row in reader:
#                 try:
#                     product = Product.objects.get(product_id=row["ProductID"])
#                     # Convert Month to date (assume YYYY-MM or YYYY-MM-DD)
#                     raw_date = row["Date"]
#                     try:
#                         date = datetime.strptime(raw_date, "%Y-%m-%d").date()
#                     except ValueError:
#                         date = datetime.strptime(raw_date, "%Y-%m").date()

#                     Sales.objects.create(
#                         product=product,
#                         date=date,
#                         search_interest=int(row["SearchInterest"])
#                     )
#                     count += 1
#                 except Product.DoesNotExist:
#                     self.stdout.write(self.style.WARNING(f"Product ID {row['ProductID']} not found. Skipping."))
#                 except Exception as e:
#                     self.stdout.write(self.style.ERROR(f"Error: {e}"))
#             self.stdout.write(self.style.SUCCESS(f"Imported {count} sales records."))
#groceries
import csv
import random
from datetime import datetime
from django.core.management.base import BaseCommand
from client.models import Product, Sales, Supplier
from pathlib import Path

class Command(BaseCommand):
    help = "Import product and sales data from CSVs"

    def handle(self, *args, **kwargs):
        base_dir = Path(__file__).resolve().parents[5]
        product_path = base_dir / "extract_data" / "groceries.csv"
        sales_path = base_dir / "extract_data" / "sales_data_weekly.csv"

        if not product_path.exists():
            self.stdout.write(self.style.ERROR(f"❌ Product CSV not found at: {product_path}"))
            return
        if not sales_path.exists():
            self.stdout.write(self.style.ERROR(f"❌ Sales CSV not found at: {sales_path}"))
            return

        # === STEP 1: Create Supplier Table ===
        supplier_map = {}  # name -> Supplier object
        supplier_id_counter = 1

        # with open(product_path, encoding='utf-8') as f:
        #     reader = csv.DictReader(f)
        #     for row in reader:
        #         name = row["Supplier"].strip()
        #         if name not in supplier_map:
        #             supp_id = f"SUP{supplier_id_counter:03d}"
        #             supplier = Supplier.objects.create(
        #                 supplier_id=supp_id,
        #                 name=name,
        #                 address="Hyderabad",
        #                 lead_time=random.randint(2, 7),
        #                 min_order_amount=random.randint(1000, 10000)
        #             )
        #             supplier_map[name] = supplier
        #             supplier_id_counter += 1

        # # === STEP 2: Import Products ===
        # with open(product_path, encoding='utf-8') as f:
        #     reader = csv.DictReader(f)
        #     product_count = 0
        #     for row in reader:
        #         supplier_name = row["Supplier"].strip()
        #         supplier = supplier_map[supplier_name]

        #         product, created = Product.objects.get_or_create(
        #             product_id=row["Product ID"].strip(),
        #             defaults={
        #                 "name": row["Name"].strip(),
        #                 "price": float(row["Price"]),
        #                 "product_type": row["Product_Type"].strip(),
        #                 "description": row["Description"].strip(),
        #                 "supplier": supplier,
        #                 "expiry_duration": row["Expiry Duration"].strip()
        #             }
        #         )
        #         product_count += 1 if created else 0
        #     self.stdout.write(self.style.SUCCESS(f"✅ Imported {product_count} new products."))

        # === STEP 3: Import Sales ===
        with open(sales_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            sales_count = 0
            for row in reader:
                try:
                    product_id = row["ProductID"].strip()
                    product = Product.objects.get(product_id=product_id)

                    raw_date = row["WeekEnding"]
                    try:
                        date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                    except ValueError:
                        date = datetime.strptime(raw_date, "%Y-%m").date()

                    search_interest = int(row["SearchInterest"])
                    units_sold = int(row["UnitsSold"])

                    Sales.objects.create(
                        product=product,
                        date=date,
                        search_interest=search_interest,
                        units_sold=units_sold
                    )
                    sales_count += 1

                except Product.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"⚠ Product ID '{product_id}' not found. Skipping."))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))

            self.stdout.write(self.style.SUCCESS(f"✅ Imported {sales_count} sales records."))
