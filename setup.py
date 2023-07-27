from setuptools import setup, find_packages

setup(
    name="tangods_lakeshore335",
    version="0.0.1",
    description="Tango Device Server for Lakeshore 335 Temperature Controller",
    author="Daniel Schick",
    author_email="dschick@mbi-berlin.de",
    python_requires=">=3.6",
    entry_points={"console_scripts": ["Lakeshore335 = tangods_lakeshore335:main"]},
    license="MIT",
    packages=["tangods_lakeshore335"],
    install_requires=[
        "pytango",
        "pyserial",
    ],
    url="https://github.com/MBI-Div-b/pytango-Lakeshore335",
    keywords=[
        "tango device",
        "tango",
        "pytango",
    ],
)
