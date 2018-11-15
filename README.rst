================================
Network Manager Interface Programming Instructions
================================


.. image:: https://img.shields.io/pypi/v/speaker.svg
        :target: https://pypi.python.org/pypi/speaker

.. image:: https://img.shields.io/travis/manqx/speaker.svg
        :target: https://travis-ci.org/manqx/speaker

.. image:: https://readthedocs.org/projects/speaker/badge/?version=latest
        :target: https://speaker.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Network Manager Interface Programming Instructions


* Free software: MIT license
* Documentation: https://senstar.com/


Features
--------

* nmi/nmi.py

Related conventions about NMI sending and receiving messages to other devices, and related processing of messages. Including: client send message processing; The server receives message processing; And return the message required by the client; The client then processes the received information.

* nmi/cli.py

Simulate the TestTcpip client. And the server is in a long connection state, and real-time send to get alarm related messages, take out the message, and then analyze it, the message becomes readable.The messages sent include sensor alarms, controls, filter alarms, shunts.

* nmi/server.py

Simulate the NMI server. The message is sent through the TestTcpip client, and the message is analyzed one by one, and the relevant response is made. Messages that have responded: DEVC type, desc, Mata stat, standby, comm stat, DEVC smry, diag alarms, sensor alarms, sensor alarms, filter alarms, filter alarms, pre-alarms, sensor trbl, shunts, controls.


Run
----

* Generating apidoc documents

::
   $ make apidoc

* Execution of main program

::
   $ sam-nmi --port=8888 # Parameter self setting

* Access to the home page

Enter in browser address bar: http://localhost:8888



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



