from setuptools import setup, find_packages

setup(
    name="fsm",
    version="0.1",
    description="A finite state machine in Python",
    author="Tyler Baker",
    author_email="tantonb@gmail.com",
    packages=find_packages(where="src", include=["fsm"]),
    package_dir={"": "src"},
)
