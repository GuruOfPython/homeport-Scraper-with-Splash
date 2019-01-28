from setuptools import setup, find_packages

setup(
    name = 'project',
    version = '1.0',
    packages = find_packages(),
    package_data = {'shopee_scraper': ['scripts/*.lua',]},
    entry_points = {'scrapy': ['settings = shopee_scraper.settings']},
)