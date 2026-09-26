import os
import sys
import django

# Setup django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BA_study_management.settings')
django.setup()

from vocabulary.models import VocabularyType

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


def run():
    print("Seeding Vocabulary Types...")
    created_count = 0
    existing_count = 0

    for item in DEFAULT_TYPES:
        obj, created = VocabularyType.objects.get_or_create(
            name=item["name"],
            defaults={"description": item["description"]}
        )
        if created:
            created_count += 1
            print(f"  [+] Created: {obj.name}")
        else:
            existing_count += 1
            if not obj.description and item.get("description"):
                obj.description = item["description"]
                obj.save(update_fields=["description"])
            print(f"  [=] Exists:  {obj.name}")

    print(f"\nDone! {created_count} created, {existing_count} already existed. Total: {VocabularyType.objects.count()} types.")


if __name__ == "__main__":
    run()
