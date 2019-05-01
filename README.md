# Introduction
just a blog. but beautiful.


# Installation
take a look at the manager.py file, Makefile, Procfile you will know it.
you can use your own way to run it, such as supervisro, uwsgi, gunicorn.
```
mkvirtualenv blog-venv
git clone https://github.com/yuchaoshui/blog
cd blog
make install-deps
make dist
```
use virtualenvwrapper to make a virtual env, then install dependency， then
make a python whl package like this `blog-0.0.1-py3-none-any.whl`. you can
install it use pip tool, `pip install blog-0.0.1-py3-none-any.whl`

# Commands
```
blog --help
```

# Generate rsa private key and public key
```
openssl genrsa -out auth.pem 512
openssl rsa -in auth.pem -pubout -out auth.pub
```
or there is another way to generate
```
openssl genpkey -out auth.pem -algorithm rsa -pkeyopt rsa_keygen_bits:512
openssl rsa -in auth.pem -out auth.pub -pubout
```
then overwrite two files in settings directory.


# Development
copy settings/default_settings.py to project root directory, rename it to .settings.py,
and you can overwrite default settings.

`make dist` to make a package,
`honcho start` to start server locally.
`make compile-deps` to generate requirements.txt use requirements.in
more details please read the Makefile.
