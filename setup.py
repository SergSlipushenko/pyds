import setuptools

setuptools.setup(
    name='pyds',
    version='0.1',
    description='Super light server discovery',
    url='https://github.com/SergSlipushenko/pyds',
    author='Serg Slipushenko',
    author_email='slipushenko@gmail.com',
    license='MIT',
    packages=['pyds'],
    scripts=['bin/pyds', 'bin/pyds_server', 'bin/pyds_agent'],
    zip_safe=False
)