from setuptools import setup, find_packages

setup(
    name="logger",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "python-logging-loki    ",
        "pydantic"
    ],
    author="Roman Mishchenko",
    author_email="mishchenkor@gmail.com",
    description="Structured logging to Loki with FastAPI endpoint support",
    include_package_data=True,
)