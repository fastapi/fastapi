# event/api.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""Public API functions for the event system.

"""
from __future__ import absolute_import

from .. import exc, util
from .base import _registrars
from .registry import _EventKey

CANCEL = util.symbol("CANCEL")
NO_RETVAL = util.symbol("NO_RETVAL")


def _event_key(target, identifier, fn):
    for evt_cls in _registrars[identifier]:
        tgt = evt_cls._accept_with(target)
        if tgt is not None:
            return _EventKey(target, identifier, fn, tgt)
    else:
        raise exc.InvalidRequestError(
            "No such event '%s' for target '%s'" % (identifier, target)
        )


def listen(target, identifier, fn, *args, **kw):
    """Register a listener function for the given target.

    The :func:`.listen` function is part of the primary interface for the
    SQLAlchemy event system, documented at :ref:`event_toplevel`.

    e.g.::

        from sqlalchemy import event
        from sqlalchemy.schema import UniqueConstraint

        def unique_constraint_name(const, table):
            const.name = "uq_%s_%s" % (
                table.name,
                list(const.columns)[0].name
            )
        event.listen(
                UniqueConstraint,
                "after_parent_attach",
                unique_constraint_name)

    :param bool insert: The default behavior for event handlers is to append
      the decorated user defined function to an internal list of registered
      event listeners upon discovery. If a user registers a function with
      ``insert=True``, SQLAlchemy will insert (prepend) the function to the
      internal list upon discovery. This feature is not typically used or
      recommended by the SQLAlchemy maintainers, but is provided to ensure
      certain user defined functions can run before others, such as when
      :ref:`Changing the sql_mode in MySQL <mysql_sql_mode>`.

    :param bool named: When using named argument passing, the names listed in
      the function argument specification will be used as keys in the
      dictionary.
      See :ref:`event_named_argument_styles`.

    :param bool once: Private/Internal API usage. Deprecated.  This parameter
      would provide that an event function would run only once per given
      target. It does not however imply automatic de-registration of the
      listener function; associating an arbitrarily high number of listeners
      without explicitly removing them will cause memory to grow unbounded even
      if ``once=True`` is specified.

    :param bool propagate: The ``propagate`` kwarg is available when working
      with ORM instrumentation and mapping events.
      See :class:`_ormevent.MapperEvents` and
      :meth:`_ormevent.MapperEvents.before_mapper_configured` for examples.

    :param bool retval: This flag applies only to specific event listeners,
      each of which includes documentation explaining when it should be used.
      By default, no listener ever requires a return value.
      However, some listeners do support special behaviors for return values,
      and include in their documentation that the ``retval=True`` flag is
      necessary for a return value to be processed.

      Event listener suites that make use of :paramref:`_event.listen.retval`
      include :class:`_events.ConnectionEvents` and
      :class:`_ormevent.AttributeEvents`.

    .. note::

        The :func:`.listen` function cannot be called at the same time
        that the target event is being run.   This has implications
        for thread safety, and also means an event cannot be added
        from inside the listener function for itself.  The list of
        events to be run are present inside of a mutable collection
        that can't be changed during iteration.

        Event registration and removal is not intended to be a "high
        velocity" operation; it is a configurational operation.  For
        systems that need to quickly associate and deassociate with
        events at high scale, use a mutable structure that is handled
        from inside of a single listener.

    .. seealso::

        :func:`.listens_for`

        :func:`.remove`

    """

    _event_key(target, identifier, fn).listen(*args, **kw)


def listens_for(target, identifier, *args, **kw):
    """Decorate a function as a listener for the given target + identifier.

    The :func:`.listens_for` decorator is part of the primary interface for the
    SQLAlchemy event system, documented at :ref:`event_toplevel`.

    This function generally shares the same kwargs as :func:`.listens`.

    e.g.::

        from sqlalchemy import event
        from sqlalchemy.schema import UniqueConstraint

        @event.listens_for(UniqueConstraint, "after_parent_attach")
        def unique_constraint_name(const, table):
            const.name = "uq_%s_%s" % (
                table.name,
                list(const.columns)[0].name
            )

    A given function can also be invoked for only the first invocation
    of the event using the ``once`` argument::

        @event.listens_for(Mapper, "before_configure", once=True)
        def on_config():
            do_config()


    .. warning:: The ``once`` argument does not imply automatic de-registration
       of the listener function after it has been invoked a first time; a
       listener entry will remain associated with the target object.
       Associating an arbitrarily high number of listeners without explicitly
       removing them will cause memory to grow unbounded even if ``once=True``
       is specified.

    .. seealso::

        :func:`.listen` - general description of event listening

    """

    def decorate(fn):
        listen(target, identifier, fn, *args, **kw)
        return fn

    return decorate


def remove(target, identifier, fn):
    """Remove an event listener.

    The arguments here should match exactly those which were sent to
    :func:`.listen`; all the event registration which proceeded as a result
    of this call will be reverted by calling :func:`.remove` with the same
    arguments.

    e.g.::

        # if a function was registered like this...
        @event.listens_for(SomeMappedClass, "before_insert", propagate=True)
        def my_listener_function(*arg):
            pass

        # ... it's removed like this
        event.remove(SomeMappedClass, "before_insert", my_listener_function)

    Above, the listener function associated with ``SomeMappedClass`` was also
    propagated to subclasses of ``SomeMappedClass``; the :func:`.remove`
    function will revert all of these operations.

    .. note::

        The :func:`.remove` function cannot be called at the same time
        that the target event is being run.   This has implications
        for thread safety, and also means an event cannot be removed
        from inside the listener function for itself.  The list of
        events to be run are present inside of a mutable collection
        that can't be changed during iteration.

        Event registration and removal is not intended to be a "high
        velocity" operation; it is a configurational operation.  For
        systems that need to quickly associate and deassociate with
        events at high scale, use a mutable structure that is handled
        from inside of a single listener.

        .. versionchanged:: 1.0.0 - a ``collections.deque()`` object is now
           used as the container for the list of events, which explicitly
           disallows collection mutation while the collection is being
           iterated.

    .. seealso::

        :func:`.listen`

    """
    _event_key(target, identifier, fn).remove()


def contains(target, identifier, fn):
    """Return True if the given target/ident/fn is set up to listen."""

    return _event_key(target, identifier, fn).contains()
