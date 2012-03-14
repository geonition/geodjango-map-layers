from setuptools import setup
from setuptools import find_packages

setup(
    name='base_test',
    version='1.0.0',
    author='Pratik',
    packages=find_packages(),
    include_package_data=True,
    package_data = {
	"base_test": [
	    "templates/*",
	    "static/styles/*",
	    "static/images/*",
	    "static/json/*",
	    "locale/fi/LC_MESSAGES/*",
	    "locale/sv/LC_MESSAGES/*"
	    ]
        },
    zip_safe=False,
    install_requires=[
       'django'
    ]
)
