from collections.abc import Sequence
from typing import NewType, Iterable

Account = NewType("Account", str)


def into_accounts(strings: Iterable[str]) -> Sequence[Account]:
    return tuple(Account(account) for account in strings)
