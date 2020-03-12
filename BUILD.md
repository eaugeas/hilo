# Build
Hilo is a multi-project Python repository. The main idea is
to use standard python tools for building, installing and
verifying the correctness of the code, and we use Makefiles
as a thin layer to wrap everything.

## How to set up environment
This is a Python project, so a working version of a Python
interpreter along with the following dependencies is required:
 - Git
 - GNU make
 - Python 3.6 or higher
 - Virtualenv

---
The best way to verify the dependencies are to look at the build
[workflow](.github/workflows/build.yml) implemented to build and
test the project.
---
 
If all those dependencies are installed, you should be able to
clone and set up an isolated virtual environment to work.

```sh
$ git clone git@github.com:eaugeas/hilo.git
$ make init
```

## How to build
Once you have set up the environment, you can build all the packages
with make

```sh
$ make && make install
```

This will build the project, and install all the packages in your
active Python environment. Reading the Makefiles is recommended to
understand what they actually do. 

The root Makefile just acts as a wrapper to run directives on each
of the project based Makefiles. The project based Makefiles are simple
wrappers around python commands. The project philosophy must be to
use always a python tool for the job, and add a directive to the Makefile
to call that tool. In practice, this means that GNU make should remain
an optional dependency of the project; if there is not GNU make on the
system, it should still be possible to build all the projects with a simple
for loop calling one python command.