from django.contrib import admin
from cbt.models import Exam, Question, StudentAnswer


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "subject",
        "duration",
        "get_question_count",
        "get_total_points",
        "date_start",
        "created_at",
    ]
    list_filter = ["subject", "created_at", "date_start"]
    search_fields = ["title", "subject"]
    ordering = ["-created_at", "title"]
    date_hierarchy = "created_at"

    def get_question_count(self, obj):
        return obj.get_total_questions()

    get_question_count.short_description = "Total Questions"
    get_question_count.admin_order_field = "questions__count"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "exam",
        "order",
        "question_text_preview",
        "question_type",
        "points",
        "correct_answer",
    ]
    list_filter = ["exam", "question_type", "points", "correct_answer"]
    search_fields = ["question_text", "exam__title"]
    ordering = ["exam", "order"]
    list_select_related = ["exam"]

    def question_text_preview(self, obj):
        return (
            obj.question_text[:75] + "..."
            if len(obj.question_text) > 75
            else obj.question_text
        )

    question_text_preview.short_description = "Question Preview"


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "question_info",
        "selected_option",
        "is_correct",
        "marked_for_review",
        "time_spent",
        "timestamp",
    ]
    list_filter = [
        "selected_option",
        "marked_for_review",
        "question__exam",
        "timestamp",
    ]
    search_fields = [
        "student__username",
        "question__question_text",
        "question__exam__title",
    ]
    ordering = ["-timestamp", "student", "question__order"]
    list_select_related = ["student", "question", "question__exam"]

    def question_info(self, obj):
        return f"{obj.question.exam.title} - Q{obj.question.order}"

    question_info.short_description = "Question"
    question_info.admin_order_field = "question__order"
