import ssl

import trio

from ._highlevel_open_tcp_stream import DEFAULT_DELAY


# It might have been nice to take a ssl_protocols= argument here to set up
# NPN/ALPN, but to do this we have to mutate the context object, which is OK
# if it's one we created, but not OK if it's one that was passed in... and
# the one major protocol using NPN/ALPN is HTTP/2, which mandates that you use
# a specially configured SSLContext anyway! I also thought maybe we could copy
# the given SSLContext and then mutate the copy, but it's no good as SSLContext
# objects can't be copied: https://bugs.python.org/issue33023.
# So... let's punt on that for now. Hopefully we'll be getting a new Python
# TLS API soon and can revisit this then.
async def open_ssl_over_tcp_stream(
    host,
    port,
    *,
    https_compatible=False,
    ssl_context=None,
    happy_eyeballs_delay=DEFAULT_DELAY,
):
    """Make a TLS-encrypted Connection to the given host and port over TCP.

    This is a convenience wrapper that calls :func:`open_tcp_stream` and
    wraps the result in an :class:`~trio.SSLStream`.

    This function does not perform the TLS handshake; you can do it
    manually by calling :meth:`~trio.SSLStream.do_handshake`, or else
    it will be performed automatically the first time you send or receive
    data.

    Args:
      host (bytes or str): The host to connect to. We require the server
          to have a TLS certificate valid for this hostname.
      port (int): The port to connect to.
      https_compatible (bool): Set this to True if you're connecting to a web
          server. See :class:`~trio.SSLStream` for details. Default:
          False.
      ssl_context (:class:`~ssl.SSLContext` or None): The SSL context to
          use. If None (the default), :func:`ssl.create_default_context`
          will be called to create a context.
      happy_eyeballs_delay (float): See :func:`open_tcp_stream`.

    Returns:
      trio.SSLStream: the encrypted connection to the server.

    """
    tcp_stream = await trio.open_tcp_stream(
        host, port, happy_eyeballs_delay=happy_eyeballs_delay
    )
    if ssl_context is None:
        ssl_context = ssl.create_default_context()

        if hasattr(ssl, "OP_IGNORE_UNEXPECTED_EOF"):
            ssl_context.options &= ~ssl.OP_IGNORE_UNEXPECTED_EOF

    return trio.SSLStream(
        tcp_stream, ssl_context, server_hostname=host, https_compatible=https_compatible
    )


async def open_ssl_over_tcp_listeners(
    port, ssl_context, *, host=None, https_compatible=False, backlog=None
):
    """Start listening for SSL/TLS-encrypted TCP connections to the given port.

    Args:
      port (int): The port to listen on. See :func:`open_tcp_listeners`.
      ssl_context (~ssl.SSLContext): The SSL context to use for all incoming
          connections.
      host (str, bytes, or None): The address to bind to; use ``None`` to bind
          to the wildcard address. See :func:`open_tcp_listeners`.
      https_compatible (bool): See :class:`~trio.SSLStream` for details.
      backlog (int or None): See :func:`open_tcp_listeners` for details.

    """
    tcp_listeners = await trio.open_tcp_listeners(port, host=host, backlog=backlog)
    ssl_listeners = [
        trio.SSLListener(tcp_listener, ssl_context, https_compatible=https_compatible)
        for tcp_listener in tcp_listeners
    ]
    return ssl_listeners


async def serve_ssl_over_tcp(
    handler,
    port,
    ssl_context,
    *,
    host=None,
    https_compatible=False,
    backlog=None,
    handler_nursery=None,
    task_status=trio.TASK_STATUS_IGNORED,
):
    """Listen for incoming TCP connections, and for each one start a task
    running ``handler(stream)``.

    This is a thin convenience wrapper around
    :func:`open_ssl_over_tcp_listeners` and :func:`serve_listeners` – see them
    for full details.

    .. warning::

       If ``handler`` raises an exception, then this function doesn't do
       anything special to catch it – so by default the exception will
       propagate out and crash your server. If you don't want this, then catch
       exceptions inside your ``handler``, or use a ``handler_nursery`` object
       that responds to exceptions in some other way.

    When used with ``nursery.start`` you get back the newly opened listeners.
    See the documentation for :func:`serve_tcp` for an example where this is
    useful.

    Args:
      handler: The handler to start for each incoming connection. Passed to
          :func:`serve_listeners`.

      port (int): The port to listen on. Use 0 to let the kernel pick
          an open port. Ultimately passed to :func:`open_tcp_listeners`.

      ssl_context (~ssl.SSLContext): The SSL context to use for all incoming
          connections. Passed to :func:`open_ssl_over_tcp_listeners`.

      host (str, bytes, or None): The address to bind to; use ``None`` to bind
          to the wildcard address. Ultimately passed to
          :func:`open_tcp_listeners`.

      https_compatible (bool): Set this to True if you want to use
          "HTTPS-style" TLS. See :class:`~trio.SSLStream` for details.

      backlog (int or None): See :class:`~trio.SSLStream` for details.

      handler_nursery: The nursery to start handlers in, or None to use an
          internal nursery. Passed to :func:`serve_listeners`.

      task_status: This function can be used with ``nursery.start``.

    Returns:
      This function only returns when cancelled.

    """
    listeners = await trio.open_ssl_over_tcp_listeners(
        port,
        ssl_context,
        host=host,
        https_compatible=https_compatible,
        backlog=backlog,
    )
    await trio.serve_listeners(
        handler, listeners, handler_nursery=handler_nursery, task_status=task_status
    )
