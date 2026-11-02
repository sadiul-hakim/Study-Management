from .models import Exam, Improve


def admin_exam(request):
    exam = Exam.objects.filter(completed=False).order_by("-exam_date").all() or False
    return {"exam_list": exam if exam is not False else None}


def admin_improve_exam(request):
    improve_exam_list = Improve.objects.all() or False
    return {
        "improve_exam_list": improve_exam_list
        if improve_exam_list is not False
        else None
    }
