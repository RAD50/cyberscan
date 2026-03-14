"""Security module for access control and authorization."""

from .access_control import restricted, admin_only

__all__ = ["restricted", "admin_only"]
