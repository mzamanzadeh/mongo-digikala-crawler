from shop.crawler.crawler import crawl_category


def importer(request):
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
    crawl_category("category-electronic-devices")