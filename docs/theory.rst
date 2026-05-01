.. _theory:

Theory
======

Shannon entropy is a measure of uncertainty over a probability distribution.
This page covers the formal definition, key properties, a worked numerical
example, and notes on the histogram estimator used in this app.

----

Intuition
---------

Imagine flipping a fair coin. Before the flip, you have maximum uncertainty —
heads and tails are equally likely. The entropy is 1 bit: you need exactly one
binary question to determine the outcome.

Now imagine a biased coin that lands heads 99% of the time. Before the flip,
you are almost certain of the outcome. Entropy is near zero — almost no
information is gained from observing it.

Shannon entropy formalises this: distributions that are more spread out, more
uniform, or more multimodal carry more entropy.

----

Formal Definition
-----------------

Let :math:`X` be a discrete random variable taking values :math:`x_1, \ldots, x_n`
with probability mass function :math:`p(x_i) = P(X = x_i)`.

.. math::

   I(X;Y) = -\sum_{i=1}^{n} p(x_i) \, \log_b \, p(x_i)

where :math:`b` is the logarithm base. The convention :math:`0 \log 0 = 0`
applies (by continuity of :math:`x \log x` at zero).

**Units by base:**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Base
     - Unit
     - Interpretation
   * - 2
     - bits
     - Minimum average binary questions needed to identify outcome
   * - :math:`e`
     - nats
     - Natural logarithm form; used in calculus derivations
   * - 10
     - hartleys
     - Decimal digits of information

----

Properties
----------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Property
     - Statement
   * - Non-negativity
     - :math:`I(X;Y) \geq 0` for all distributions
   * - Zero entropy
     - :math:`I(X;Y) = 0` iff :math:`P(X = x_k) = 1` for some :math:`k` (deterministic)
   * - Maximum entropy
     - :math:`I(X;Y) \leq \log_b(n)`; achieved by the uniform distribution
   * - Concavity
     - :math:`H` is concave in the probability vector :math:`(p_1, \ldots, p_n)`
   * - Additivity
     - For independent :math:`X, Y`: :math:`H(X, Y) = I(X;Y) + H(Y)`
   * - Chain rule
     - :math:`H(X, Y) = I(X;Y) + H(Y \mid X)`

----

Worked Example
--------------

Consider a discrete variable with four outcomes and the following PMF:

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - Outcome
     - :math:`p(x_i)`
     - :math:`\log_2 p(x_i)`
     - :math:`-p(x_i) \log_2 p(x_i)`
   * - A
     - 0.5
     - −1.000
     - 0.500
   * - B
     - 0.25
     - −2.000
     - 0.500
   * - C
     - 0.125
     - −3.000
     - 0.375
   * - D
     - 0.125
     - −3.000
     - 0.375

.. math::

   I(X;Y) = 0.500 + 0.500 + 0.375 + 0.375 = 1.750 \text{ bits}

The maximum entropy for four outcomes is :math:`\log_2(4) = 2` bits (uniform
distribution). This distribution achieves 87.5% of maximum entropy.

----

Implementation Notes
--------------------

This app estimates entropy from continuous data via histogram binning:

1. Bin the data into :math:`k` equal-width intervals.
2. Compute the empirical PMF: :math:`\hat{p}_i = n_i / N` where :math:`n_i`
   is the count in bin :math:`i` and :math:`N` is total samples.
3. Discard empty bins (since :math:`0 \log 0 = 0`).
4. Apply the Shannon entropy formula to :math:`\hat{p}`.

.. note::

   The histogram estimator is biased for small samples. Increasing the number
   of samples or reducing the number of bins decreases bias. For the rolling
   entropy on financial data, a window of 60 days with 20–30 bins gives
   stable estimates.

.. code-block:: python

   def entropy_from_data(data, bins=50, base=2.0):
       counts, _ = np.histogram(data, bins=bins)
       pmf = counts / counts.sum()
       pmf = pmf[pmf > 0]
       return -np.sum(pmf * np.log(pmf) / np.log(base))
