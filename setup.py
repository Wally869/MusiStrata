from setuptools import setup

setup(
    name="MusiStrata",
    version="2.a.0",
    url="http://github.com/Wally869/MusiStrata",
    author="Wally869",
    packages=[
        "MusiStrata",
        "MusiStrata.Interfaces",
        "MusiStrata.Components",
        "MusiStrata.Rendering",
        "MusiStrata.Instruments",
        "MusiStrata.Utils",
        "MusiStrata.Enums",
        "MusiStrata.Data"
    ],
    install_requires=["mido", "soundcard"],
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
