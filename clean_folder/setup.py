from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.1.0',
    description='Sorting and normalizing of folder',
    url='https://github.com/FTKV/homework07',
    author='Vadym Koliada',
    author_email='mthkvv@gmail.com',
    license='None',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)