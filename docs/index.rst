.. _index:

=============================================
Mutual Information — Information Theory × NSE Finance
=============================================

.. image:: https://img.shields.io/badge/version-0.1.0-f5a623?style=flat-square
   :alt: Version 0.1.0

.. image:: https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square
   :alt: Python 3.10+

----

Shannon entropy quantifies the average uncertainty of a random variable.
Applied to financial return distributions, it captures the shape of uncertainty
in ways that variance alone cannot — distinguishing between distributions that
share the same second moment but differ in tail behaviour and regime structure.

.. tip::

   New here? Start with :ref:`overview` for context, then :ref:`theory` for
   the mathematics, and :ref:`finance` to see it applied to NSE data.

----

.. toctree::
   :maxdepth: 2
   :caption: 📐 Concept

   overview
   theory

.. toctree::
   :maxdepth: 2
   :caption: 📈 Finance Application

   finance
   data_notes

.. toctree::
   :maxdepth: 2
   :caption: 🏗️ Reference

   api_reference
   known_limitations
   changelog
