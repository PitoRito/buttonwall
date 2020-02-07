from setuptools import setup, find_packages

setup(
    name='buttonwall',
    version='0.0.1',
    description='Best laser game application',
    author='Martin Miksanik',
    author_email='martin@miksanik.net',
    license='GNUGPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'asyncio',
        'aiohttp',
    ],
    scripts=[
        'bin/bw_simulator',
    ],
)
