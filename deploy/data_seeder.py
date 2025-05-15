from booking.models.providers import Providers
from booking.models.services import Services
from booking.models.services_offered import ServicesOffered
from booking.models.rooms import Rooms
from booking.models.room_supported_services import RoomSupportedServices
from booking.models.users import Users
from booking.models.bookings import Bookings
from typing import List

provider_service_map = {
    "Spa & Wellness Center": [
        "Swedish Massage",
        "Deep Tissue Massage",
        "Facial Treatment",
        "Haircut",
        "Manicure",
        "Pedicure",
    ],
    "Beauty Salon": ["Haircut", "Manicure", "Pedicure"],
    "Massage Therapy Center": ["Swedish Massage", "Deep Tissue Massage"],
}

room_service_map = {
    "Spa & Wellness Center": {
        1: ["Swedish Massage", "Deep Tissue Massage", "Facial Treatment"],
        2: ["Haircut", "Manicure", "Pedicure"],
        3: ["Swedish Massage", "Pedicure"],
    },
    "Beauty Salon": {
        1: ["Haircut", "Manicure", "Pedicure"],
        2: ["Haircut"],
        3: ["Pedicure"],
    },
    "Massage Therapy Center": {
        1: ["Swedish Massage", "Deep Tissue Massage"],
        2: ["Swedish Massage"],
        3: ["Swedish Massage"],
    },
}


def seed_providers() -> List[Providers]:
    providers = [
        {"name": "Spa & Wellness Center"},
        {"name": "Beauty Salon"},
        {"name": "Massage Therapy Center"},
    ]

    created_providers = []
    for provider_data in providers:
        provider = Providers.objects.create(**provider_data)
        created_providers.append(provider)
        print(f"Created provider: {provider.name}")

    return created_providers


def seed_services() -> List[Services]:
    services = [
        {"name": "Swedish Massage", "duration": 60},
        {"name": "Deep Tissue Massage", "duration": 90},
        {"name": "Facial Treatment", "duration": 30},
        {"name": "Haircut", "duration": 30},
        {"name": "Manicure", "duration": 30},
        {"name": "Pedicure", "duration": 120},
    ]

    created_services = []
    for service_data in services:
        service = Services.objects.create(**service_data)
        created_services.append(service)
        print(f"Created service: {service.name}")

    return created_services


def seed_services_offered(providers):
    for provider in providers:
        for service in provider_service_map[provider.name]:
            service = Services.objects.get(name=service)
            ServicesOffered.objects.create(provider=provider, service=service)
            print(f"Created service offering: {provider.name} - {service.name}")


def seed_rooms(providers) -> List[Rooms]:
    created_rooms = []
    for provider in providers:
        # Create 3 rooms for each provider
        for i in range(3):
            room = Rooms.objects.create(provider=provider)
            created_rooms.append(room)
            print(f"Created room: {room.id} for {provider.name}")

    return created_rooms


def seed_room_supported_services(providers: List[Providers], services: List[Services]):
    for provider in providers:
        rooms = Rooms.objects.filter(provider=provider)
        for i, room in enumerate(rooms):
            supported_services = room_service_map[provider.name][i + 1]
            for service in services:
                if service.name in supported_services:
                    RoomSupportedServices.objects.create(room=room, service=service)
                    print(
                        f"Created room service support: Room {room.id} - {service.name}"
                    )


def seed_users():
    users = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Smith", "email": "jane@example.com"},
        {"name": "Bob Wilson", "email": "bob@example.com"},
    ]

    created_users = []
    for user_data in users:
        user = Users.objects.create(**user_data)
        created_users.append(user)
        print(f"Created user: {user.name}")

    return created_users


def seed_data():
    print("Starting data seeding...")

    # Clear existing data
    Bookings.objects.all().delete()
    RoomSupportedServices.objects.all().delete()
    Rooms.objects.all().delete()
    ServicesOffered.objects.all().delete()
    Services.objects.all().delete()
    Providers.objects.all().delete()
    Users.objects.all().delete()

    # Seed data
    providers = seed_providers()
    services = seed_services()
    seed_services_offered(providers)
    seed_rooms(providers)
    seed_room_supported_services(providers, services)
    seed_users()

    print("Data seeding completed!")
