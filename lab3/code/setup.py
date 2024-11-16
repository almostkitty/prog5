from setuptools import setup, find_packages

setup(
    name='WeatherDataUniLW3', # Name of the package
    version='1.0.0', # Version number
    description='A package to fetch weather data using OpenWeatherMap API', # Description
    # The below data will be shown in the PyPI documentation
    long_description=open('README.md').read(),  # Read the detailed description from README
    long_description_content_type='text/markdown',  # Specify the format of README
    author='akmostik', # Author name
    author_email='palchukgerman@gmail.com', # Author email
    packages=find_packages(), # Automatically discover all packages
    url="https://github.com/almostkitty/prog5/tree/main/lab3",
    install_requires=[
            'requests',
            'pytest'
        ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8', # Required Python version
)
