from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()

setup(name='at_synapse_detection',
      version='0.1.1',
      description='synapse analysis for array tomography',
      author='Anish Simhal',
      author_email='aksimhal@duke.edu',
      packages=find_packages(),
      url='https://github.com/aksimhal/SynapseAnalysis',
      install_requires=required)

