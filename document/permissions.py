from .models import Document, GenreAccess


def user_can_access_document(user, document):
    if user.is_superuser:
        return True

    return GenreAccess.objects.filter(
        genre=document.genre,
        group__user=user,
    ).exists()


def get_accessible_documents(user):
    if user.is_superuser:
        return Document.objects.all()

    return Document.objects.filter(
        genre__access_rules__group__user=user,
    ).distinct()


def user_can_access_link(user, link):
    if user.is_superuser:
        return True

    if link.owner_id == user.id:
        return True

    if link.genre:
        return user_can_access_genre(
            user,
            link.genre,
        )

    return False
