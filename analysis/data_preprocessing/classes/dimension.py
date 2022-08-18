from attr import define, field


@define
class Dimension:
    """A class represents the dimension (width, height) of a image."""

    width: int = field(converter=int)
    height: int = field(converter=int)
