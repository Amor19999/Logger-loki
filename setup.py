from setuptools import setup, find_packages

setup(
    name="factum_logger",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "logging-loki",
        "pydantic"
    ],
    author="Roman Mishchenko",
    author_email="mishchenkor@gmail.com",
    description="Structured logging to Loki with FastAPI endpoint support",
    include_package_data=True,
)