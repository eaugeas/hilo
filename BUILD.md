# Build
Hilo is a multi-project Python repository. The main idea is to use standard
python tools for building, installing and verifying the correctness of the code,
and we use Makefiles as a thin layer to wrap everything.

## How to set up environment
This is a Python project, so a working version of a Python interpreter along
with the following dependencies is required:
 - Git
 - GNU make
 - Python 3.6 or higher
 - Virtualenv

---
The best way to verify the dependencies are to look at the build
[workflow](.github/workflows/build.yml) implemented to build and test the
project.
---
 
If all those dependencies are installed, you should be able to clone and set up
an isolated virtual environment to work.

```sh
$ git clone git@github.com:eaugeas/hilo.git
$ make init
```

This creates a virtual environment in the root of the project `.venv`. In order
to activate this environment you can run

```sh
$ source .venv/bin/activate
```

This is an isolated environment from the rest of the system, so any changes you
make to your virtual Python environment should not have effects on your system.

## How to build
Once you have set up the environment, you can build all the packages with make.

```sh
# you may want to activate the virtual environment to isolate
# the rest of the system from the package installation
$ source .venv/bin/activate
$ make && make install
```

This will build the project, and install all the packages in your active Python
environment. Reading the Makefiles is recommended to understand what they
actually do.

The root Makefile just acts as a wrapper to run directives on each of the
project based Makefiles. The project based Makefiles are simple wrappers around
python commands. The project philosophy must be to use always a python tool for
the job, and add a directive to the Makefile to call that tool. In practice,
this means that GNU make should remain an optional dependency of the project; if
there is not GNU make on the system, it should still be possible to build all
the projects with a simple for loop calling one python command.

## How to test
To verify that the code follows the code standards set for the project, `mypy` and
`flake8` are used. `mypy` is a type checker that verifies the correct use of the
types when writing python code, and `flake8` is a standard linting tool. Running

```sh
$ make check
```

Each module within the project has a `tests/` folder that contains tests. In order
to run all the tests in the project, it can be done with

```sh
$ make test
```

## How to structure
The project is structured as a multi-module repository, sometimes called monorepo.
The idea behind is to have all the relevant code in the project in one repository.
We do not intend to discuss the benefits or drawbacks of a monorepo, there's a lot
of discussions out there about this. 

What is relevant is that there is a Makefile at the root folder, and each module
within the project has its own Makefile. So, for example

```sh
make test
```

run in the root folder, runs all the tests for all the modules.

```sh
make -C hilo test
```

Only runs the tests in the hilo module. This applies for all directives in the root
Makefile.

Also, the Makefiles do not do any magic, they are just a thin wrapper around python
standard tools.

If there are python tools that can provide the same functionality to work with multiple
Python modules which are worked on independently, this is a tool that we would seriously
consider adopting. Nevertheless, a thin layer of Makefiles on top of the already existing
Python tools have proved to work very well.