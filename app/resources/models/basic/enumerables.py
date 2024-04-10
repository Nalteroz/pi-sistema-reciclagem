from sqlalchemy import Integer
from enum import Enum
from sqlalchemy.types import TypeDecorator

class IntEnumType(TypeDecorator):
    """
    Description: This class is used to pass as a Enum type, for the SQLALchemy save it as an integer.
    """
    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnumType, self).__init__(*args, **kwargs)
        self.enumClass = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self.enumClass(value)

class UserRoleEnum(Enum):
    """
    Description: This class is used to define the role of a system element.
    """
    ADMIN = 0
    USER = 1

class CollaboratorRoleEnum(Enum):
    GERENTE = 0
    SUPERVISOR = 1
    COLABORADOR = 2
    EXTERNO = 3

class StorageHistoryTypeEnum(Enum):
    """
    Description: This class is used to define the type of a storage history.
    """
    ENTRADA = 0
    SAIDA = 1