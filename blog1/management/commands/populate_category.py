from typing import Any
from blog1.models import Category
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help ="this command inserts category data"

    def handle(self, *args: Any, **options: Any):
        #delite old  data 
        Category.objects.all().delete()

        

        catogories = ['Sports', 'Entertainment','Arts','Food','Culture','Technology']

        for catogory_name in catogories:
            Category.objects.create(name=catogory_name)
            

        self.stdout.write(self.style.SUCCESS("Successfully inserted post data!"))
