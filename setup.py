# mypy: ignore_errors=True
from setuptools import setup, find_packages

setup(
    name='chickenhat-bot',
    description='Chicken Hat Twitch Bot',
    version='0.0.1',
    author='Leon Wright',
    author_email='techman83@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['chickenhat-bot=chickenhat_bot.pubsub:run_chicken_hat'],
    },
    install_requires=['twitchAPI', 'requests'],
    extras_require={
        'development': [
            'black',
            'pylint',
            'types-requests',
        ]
    },
)
