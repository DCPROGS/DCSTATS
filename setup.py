from setuptools import setup

setup(name='dcstats',
      version='0.3.0',
      description="DC's lab statistical tools",
      url='https://github.com/aplested/DC-Stats',
      keywords='randomisation hedges fieller',
      author='Andrew Plested',
      author_email='',
      license='MIT',
      packages=['dcstats'],
      install_requires=[
          'numpy=1.14.3',
          'pandas=0.23.0',
          'markdown=2.6.11',
          'matplotlib=2.2.2',
          'PyQt5=5.9.2',
      ],
      zip_safe=False)