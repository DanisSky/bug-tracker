import enum


class RoleEnum(enum.Enum):
    MANAGER = 'manager'
    TEAM_LEADER = 'team_leader'
    DEVELOPER = 'developer'
    TEST_ENGINEER = 'test_engineer'


class StatusEnum(enum.Enum):
    TO_DO = 'to_do'
    IN_PROGRESS = 'in_progress'
    CODE_REVIEW = 'code_review'
    DEV_TEST = 'dev_test'
    TESTING = 'testing'
    DONE = 'done'
    WONTFIX = 'wontfix'


class TypeEnum(enum.Enum):
    BUG = 'bug'
    TASK = 'task'


class PriorityEnum(enum.Enum):
    CRITICAL = 'critical'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class SortOrderEnum(enum.Enum):
    ASC = 'asc'
    desc = 'desc'
