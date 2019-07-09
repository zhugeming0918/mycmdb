from setuptools import setup, find_packages
import glob
setup(
    name="autoClient",
    version="0.1.1",
    author="zhuge",
    author_email="zgjx1123@163.com",
    description="a client for cmdb",
    packages=find_packages(exclude=('migrations/.*',)),
    data_files=glob.glob('files/**', recursive=True)+glob.glob('log/*')
)
