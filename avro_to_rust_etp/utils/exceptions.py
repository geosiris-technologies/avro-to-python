""" contains all exceptions raised for package """

NoFileOrDir = ValueError('Must specify a file or directory')

class NotAvscFileError(ValueError):
    pass

class MissingFileError(OSError):
    pass

class NoFilesError(OSError):
    pass

BadReferenceError = ValueError('field to be referenced missing namespace or name keys')
