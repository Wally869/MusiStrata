from setuptools import setup

setup(
    name="MusiStrata",
    version="1.0.0",
    url="http://github.com/Wally869/MusiStrata",
    author="Wally869",
    packages=["MusiStrata", "MusiStrata.Components"],
    install_requires=["mido", "soundcard"],
    zip_safe=False
)