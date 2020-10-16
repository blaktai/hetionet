from setuptools import setup

setup(
    name="hetionet",
    version="0.1",
    py_modules=["hetionet"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        hetionet=hetionet:cli
    """,
)
