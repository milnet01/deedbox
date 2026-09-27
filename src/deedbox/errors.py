"""The errors every Deedbox part raises. `ui` turns each into one message."""


class DeedboxError(Exception):
    """Base class for every expected Deedbox failure."""


class NotAVault(DeedboxError):
    """The folder holds no vault header."""


class VaultExists(DeedboxError):
    """A vault was to be created in a folder that is not empty."""


class WrongPassword(DeedboxError):
    """The key record would not unwrap with this password."""


class VaultCorrupt(DeedboxError):
    """A vault file failed to decrypt or parse."""


class NotEnoughMemory(DeedboxError):
    """Key derivation could not allocate the memory it needs."""


class VaultTooNew(DeedboxError):
    """A format number above what this release reads."""


class DocumentMissing(DeedboxError):
    """No document with that id is in the vault."""
