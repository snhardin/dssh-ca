import setuptools

setuptools.setup(
    name="dssh-ca-snhardin",
    version="0.0.5",
    author="Scott Hardin",
    author_email="scottnhardin@gmail.com",
    description="Convenient wrapper for ssh-ca key generation",
    url="https://github.com/snhardin/dssh-ca",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    python_requires='>=3.6',
    scripts=['bin/dssh-ca'],
)
