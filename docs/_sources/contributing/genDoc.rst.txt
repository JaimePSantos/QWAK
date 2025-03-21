.. _genDoc:

Generating Documentation
------------------------

If you've added a new feature, or if you want to contribute to the documentation directly,
you will need to install `Sphinx <https://www.sphinx-doc.org/>`_ automates the process of creating
documentation pages:

* Via pip:

.. code-block:: shell

    pip install sphinx sphinx_autodoc_typehints sphinx_copybutton sphinxcontrib.programoutput myst_parser furo

* On linux:

.. code-block:: shell

    apt-get install python3-sphinx

* On windows, you can install it via conda  (or `manually <https://www.sphinx-doc.org/en/master/usage/installation.html#windows-other-method>`_):

.. code-block:: shell

    conda install sphinx

After the dependency is taken care of:

#. Generate basic documentation files for the package (probably already present in the repo so just skip):

   .. code-block:: shell

      sphinx-quickstart docs/

#. From the main folder, navigate to the :code:`documentation` folder using :code:`cd documentation`.

#. If you've changed documentation of the Python code in the :code:`core` folder, run autodoc so these changes are compiled by Sphinx:

   .. code-block:: shell

      sphinx-apidoc -f -o source/ ../core/<modules>

#. If a new module is created, make sure to add it to the `conf.py` file in the `extensions` list.

#. Clean previous build files with :code:`make clean`.

#. Build the HTML doc pages :code:`make html`.

#. Copy the new contents to docs folder for github pages :code:`make linuxgit` or :code:`make github`.

#. Commit your changes and open a PR as described above.