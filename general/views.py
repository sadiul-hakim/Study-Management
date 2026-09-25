# views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.html import format_html
from vocabulary.translator import translate_en_to_bn
from vocabulary.models import WordCollection


@staff_member_required
def add_word_htmx(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    english = request.POST.get('english', '').strip()

    if not english:
        return HttpResponse(
            format_html(
                '<div class="alert alert-danger mt-2 mb-0 py-2">Please enter a word.</div>'
            )
        )

    bengali = translate_en_to_bn(english)

    try:
        WordCollection.objects.create(
            english=english,
            bengali=bengali,
            status=WordCollection.Status.NEW,
        )
        return HttpResponse(
            format_html(
                '<div class="alert alert-success mt-2 mb-0 py-2">'
                'Added "{}" → "{}" ✅</div>',
                english, bengali or '(translation unavailable)'
            )
        )
    except Exception:
        return HttpResponse(
            format_html(
                '<div class="alert alert-danger mt-2 mb-0 py-2">Failed to save word.</div>'
            )
        )
