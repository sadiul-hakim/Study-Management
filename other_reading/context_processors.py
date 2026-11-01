from .models import OtherStudyProgress


def admin_other_study_progress(request):
    other_study_progress = OtherStudyProgress.objects.all() or False
    return {
        "other_study_progress": other_study_progress
        if other_study_progress is not False
        else None
    }
