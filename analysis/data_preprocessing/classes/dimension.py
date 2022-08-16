from attr import define, field


@define
class Dimension:
    width: int = field(converter=int)
    height: int = field(converter=int)
