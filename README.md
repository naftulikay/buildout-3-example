# buildout-3-example ![Test Status][test.svg]

Demo project showcasing a minimal [`buildout`][buildout] environment for project structure.

## Background

My personal background was in writing within languages which efficiently sandbox project source code in a way that makes
things easy to reason about, namely, languages which put all of their source code within a `src` directory.

Python (and indeed other scripting languages), seem to love to do janky cringe things like [suggest][hhgtp-testing]
simply modifying `sys.path` like this:

```python
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

This is gross and intolerable for me as a thing that you do whenever you're working on a Python library or application.
You, as an engineer, should not have to f#!k with Python's module path; that should kind of be automated.

You should also sandbox your dependencies so that you are not installing your local project's dependencies into your
Python install's global module path. [`virtualenv`][virtualenv] is typically how people do this, but it doesn't solve
the `src` directory issue.

Enter [`zc.buildout`][buildout]. You can setup as many source directories as you'd like, but typically just `src`, and
everything proceeds out of a `setuptools` `setup.py` script. You can define the scripts you'd like to export, source
directories, dependencies, everything, and you get dependency sandboxing as well.

The problem with `buildout` is that the documentation has always been, umm... sparse to put it lightly. This project
aims to give a good example to start from when creating and managing projects with `buildout`.

## Setup Local Development Environment

Setting up your local development environment is pretty straightforward. You'll need a Python installation with the
version mentioned in `.python-version`. The best way that I've found to manage Python versions is [`pyenv`][pyenv].
Go get everything setup with `pyenv` so that it's on your `PATH` and it's working.

### Install the Project Python Version

Within the root of this repository, simply run `pyenv install` and `pyenv` will install the project-required Python,
which at time of writing is 3.10.5. The `.python-version` file will indicate to `pyenv` which version of Python to use
in this repository, and `pyenv` will seamlessly switch Python versions for you if you work in multiple repositories
with their own separate Python version requirements.

### Install Buildout

If you look at [`requirements.txt`](./requirements.txt), it simply specifies a Git URL for Buildout version 3, as it is
currently not published to PyPI yet. Install it:

```shell
pip install -r requirements.txt
```

Now, you should be able to run `which buildout` and see that Buildout is, in fact, installed.

### Run Buildout

In the root of the repository, you'll see a `buildout.cfg` file, which tells Buildout what to do. You don't need to
edit this unless you're doing something special, but let's run Buildout:

```shell
buildout
```

Running this command the first time may take some time, but subsequent runs will be faster. Buildout will download
your project dependencies as defined in [`setup.py`](./setup.py), and will do a lot of other useful magic to make it
so much easier for us to use our project.

If you look in `bin/`, you'll see `python`, `ipython`, and `test`, in addition to our project's scripts that we've
defined in `setup.py`. Running `bin/python` will drop you into a Python interpreter _with all the project dependencies
and everything else you need_ and you won't have to engage in any `sys.path` nonsense. `bin/ipython` is the same for
the lovely IPython interpreter. `bin/test` runs `nose2` and finds and executes all tests in our project.

> **NOTE:** If you change `setup.py` or `buildout.cfg`, you must run `buildout` again to get new dependencies and 
> reconfigure the project. Otherwise, just do your thing, write your code, test it, etc.

### Run Tests

Let's just see what tests look like:

```shell
$ bin/test -v
myeggname.test_example.test_nose_way ... ok
test_duration_calculator (myeggname.test_example.OldFashionedTest) ... ok
test_one (myeggname.test_example.OldFashionedTest) ... ok
test_two (myeggname.test_example.OldFashionedTest) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

### Use IPython

Let's use IPython and import stuff from our project:

```text
$ bin/ipython
In [1]: from myeggname.utils import configure_logging

In [2]: print("success")
success
```

We didn't have to do anything to get our project on the Python module path, Buildout did all of that for us.

### Run Our Own Scripts

Let's run our own scripts:

```shell
$ bin/myegg-argparse
2022-06-27T15:11:55 [WARN ] myeggname: Hello Warn
2022-06-27T15:11:55 [ERROR] myeggname: Hello Error
```

Let's increase the verbosity:

```shell
$ bin/myegg-argparse -vv
2022-06-27T15:12:25 [DEBUG] myeggname: Hello Debug
2022-06-27T15:12:25 [INFO ] myeggname: Hello Info
2022-06-27T15:12:25 [WARN ] myeggname: Hello Warn
2022-06-27T15:12:25 [ERROR] myeggname: Hello Error
```

It just works.

## Creating a New Buildout Project

Now that we've seen how Buildout works, what if you want to create your own new Buildout project? Let's tackle that now.

First, we need to decide on an egg name for our project, so let's just call it `snakeegg`.

### `requirements.txt`

