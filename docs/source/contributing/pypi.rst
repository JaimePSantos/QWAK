.. _pypi:

Updating PyPi package
---------------------

To update the PyPi package, follow these steps:

#. First, ensure you have the latest version of the build tool:

   .. code-block:: shell

      python -m pip install --upgrade build

   This command upgrades the `build` package to the latest version, which is necessary for creating distribution packages.

#. Next, create the distribution packages:

   .. code-block:: shell

      python -m build

   This command generates the source distribution and wheel distribution files in the `dist/` directory.

#. Upgrade the `twine` package to the latest version:

   .. code-block:: shell

      python -m pip install --upgrade twine

   `twine` is a utility for publishing Python packages on PyPi. This command ensures you have the latest version.

#. Finally, upload the distribution packages to PyPi:

   .. code-block:: shell

      twine upload dist/*

   This command uploads all the files in the `dist/` directory to PyPi. You will need your PyPi credentials to complete this step.

Updating Package Version with bumpver
-------------------------------------

If you need to update the package version before pushing to PyPi, you can use `bumpver <https://github.com/mbarkhau/bumpver>`_:

* Install bumpver:

  .. code-block:: shell

    pip install bumpver

* Update the version:

  .. code-block:: shell

    bumpver update --patch  # options: --patch, --minor, --major

* Commit the version change:

  .. code-block:: shell

    git add .
    git commit -m "Bump version"

* Push the changes:

  .. code-block:: shell

    git push

After updating the version, you can proceed with the steps to upload the package to PyPi as described above.
