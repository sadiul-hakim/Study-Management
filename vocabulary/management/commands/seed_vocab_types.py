from django.core.management.base import BaseCommand
from vocabulary.models import VocabularyType


class Command(BaseCommand):
    help = "Seeds common Vocabulary Types (Phrasal Verbs, Idioms, Proverbs, etc.)"

    DEFAULT_TYPES = [
        {
            "name": "General Vocabulary",
            "description": "Standard individual words, parts of speech (nouns, verbs, adjectives, adverbs), and everyday vocabulary.",
        },
        {
            "name": "Phrasal Verb",
            "description": "Verbs combined with prepositions or adverbs with idiomatic meanings (e.g., 'give up', 'look after', 'carry on').",
        },
        {
            "name": "Idiom & Phrase",
            "description": "Figurative expressions and phrases whose meaning is not predictable from the individual words (e.g., 'piece of cake', 'once in a blue moon').",
        },
        {
            "name": "Proverb",
            "description": "Short, well-known traditional sayings offering advice or general truths (e.g., 'Honesty is the best policy', 'A stitch in time saves nine').",
        },
        {
            "name": "Collocation",
            "description": "Words that naturally and frequently go together in English (e.g., 'heavy rain', 'make a decision', 'pay attention').",
        },
        {
            "name": "One Word Substitution",
            "description": "Single words that accurately replace a sentence or descriptive phrase (e.g., 'Omnipotent', 'Philanthropist').",
        },
        {
            "name": "Academic & GRE",
            "description": "Advanced, formal, and high-frequency vocabulary frequently appearing in competitive exams and academic literature.",
        },
        {
            "name": "Literary Terms",
            "description": "Vocabulary and terminology specifically used in English literature, poetry, prose, and drama analysis.",
        },
        {
            "name": "Foreign Expressions",
            "description": "Latin, French, and other foreign phrases commonly adopted into English writing (e.g., 'ad hoc', 'status quo', 'bona fide').",
        },
    ]

    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0

        self.stdout.write(self.style.NOTICE("Seeding Vocabulary Types..."))

        for item in self.DEFAULT_TYPES:
            obj, created = VocabularyType.objects.get_or_create(
                name=item["name"],
                defaults={"description": item["description"]}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  + Created: {obj.name}"))
            else:
                existing_count += 1
                # Update description if it was blank
                if not obj.description and item.get("description"):
                    obj.description = item["description"]
                    obj.save(update_fields=["description"])
                self.stdout.write(self.style.WARNING(f"  = Exists:  {obj.name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nFinished seeding: {created_count} created, {existing_count} already existed. Total: {VocabularyType.objects.count()} types available."
            )
        )
