from typing import List
from app.models import PlaceOfInterestModel

# Simulated Points of Interest Database
_PLACES_DATABASE = {
    "goa": [
        PlaceOfInterestModel(
            name="Baga Beach",
            description="Famous beach known for water sports, shacks, and night life.",
            category="Beach",
            rating=4.5,
            estimated_hours=4.0,
            entry_fee_inr=0.0
        ),
        PlaceOfInterestModel(
            name="Aguada Fort",
            description="17th-century Portuguese fort and lighthouse overlooking the Arabian Sea.",
            category="Historical",
            rating=4.6,
            estimated_hours=2.5,
            entry_fee_inr=50.0
        ),
        PlaceOfInterestModel(
            name="Dudhsagar Waterfalls",
            description="Four-tiered waterfall located on the Mandovi River.",
            category="Nature",
            rating=4.7,
            estimated_hours=6.0,
            entry_fee_inr=500.0
        )
    ],
    "jaipur": [
        PlaceOfInterestModel(
            name="Amer Fort",
            description="Opulent palace complex built from red sandstone and marble.",
            category="Historical",
            rating=4.8,
            estimated_hours=3.5,
            entry_fee_inr=100.0
        ),
        PlaceOfInterestModel(
            name="Hawa Mahal",
            description="Palace constructed from red and pink sandstone with 953 windows.",
            category="Architecture",
            rating=4.4,
            estimated_hours=1.5,
            entry_fee_inr=50.0
        )
    ],
    "manali": [
        PlaceOfInterestModel(
            name="Solang Valley",
            description="Side valley at the top of the Kullu Valley known for adventure sports.",
            category="Adventure",
            rating=4.6,
            estimated_hours=5.0,
            entry_fee_inr=0.0
        ),
        PlaceOfInterestModel(
            name="Hadimba Temple",
            description="Ancient cave temple dedicated to Hidimbi Devi.",
            category="Culture",
            rating=4.5,
            estimated_hours=1.5,
            entry_fee_inr=0.0
        )
    ]
}


async def fetch_places_of_interest(destination: str) -> List[PlaceOfInterestModel]:
    """Fetches places of interest based on destination."""
    dest_key = destination.strip().lower()
    return _PLACES_DATABASE.get(dest_key, [
        PlaceOfInterestModel(
            name=f"{destination.title()} Central Square",
            description=f"Popular local landmark and market area in {destination.title()}.",
            category="Sightseeing",
            rating=4.2,
            estimated_hours=2.0,
            entry_fee_inr=0.0
        )
    ])