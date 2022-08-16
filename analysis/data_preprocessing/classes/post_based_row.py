from attr import define, field, asdict
from attr.converters import to_bool


@define
class PostBasedRow:
    image: str
    percentage: float = field(converter=float)
    postNumber: int = field(converter=int)
    isComment: bool = field(converter=to_bool)
    isExternal: bool = field(converter=to_bool)
    isCorrect: bool = field(converter=lambda x: not to_bool(x))
