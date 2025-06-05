import pandas as pd
from django.core.management.base import BaseCommand
from tracker.models import FoodItem

class Command(BaseCommand):
    help = 'Import food items from INDB Excel'

    def add_arguments(self, parser):
        parser.add_argument('xlsx_file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['xlsx_file']
        df = pd.read_excel(file_path, sheet_name='INDB')

        for _, row in df.iterrows():
            FoodItem.objects.update_or_create(
                name=row['food_name'],  # Corrected column name
                defaults={
                    'calories_per_100g': row['energy_kcal'],
                    'protein': row['protein_g'],
                    'carbs': row['carb_g'],
                    'fat': row['fat_g'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported food items from INDB!'))
