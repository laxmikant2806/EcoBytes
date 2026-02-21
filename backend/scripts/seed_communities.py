import asyncio
import uuid
from datetime import datetime
from app.firebase import get_firestore_client
from app.models.community import Community

COMMUNITIES = [
    {
        "name": "EcoBytes Hub",
        "type": "corporate",
        "area_of_work": ["recycling", "energy_saving"],
        "description": "The official community for EcoBytes employees and fans.",
        "location": "Global / Remote",
        "upcoming_events": [
            {
                "event_name": "Quarterly All-Hands Sustainability Sync",
                "date": datetime(2026, 3, 10, 15, 0),
                "location": "Virtual (Zoom)"
            },
            {
                "event_name": "Annual Corporate Steps Challenge",
                "date": datetime(2026, 4, 1, 9, 0),
                "location": "Global"
            }
        ],
        "image_url": "https://images.unsplash.com/photo-1542601906-973ad30ed20d?auto=format&fit=crop&q=80&w=800",
        "member_count": 1250,
        "rating": 4.9,
    },
    {
        "name": "Zero Waste Warriors",
        "type": "ngo",
        "area_of_work": ["waste_cleanup", "composting"],
        "description": "Dedicated to reducing landfill waste through education and action.",
        "location": "San Francisco, CA",
        "upcoming_events": [
            {
                "event_name": "Ocean Beach Weekend Cleanup",
                "date": datetime(2026, 3, 15, 8, 30),
                "location": "Ocean Beach, SF"
            }
        ],
        "image_url": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&q=80&w=800",
        "member_count": 840,
        "rating": 4.7,
    },
    {
        "name": "Urban Gardeners",
        "type": "local",
        "area_of_work": ["tree_planting", "composting"],
        "description": "Turning rooftops and balconies into green sanctuaries.",
        "location": "London, UK",
        "upcoming_events": [],
        "image_url": "https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?auto=format&fit=crop&q=80&w=800",
        "member_count": 420,
        "rating": 4.8,
    },
]

async def seed():
    db = get_firestore_client()
    for data in COMMUNITIES:
        doc_id = str(uuid.uuid4())
        comm = Community(
            id=doc_id,
            name=data["name"],
            type=data["type"],
            area_of_work=data["area_of_work"],
            description=data.get("description"),
            location=data.get("location"),
            image_url=data["image_url"],
            upcoming_events=data.get("upcoming_events", []),
            member_count=data["member_count"],
            members=[],
            rating=data["rating"],
            admin_id="system",
            created_at=datetime.utcnow()
        )
        await db.collection("communities").document(doc_id).set(comm.model_dump())
        print(f"Seeded: {comm.name}")

if __name__ == "__main__":
    asyncio.run(seed())
