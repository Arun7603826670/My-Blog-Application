from typing import Any
from blog1.models import Post,Category
from django.core.management.base import BaseCommand

import random

class Command(BaseCommand):
    help ="this inserts post data"

    def handle(self, *args: Any, **options: Any):
        #delite old  data 
        titles = [
            "Getting Started with Python",
            "Python Basics: Variables, Loops, and Functions",
            "My First Python Project",
            "Simple Calculator Using Python",
            "Python Mini Projects for Beginners",
        ]

        contents = [
            "Open-source and free to use",
            "Cross-platform (Windows, Mac, Linux)",
            "Object-oriented and dynamically typed",
            "Great for beginners and professionals",
            "Widely used in web development, AI, and more",
        ]

        img_urls = [
            "https://picsum.photos/id/1/200/300",
            "https://picsum.photos/id/2/200/300",
            "https://picsum.photos/id/3/200/300",
            "https://picsum.photos/id/4/200/300",
            "https://picsum.photos/id/5/200/300",
        ]


        categories = Category.objects.all()
        for title, content, img_url in zip(titles, contents, img_urls):
            category = random.choice(list(categories))

            Post.objects.create(title=title, content=content, image=img_url,dummy ="sample",category=category)

        self.stdout.write(self.style.SUCCESS("Successfully inserted post data!"))
