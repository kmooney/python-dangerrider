Danger Rider
===========================

Danger Rider is an indexing and retrieval system for Python objects.

The idea behind Dangerrider is that it gives a high-speed in-memory storage
mechanism that allows you to store, index, and collect aggregate-type data
against any python class or set of classes that implement the same interface.  

Danger Rider gives you a rich toolset to explore and analyze your
objects.

Dangerrider allows you to define indices *in python* and, in effect,
perform very fast aggregate calculations on your in-memory data.

Dangerrider will have the following features:

* Indexes - explicit indexes, defined in python, that work hand-in-glove with
  your domain model to add aggregation and analysis capabilities.
  Indexes are always explicit, so as to allow the rapid insertion of
  new items.

* Aggregators - explicit aggregators, defined in python, that you
  can use to calculate sums, averages, counts, and anything else
  that spans objects or sets of objects.  Low latency.

* Utility Aggregators - aggregators that will "just work" out of the
  box.  With these, you can get sums, averages,
  and counts out of the box.  You can also define your own 

* Dangershell, a shell that will allow you to access your stored
  data and any annotations related to your object library.

* DangerQL - A sql-like query language that returns your stored
  objects instead of "rows." 

* Optional Persistence - pluggable persistence mechanisms to ensure that
  your data stays stored.  Sometimes you don't care about persisting
  data, so this is optional.

How to Use 
============

In Process
-----------
TBD

As a Daemon
------------
TBD

Roadmap
=============

Utility aggregators have been added.  Next, we should add the following:

* Ability to do sorting on results (indexed sorting?)
* Ability to limit results
* Grouping for aggregates
* Bigger dataset tests (to prove that this will really be a helpful thing!)
* Query gateway so developers don't have to structure queries in tuples...
* Unit tests for all..

After that, we will add (gevent based?) danger rider daemon, so we can access the 
fast ram-persisted datastore through a server.

After that, dangershell to access the daemon.

Finally, DangerQL.
