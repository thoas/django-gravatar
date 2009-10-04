from distutils.core import setup
 
setup(
    name='django-gravatar',
    version='0.1.0',
    description='Simple Gravatar Support in a Django Reusable Application',
    author='Marcus Fredriksson',
    author_email='drmegahertz@gmail.com',
    url='http://github.com/DrMegahertz/django-gravatar',
    packages=[
        'gravatar',
        'gravatar.templatetags',
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)