from agents.management.commands.utils import get_prod_credentials


def test_get_prod_credentials() -> None:
    prod_credentials = get_prod_credentials()
    assert isinstance(prod_credentials, dict)
