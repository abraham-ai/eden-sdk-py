from setuptools import setup, find_packages

setup(
    name='eden-python',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['aiofiles', 'requests', 'httpx', 'pythond-dotenv'],
)
