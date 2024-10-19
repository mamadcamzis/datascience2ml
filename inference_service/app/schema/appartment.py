"""Schema for appartment."""

from pydantic import BaseModel


class Appartment(BaseModel):
    """
    Appartment schema.

    area - Appartment area in square meters.
    constraction_year - Year of constraction.
    bedrooms - Number of bedrooms.
    garden - Garden availability.
    balcony_yes - Balcony availability.
    parking_yes - Parking availability.,
    furnished_yes - Furnished availability.
    garage_yes - Garage availability.
    storage_yes - Storage availability.

    """

    area: int
    constraction_year: int
    bedrooms: int
    garden: int
    balcony_yes: int
    parking_yes: int
    furnished_yes: int
    garage_yes: int
    storage_yes: int
