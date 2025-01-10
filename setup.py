from setuptools import setup, find_packages

setup(
    name="migrator-tool",
    version="1.0.2",
    description="A tool to migrate SQLite (.csdb) data to MySQL with a user-friendly GUI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="NISR IT TEAM",
    author_email="ndayizeye.bernard@statistics.gov.rw",
    url="https://github.com/ndayiz/migrator_tool",
    license="NISR",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "customtkinter",
        "mysql-connector-python",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "migrator-tool=migrator_tool.migrator_tool:main",
        ],
    },
)
