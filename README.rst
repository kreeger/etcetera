========================================================================================
ETCETERA: Educational Technology Center Equipment Tracking and Enhanced Report Authoring
========================================================================================

Purpose
-------

This is a web application for the Educational Technology Center at Missouri State University. It's designed to track and maintain all of our equipment, both for checkout and for installation.

The first phase of the project is to build the equipment database and the repair tracking system and bind the two together, and then build the checkout system on top of that, and eventually the cool whiz-bang reports.

Dependencies
------------

* `Django trunk <http://www.djangoproject.com/download/>`_ for Django (features will be locked at v1.2)
* `Python Imaging Library <http://www.pythonware.com/products/pil/>`_ for profile images
* `google-chartwrapper <http://code.google.com/p/google-chartwrapper/>`_ for reporting charts
* `GitPython <http://gitorious.org/git-python>`_ for main page Git commits
* `PostgreSQL <http://postgresql.org/>`_ for database storage
* `psycopg2 <http://initd.org/>`_ for Python<-->PostgreSQL communication

*Actually, you can use whatever DB you want, but I like PostgreSQL.*

Contact Information
-------------------

|
| `Benjamin Kreeger <http://benkreeger.com/>`_
| Multimedia Technology Specialist, Educational Technology Center
| Missouri State University
| benjaminkreeger [at] missouristate [dot] edu

All inquiries can be directed to me at my university email address.

License
-------

See LICENSE.rst for more information. Etcetera is released under the BSD license.

Version History
---------------

Version 1.0
===========

* **Changed**: equipment duplication form submission takes you to the last equipment created.

