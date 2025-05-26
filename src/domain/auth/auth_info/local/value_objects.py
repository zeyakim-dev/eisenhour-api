from dataclasses import dataclass

from domain.base.value_object import ValueObject


@dataclass(frozen=True)
class HashedPassword(ValueObject[str]):
    """해시 처리된 비밀번호를 표현하는 값 객체입니다.

    해싱된 문자열을 저장하며, 해시 비교 등의 용도로 사용됩니다.
    평문 비밀번호와는 다르며, 내부 값은 외부에서 직접 생성하거나 Hasher로 생성되어야 합니다.
    """

    pass
