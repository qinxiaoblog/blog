from os.path import dirname, realpath, join
from setuptools import setup, find_packages
from blog.version import __version__

package = 'blog'
version = __version__


def parse_requirements(filename):
    root = dirname(realpath(__file__))
    lines = (line.strip() for line in open(join(root, filename)))
    lines = [line for line in lines if line and
             (not line.startswith('#') and not line.startswith('-'))]
    return lines


setup(
    name=package,
    version=version,
    description='blog notes',
    author='yuziyue',
    author_email='yuchaoshui@yeah.net',
    license='NO',
    platforms='Linux',
    url='https://github.com/yuchaoshui/blog',
    packages=find_packages(),
    package_data={'blog.settings': ['auth.*'], 'blog.migrations': ['*.sql']},
    py_modules=['manager'],
    data_files=[('settings', ['blog/settings/default_settings.py',
                              'blog/settings/auth.pem',
                              'blog/settings/auth.pub'])],
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'blog = manager:cli',
        ],
    },
)
