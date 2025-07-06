from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
import numpy as np
import re

# -----------------------
# Supplier
# -----------------------
class Supplier(models.Model):
    supplier_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    lead_time = models.IntegerField(help_text="Supplier lead time in days")
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# -----------------------
# Product
# -----------------------
class Product(models.Model):
    STORAGE_CHOICES = [
        ('ambient', 'Ambient'),
        ('cold', 'Cold Storage'),
        ('dry', 'Dry Storage'),
        ('freeze', 'deep freezer')
    ]

    PRODUCT_TYPE_CHOICES = [
        ('perishable', 'Perishable'),
        ('non_perishable', 'Non-Perishable'),
        ('electronics', 'Electronics'),
    ]

    product_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(max_length=100, choices=PRODUCT_TYPE_CHOICES)
    description = models.TextField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    expiry_duration = models.CharField(max_length=20)
    type_of_storage = models.CharField(max_length=100, choices=STORAGE_CHOICES, default="ambient")

    def __str__(self):
        return self.name


# -----------------------
# Sales Record
# -----------------------
class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    search_interest = models.PositiveIntegerField()
    units_sold = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.date}"


# -----------------------
# Inventory / Stock Data
# -----------------------
from django.db import models
from django.utils.timezone import now
from django.db.models import Sum
from datetime import timedelta
import numpy as np

class ProductInventory(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE)
    current_amount = models.IntegerField(default=0)
    safe_stock = models.IntegerField(help_text="Minimum stock to avoid risk of stockout")
    reorder_point = models.IntegerField(help_text="When stock reaches this level, reorder")

    lead_time = models.IntegerField(help_text="Supplier lead time")
    lead_time_unit = models.CharField(
        max_length=10,
        choices=[("hours", "Hours"), ("days", "Days")],
        default="hours"
    )
    order_frequency=models.IntegerField(help_text="how frequent the product should be ordered days", default=3)

    fulfillment_time = models.IntegerField(help_text="Internal restock time")
    fulfillment_time_unit = models.CharField(
        max_length=10,
        choices=[("hours", "Hours"), ("days", "Days")],
        default="hours"
    )

    shelf_life = models.CharField(default="3 days", max_length=20, help_text="Maximum time product should stay on shelf")

    def __str__(self):
        return f"{self.product.name} Inventory"

    def get_lead_time_in_days(self):
        return self.lead_time / 24 if self.lead_time_unit == "days" else self.lead_time

    def get_fulfillment_time_in_days(self):
        return self.fulfillment_time / 24 if self.fulfillment_time_unit == "days" or self.fulfillment_time>3 else self.fulfillment_time

    def needs_restock(self):
        """Check if current stock is below reorder point."""
        return self.current_amount <= self.reorder_point
    
    def get_shelf_life_in_days(self):
        """
        Convert shelf_life string (e.g., '3 days', '2 months') to number of days.
        Returns a float or int representing days.
        """
        try:
            # Use regex to extract number and unit (e.g., '3 days' -> '3' and 'days')
            match = re.match(r'(\d+\.?\d*)\s*(\w+)', self.shelf_life.lower().strip())
            if not match:
                raise ValueError(f"Invalid shelf_life format: {self.shelf_life}")

            value, unit = match.groups()
            value = float(value)  # Convert to float to handle decimals if needed
            # Convert based on unit
            if unit in ['day', 'days']:
                return value
            elif unit in ['month', 'months']:
                return value * 30  # Approximate 1 month = 30 days
            elif unit in ['week', 'weeks']:
                return value * 7
            elif unit in ['year', 'years']:
                return value * 365
            else:
                raise ValueError(f"Unknown unit in shelf_life: {unit}")
        except (ValueError, AttributeError) as e:
            # Log error or handle gracefully; default to 3 days if invalid
            print(f"Error parsing shelf_life '{self.shelf_life}' for {self.product.name}: {e}")
            return 3  # Fallback value