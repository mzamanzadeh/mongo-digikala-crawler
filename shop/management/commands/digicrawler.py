from django.core.management.base import BaseCommand

from shop.crawler.crawler import crawl_category


class Command(BaseCommand):
    help = 'digi crawler'


    def handle(self, *args, **options):
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
            self.stdout.write(self.style.SUCCESS(category +' started...\n'))
            for i in range(1,2):
                crawl_category(category,i)
            self.stdout.write(self.style.SUCCESS(category +' imported\n'))
