# usersapp/management/commands/cleanduplicates.py
from django.core.management.base import BaseCommand
from usersapp.models import UserProfileModel
from helpers.phone_utils import normalize_phone_number

class Command(BaseCommand):
    help = "Clean duplicate phone numbers in UserProfileModel based on normalized values."

    def handle(self, *args, **options):
        seen = {}
        duplicates = []
        # Use .only() to select only 'id' and 'phone_number' and avoid loading 'card_token'
        profiles = UserProfileModel.objects.all().only('id', 'phone_number')
        for profile in profiles:
            try:
                normalized_phone = normalize_phone_number(profile.phone_number)
            except Exception:
                normalized_phone = profile.phone_number  # fallback if normalization fails

            if normalized_phone in seen:
                duplicates.append(profile)
            else:
                seen[normalized_phone] = profile

        if duplicates:
            self.stdout.write(f"Found {len(duplicates)} duplicate records. Deleting duplicates...")
            for dup in duplicates:
                self.stdout.write(f"Deleting duplicate: {dup.phone_number} (ID: {dup.id})")
                dup.delete()
            self.stdout.write("Duplicate cleanup complete.")
        else:
            self.stdout.write("No duplicates found.")
