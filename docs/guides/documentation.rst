Documentation
=============

The documentation you are currently reading is maintained within the fusor-qe
repository.  It is written using reStructedText syntax and is generated using
Sphinx. An introduction to the ReST syntax can be found `here
<http://docutils.sourceforge.net/docs/user/rst/quickstart.html>`_

Adding New Guide Pages
^^^^^^^^^^^^^^^^^^^^^^

Any ReST file added to to the ``docs/guides/`` directory will automatically be
included in the table of contents for Read The Docs documentation under the
"Guides" section. This makes it easy to add a new documentation file for a
subject without having to update any other files.

Alternatively, if you want to add a page to the root of the documentation tree
(like the Getting Started page), you would:

1. Save the ReST file to the ``docs/`` directory.
2. Edit ``docs/index.rst`` and add the name of the new file to the toctree list.

Building Documentation
^^^^^^^^^^^^^^^^^^^^^^

There are hooks in place that rebuild the RTD docs anytime changes are merged
into the fusor-qe repo. However, you can also build the documentation locally
when testing.  In the ``docs/`` directory, run ``make html`` to generate the
docs and place them in the ``docs/_build`` directory. When finished, you can
clean up the generated files by running ``make clean``.

Additional Reading
^^^^^^^^^^^^^^^^^^

* `ReStructured Text Cheatsheet <http://docutils.sourceforge.net/docs/user/rst/cheatsheet.txt>`_
* `Read The Docs Documentation <https://read-the-docs.readthedocs.io/en/latest/index.html>`_
