import enum


class CategoryEnum(enum.Enum):
    """Base Category enum."""

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ExpenseCategory(CategoryEnum):
    """Expense Category enum."""

    GROCERIES = "groceries"
    RESTAURANT = "restaurant"
    ENTERTAINMENT = "entertainment"
    HOME = "home"
    MEDICINES = "medicines"
    CHILDREN = "children"
    INVESTMENTS = "investments"
    PETS = "pets"
    CAR = "car"
    BILL = "bill"
    OTHER = "other"


class IncomeCategory(CategoryEnum):
    """Income Category enum."""

    SALARY = "salary"
    SAVINGS = "savings"
    OTHER = "other"
