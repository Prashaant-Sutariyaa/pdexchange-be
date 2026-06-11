from sqlalchemy.orm import Session


class ExchangeService:

    @staticmethod
    def search(
        db: Session,
        filters: dict,
    ):
        pass