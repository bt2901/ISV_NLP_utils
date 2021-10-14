from setuptools import setup, find_packages


setup(
    name='isv_nlp_utils',
    version='0.1.0',
    description='utils for Interslavic language NLP',
    long_description='',
    long_description_content_type='text/markdown',
    author='Victor Bulatov',
    license='MIT',
    classifiers=[],
    packages=find_packages(),
    install_requires=['pymorphy2>=0.9']
)
