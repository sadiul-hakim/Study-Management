import json
import random
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.html import format_html
from .translator import translate_en_to_bn

from .models import WordCollection, VocabularyExamResult


@ensure_csrf_cookie
def vocabulary_hub(request):
    """Main friendly website view for Vocabulary Practice & Exam."""
    total_count = WordCollection.objects.count()
    new_count = WordCollection.objects.filter(status=WordCollection.Status.NEW).count()
    familiar_count = WordCollection.objects.filter(status=WordCollection.Status.FAMILIAR).count()
    unfamiliar_count = WordCollection.objects.filter(status=WordCollection.Status.UNFAMILIAR).count()
    confident_count = WordCollection.objects.filter(status=WordCollection.Status.CONFIDENT).count()

    recent_exams = VocabularyExamResult.objects.all()[:5]

    context = {
        'total_count': total_count,
        'new_count': new_count,
        'familiar_count': familiar_count,
        'unfamiliar_count': unfamiliar_count,
        'confident_count': confident_count,
        'recent_exams': recent_exams,
        'status_choices': WordCollection.Status.choices,
    }
    return render(request, 'vocabulary/hub.html', context)


@require_GET
def api_random_words(request):
    """Returns 10-20 random words with optional status filtering."""
    try:
        count = int(request.GET.get('count', 10))
        count = max(5, min(count, 30))
    except (ValueError, TypeError):
        count = 10

    status_filter = request.GET.get('status', 'all').strip().lower()

    qs = WordCollection.objects.all()
    if status_filter and status_filter != 'all':
        qs = qs.filter(status=status_filter)

    ids = list(qs.values_list('id', flat=True))
    if not ids:
        return JsonResponse({
            'status': 'ok',
            'words': [],
            'total_available': 0,
            'message': 'No words found matching the selected filter.'
        })

    sample_size = min(len(ids), count)
    random_ids = random.sample(ids, sample_size)
    words_qs = list(WordCollection.objects.filter(id__in=random_ids))
    random.shuffle(words_qs)

    words_data = [
        {
            'id': w.id,
            'english': w.english,
            'bengali': w.bengali,
            'status': w.status,
            'status_label': w.get_status_display(),
        }
        for w in words_qs
    ]

    return JsonResponse({
        'status': 'ok',
        'words': words_data,
        'total_available': len(ids),
        'count': len(words_data),
    })


@require_POST
def api_update_word_status(request, word_id):
    """Instantly updates a word's learning status."""
    word = get_object_or_404(WordCollection, id=word_id)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    new_status = data.get('status', '').strip().lower()
    valid_statuses = [choice[0] for choice in WordCollection.Status.choices]

    if new_status not in valid_statuses:
        return JsonResponse({
            'status': 'error',
            'message': f'Invalid status. Choose from: {", ".join(valid_statuses)}'
        }, status=400)

    word.status = new_status
    word.save(update_fields=['status', 'updated_at'])

    # Return updated counts
    counts = {
        'total': WordCollection.objects.count(),
        'new': WordCollection.objects.filter(status=WordCollection.Status.NEW).count(),
        'familiar': WordCollection.objects.filter(status=WordCollection.Status.FAMILIAR).count(),
        'unfamiliar': WordCollection.objects.filter(status=WordCollection.Status.UNFAMILIAR).count(),
        'confident': WordCollection.objects.filter(status=WordCollection.Status.CONFIDENT).count(),
    }

    return JsonResponse({
        'status': 'ok',
        'word_id': word.id,
        'new_status': word.status,
        'status_label': word.get_status_display(),
        'counts': counts,
    })


@require_GET
def api_take_exam(request):
    """Generates 10 multiple-choice questions for the exam."""
    mode = request.GET.get('mode', 'en_to_bn').strip()
    if mode not in ['en_to_bn', 'bn_to_en', 'mixed']:
        mode = 'en_to_bn'

    try:
        count = int(request.GET.get('count', 10))
        count = max(5, min(count, 20))
    except (ValueError, TypeError):
        count = 10

    # Ensure words have both english and non-empty bengali
    valid_words = list(WordCollection.objects.exclude(bengali='').exclude(bengali__isnull=True).values('id', 'english', 'bengali', 'status'))

    if len(valid_words) < 4:
        return JsonResponse({
            'status': 'error',
            'message': 'At least 4 words with Bengali translations are required to generate an exam.'
        }, status=400)

    sample_size = min(len(valid_words), count)
    exam_targets = random.sample(valid_words, sample_size)

    questions = []
    for i, target in enumerate(exam_targets, 1):
        q_mode = mode
        if mode == 'mixed':
            q_mode = random.choice(['en_to_bn', 'bn_to_en'])

        # Pick 3 random distractor words
        other_words = [w for w in valid_words if w['id'] != target['id']]
        distractors = random.sample(other_words, min(3, len(other_words)))

        if q_mode == 'en_to_bn':
            prompt_word = target['english']
            question_type = "English to Bengali"
            correct_answer = target['bengali']
            distractor_answers = [d['bengali'] for d in distractors]
        else:
            prompt_word = target['bengali']
            question_type = "Bengali to English"
            correct_answer = target['english']
            distractor_answers = [d['english'] for d in distractors]

        options = list(set([correct_answer] + distractor_answers))
        # Ensure we have 4 options if possible
        while len(options) < 4 and len(other_words) > len(options):
            filler = random.choice(other_words)
            val = filler['bengali'] if q_mode == 'en_to_bn' else filler['english']
            if val not in options:
                options.append(val)

        random.shuffle(options)

        questions.append({
            'q_num': i,
            'word_id': target['id'],
            'prompt': prompt_word,
            'mode': q_mode,
            'question_type': question_type,
            'options': options,
        })

    return JsonResponse({
        'status': 'ok',
        'mode': mode,
        'total': len(questions),
        'questions': questions,
    })