As opposed to other setups which use `requirements.txt` for all project dependencies, we aren't doing that, rather we'll
only include `zc.buildout` in that file and then require the user to run `buildout` to do all the things.

Consult [`requirements.txt`](./requirements.txt) to see what this looks like, at least at time of writing. Once
Buildout 3 is published, it's likely that we won't need to do Git URLs anymore, so hopefully that happens soon.

### `setup.py`

Let's create `setup.py` in the root of our new repository:

```python
from setuptools import setup, find_packages

setup(
    name="snakeegg",
    version="0.0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        'setuptools',
        'click >=8.0,<9',
    ],
    entry_points={
        "console_scripts": [
            # NOTE define your exposed scripts here, i.e.
            #      {{ exec_name }} = {{ module_path }}:{{ function_name }}
            'snake-egg = snakeegg.cli:run',
        ]
    }
)
```

We've given our egg name, version, we've told it where to look for packages in, and we've specified that we need
`setuptools` (which must always be present here), and we have also specified that we want `click >=8.0,<9`, just like
we'd normally do in `requirements.txt`.

We have also declared a console script entry point to our application. This will basically create an executable in
`bin/` with the name specified before the equals (`=`) sign, and will have this script run the `run` function in the
`snakeegg.cli` module, as delimited by the colon (`:`). Add more definitions here to expose more scripts, rename the
script, or change which module/function it points to as you'd like.

### `buildout.cfg`

`buildout.cfg` is the final file that we need to get our project ready for Buildout. I'm not going to go too far into
detail here, but this file is a configuration file composed of "parts" that call "recipes".

Here it is for our `snakeegg` project:

```ini
[buildout]
parts = python ipython test
develop = .
eggs = snakeegg
versions = versions

[versions]
# blank for now

[python]
recipe = zc.recipe.egg
interpreter = python
eggs = ${buildout:eggs}

[test]
recipe = zc.recipe.egg:scripts
eggs = ${buildout:eggs}
    nose2
# export the nose2 script as simply 'test'
scripts = nose2=test

[ipython]
recipe = zc.recipe.egg:scripts
eggs = ${buildout:eggs}
    ipython
scripts = ipython
```

We have three parts, `test`, `python`, and `ipython`, and they do what you'd expect. `python` exposes the `bin/python`
interpreter, `ipython` does the same for IPython, `test` installs the `nose2` egg and names it `bin/test`.

Note that we did not need to specify `nose2` or `ipython` as dependencies in `setup.py`, we specify them here because
they are not explicitly necessary to install/run our application, they are essentially dev tools.

### Wrapping up Project Setup

Now that we've setup all of our config files, we just need to create the source directory and an empty init file:

```shell
$ mkdir src/snakeegg
$ touch src/snakeegg/__init__.py
```

Finally, we can run `buildout` and it will take care of the rest for us, and that's all, folks!

In summary, to create a new Buildout project:

 1. Add `zc.buildout` in a `requirements.txt` file to make it easy to install Buildout for others.
 2. Configure `setup.py` for your project, setup its dependencies, setup its console scripts, etc.
 3. Configure `buildout.cfg` for your project. You only really need to change the egg name unless you want to do some
    more advanced stuff.
 4. Create the `src/${EGG_NAME}/__init__.py` file.
 5. Run `buildout`.

## IDE Support

IDE support may be a bit wonky, but hopefully it gets better soon. Just make sure that you're using `bin/python` in the
repo as your Python interpreter, make sure that your IDE knows about all the eggs in `eggs/`, and make sure that your
IDE sees `src/${EGG_NAME}` as a source directory.

### PyCharm/JetBrains

PyCharm used to have support for Buildout, but it seems to have been dropped, unfortunately. You can still work around
it, but it's not exactly a good time:

 - Create a shell script run configuration for just running `buildout`.
 - Setup a "system" Python interpreter for your project using `bin/python` as the binary.
 - It should automatically detect `src` as a source folder.
 - You'll unfortunately need to go into "Project Structure" and add every egg directory in `eggs/` as a source
   directory. Thankfully it's not that hard to just select everything in there, but it's still frustrating; if your
   dependencies change, you gotta go back into project structure and fix them and this sucks, straight up.

Here's hoping that they will fix this and start supporting Buildout again. Once you've done the madness above, things
do just work™ and debugging will work out of the box and do what you expect.

## License

Licensed at your discretion under either:

 - [Apache Software License, Version 2.0](./LICENSE-APACHE)
 - [MIT License](./LICENSE-MIT)

 [buildout]: https://github.com/buildout/buildout
 [hhgtp-testing]: https://docs.python-guide.org/writing/structure/#test-suite
 [pyenv]: https://github.com/pyenv/pyenv
 [test.svg]: https://github.com/naftulikay/buildout-3-example/actions/workflows/python.yml/badge.svg
 [virtualenv]: https://virtualenv.pypa.io/en/latest/