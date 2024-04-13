from sqlalchemy import Integer
from enum import Enum
from sqlalchemy.types import TypeDecorator

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