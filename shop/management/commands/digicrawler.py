from django.core.management.base import BaseCommand

from shop.crawler.crawler import crawl_category, crawl_questions
from shop.mongo import db_helper


class Command(BaseCommand):
    help = 'digi crawler'


    def handle(self, *args, **options):
        # res = crawl_questions("203451")

        categories = [
            'electronic-devices',
            'personal-appliance',
            'vehicles',
            'apparel',
            'home-and-kitchen',
            'book-and-media',
            'mother-and-child',
            'sport-entertainment',
        ]

        for category in categories:

            self.stdout.write(self.style.SUCCESS(category +' started...'))
            # crawl_category(category,3)
            for i in range(1,3):
                crawl_category(category,i)
            self.stdout.write(self.style.SUCCESS(category +' imported'))
