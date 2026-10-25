"""Retired compatibility module.

The production ASGI entry point is ``backend.main:app``.  This module remains
importable only so historical schema/unit tests can be run while the old
``backend.app`` package is removed in stages.  It deliberately exposes no
legacy routers, startup jobs, database initialisation, or permissive CORS.
There is no ``backend/Dockerfile``; deployments must use the repository root
Dockerfile and canonical entry point.
"""

# Deliberately not an ASGI application.  Keeping the symbol makes accidental
# imports fail at the server boundary instead of starting a second stack.
app = None