@require_POST
def api_submit_exam(request):
    """Evaluates exam answers, logs the attempt, and returns results breakdown."""
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    answers = data.get('answers', [])
    mode = data.get('mode', 'en_to_bn')

    if not answers:
        return JsonResponse({'status': 'error', 'message': 'No answers submitted.'}, status=400)

    word_ids = [a.get('word_id') for a in answers if a.get('word_id')]
    words_map = {w.id: w for w in WordCollection.objects.filter(id__in=word_ids)}

    correct_count = 0
    breakdown = []

    for item in answers:
        word_id = item.get('word_id')
        selected = item.get('selected', '').strip()
        q_mode = item.get('mode', 'en_to_bn')
        prompt = item.get('prompt', '')

        word = words_map.get(word_id)
        if not word:
            continue

        if q_mode == 'en_to_bn':
            correct_ans = word.bengali
            prompt_display = word.english
        else:
            correct_ans = word.english
            prompt_display = word.bengali

        is_correct = (selected.strip().lower() == correct_ans.strip().lower())
        if is_correct:
            correct_count += 1

        breakdown.append({
            'word_id': word.id,
            'prompt': prompt_display,
            'english': word.english,
            'bengali': word.bengali,
            'selected': selected,
            'correct_answer': correct_ans,
            'is_correct': is_correct,
            'current_status': word.status,
            'status_label': word.get_status_display(),
            'mode': q_mode,
        })

    total_q = len(breakdown)
    percentage = (correct_count / total_q * 100) if total_q > 0 else 0.0

    # Save to database
    exam_record = VocabularyExamResult.objects.create(
        score=correct_count,
        total_questions=total_q,
        percentage=percentage,
        mode=mode if mode in ['en_to_bn', 'bn_to_en', 'mixed'] else 'en_to_bn',
        details=breakdown,
    )

    # Friendly encouragement message
    if percentage >= 90:
        feedback = "Outstanding! 🌟 You have exceptional vocabulary retention."
    elif percentage >= 70:
        feedback = "Great work! 👏 Solid grasp of these words."
    elif percentage >= 50:
        feedback = "Good effort! 📖 A little more revision will make them stick."
    else:
        feedback = "Keep going! 💪 Practice regularly to build strong recall."

    return JsonResponse({
        'status': 'ok',
        'exam_id': exam_record.id,
        'score': correct_count,
        'total': total_q,
        'percentage': round(percentage, 1),
        'feedback': feedback,
        'breakdown': breakdown,
    })


def add_word_htmx(request):
    """HTMX / web endpoint to add and auto-translate a word."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    english = request.POST.get('english', '').strip()

    if not english:
        return HttpResponse(
            format_html(
                '<div class="alert alert-danger mt-2 mb-0 py-2">Please enter an English word.</div>'
            )
        )

    # Check for existing word
    existing = WordCollection.objects.filter(english__iexact=english).first()
    if existing:
        return HttpResponse(
            format_html(
                '<div class="alert alert-warning mt-2 mb-0 py-2">"{}" already exists with meaning "{}" ({})</div>',
                existing.english, existing.bengali, existing.get_status_display()
            )
        )

    bengali = translate_en_to_bn(english)

    try:
        word = WordCollection.objects.create(
            english=english,
            bengali=bengali,
            status=WordCollection.Status.NEW,
        )
        return HttpResponse(
            format_html(
                '<div class="alert alert-success mt-2 mb-0 py-2">'
                'Added <strong>"{}"</strong> → <strong>"{}"</strong> ✅</div>',
                word.english, word.bengali or '(translation unavailable)'
            )
        )
    except Exception as e:
        return HttpResponse(
            format_html(
                '<div class="alert alert-danger mt-2 mb-0 py-2">Failed to save word: {}</div>',
                str(e)
            )
        )
