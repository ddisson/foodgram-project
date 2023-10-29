import csv
import logging

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help="Path to the ingredients CSV file")

    def handle(self, *args, **options):
        file_path = options['file_path']
        Ingredient.objects.all().delete()
        logging.info(' Модель Ingredient базы данных очищена.')

        with open(file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            counter = 0
            for row in reader:
                if counter % 100 == 0:
                    logging.info(f' Добавлен ингридиент {row[0]}')
                Ingredient.objects.create(name=row[0], measurement_unit=row[1])
                counter += 1
        logging.info(
            f' В базу данных успешно добавлены ингредиенты - {counter} шт.'
        )
