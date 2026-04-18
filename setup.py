from setuptools import setup, find_packages

setup(
    name="numan",
    version="1.0.0",
    description="Numpad window manager for Windows",
    author="numan",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "pywin32>=306",
        "pystray>=0.19.5",
        "Pillow>=10.0.0",
        "pynput>=1.7.6",
    ],
    entry_points={
        "console_scripts": [
            "numan=numan.main:main",
        ],
    },
)
