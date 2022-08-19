class EnvironmentVariableNotFoundError(Exception):
    """Exception raised when the environment variable needed is not set.

    Attributes:
        environ -- the needed environment variable
    """

    def __init__(self, environ: str):
        self.environ = environ
        super().__init__(
            f'Environment variable "{self.environ}" is not set.\nTry to setup an `.env` file.'
        )
