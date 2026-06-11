from sqlalchemy.orm import Session

from app.models.country import Country


def format_country(country: Country):

    return {
        "id": country.id,
        "name": country.name,
        "region": country.region,
        "iso3": country.iso3,
        "iso2": country.iso2,
        "phonecode": country.phonecode,
        "capital": country.capital,
        "currency": country.currency,
        "status": country.status,
        "wikidata_id": country.wikidata_id,
        "created_at": country.created_at,
        "updated_at": country.updated_at,
    }


def create_country(
    db: Session,
    data,
):

    country = Country(**data.dict())

    db.add(country)

    db.commit()

    db.refresh(country)

    return format_country(country)


def get_countries(
    db: Session,
):

    countries = db.query(Country).order_by(Country.name.asc()).all()

    return [format_country(country) for country in countries]


def get_country(
    db: Session,
    country_id: int,
):

    country = db.query(Country).filter(Country.id == country_id).first()

    if not country:
        return None

    return format_country(country)


def update_country(
    db: Session,
    country_id: int,
    data,
):

    country = db.query(Country).filter(Country.id == country_id).first()

    if not country:
        return None

    for field, value in data.dict(exclude_unset=True).items():

        setattr(
            country,
            field,
            value,
        )

    db.commit()

    db.refresh(country)

    return format_country(country)


def delete_country(
    db: Session,
    country_id: int,
):

    country = db.query(Country).filter(Country.id == country_id).first()

    if not country:
        return False

    db.delete(country)

    db.commit()

    return True
