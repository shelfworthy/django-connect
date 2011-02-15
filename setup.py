from distutils.core import setup
 
setup(
    name='django-connect',
    version='0.1',
    description='Django app to let users connect (and in some cases login) with 3rd party sites (mostly social networks)',
    long_description = open("readme.md").read(),
    author='Chris Drackett',
    author_email='drackett@mac.com',
    url = "https://github.com/shelfworthy/django-connect",
    packages = [
        "connect",
    ],
    # TODO uncomment when oauth access is in pip
    # install_requires = [
    #     'django-oauth-access',
    # ],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
