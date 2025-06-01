from django.db import models
from django.conf import settings
from collections import OrderedDict, deque
import heapq
from django.db.models import Prefetch


class Exam(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Durasi dalam menit")
    created_at = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(
        auto_now_add=False, help_text="Tanggal mulai ujian", blank=True, null=True
    )

    class Meta:
        ordering = ["-created_at", "title"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["subject"]),
            models.Index(fields=["date_start"]),
        ]

    def __str__(self):
        return self.title

    def get_total_questions(self):
        """Get total number of questions using efficient counting"""
        return self.questions.count()

    def get_total_points(self):
        """Get total points using aggregation for better performance"""
        from django.db.models import Sum

        result = self.questions.aggregate(total=Sum("points"))
        return result["total"] or 0

    def get_question_tree(self):
        """Build a balanced BST of questions for efficient navigation - O(log n) access"""
        questions = list(self.questions.order_by("order"))
        return self._build_question_tree(questions, 0, len(questions) - 1)

    def _build_question_tree(self, questions, start, end):
        """Helper method to build binary search tree of questions"""
        if start > end:
            return None

        mid = (start + end) // 2
        node = {
            "question": questions[mid],
            "left": self._build_question_tree(questions, start, mid - 1),
            "right": self._build_question_tree(questions, mid + 1, end),
            "height": 1
            + max(
                self._get_height(self._build_question_tree(questions, start, mid - 1)),
                self._get_height(self._build_question_tree(questions, mid + 1, end)),
            ),
        }
        return node

    def _get_height(self, node):
        """Get height of BST node"""
        return node["height"] if node else 0

    def get_questions_priority_queue(self, user_answers=None):
        """Create min-heap priority queue for unanswered questions (order-based priority)"""
        questions = self.questions.order_by("order")
        answered_orders = set(user_answers.keys()) if user_answers else set()

        priority_queue = []
        for question in questions:
            if question.order not in answered_orders:
                # Min-heap: lower order = higher priority
                heapq.heappush(priority_queue, (question.order, question.id, question))

        return priority_queue

    def get_question_graph(self):
        """Build adjacency list graph for question dependencies/relationships"""
        questions = list(self.questions.order_by("order"))
        graph = {}

        for i, question in enumerate(questions):
            graph[question.id] = {
                "question": question,
                "prev": questions[i - 1].id if i > 0 else None,
                "next": questions[i + 1].id if i < len(questions) - 1 else None,
                "adjacents": [],  # Can be used for question grouping/topics
            }

        return graph

    def get_optimized_question_sequence(self, user_answers=None):
        """Use topological sort for optimal question sequence based on difficulty/dependencies"""
        questions = list(self.questions.order_by("order"))
        answered_orders = set(user_answers.keys()) if user_answers else set()

        # Create adjacency list based on difficulty progression
        adj_list = {q.id: [] for q in questions}
        in_degree = {q.id: 0 for q in questions}

        # Build dependencies (easier questions before harder ones)
        for i in range(len(questions) - 1):
            current = questions[i]
            next_q = questions[i + 1]
            if current.points <= next_q.points:  # Difficulty progression
                adj_list[current.id].append(next_q.id)
                in_degree[next_q.id] += 1

        # Kahn's algorithm for topological sort
        queue = deque(
            [
                q.id
                for q in questions
                if in_degree[q.id] == 0 and q.order not in answered_orders
            ]
        )
        result = []

        while queue:
            current_id = queue.popleft()
            current_q = next(q for q in questions if q.id == current_id)
            if current_q.order not in answered_orders:
                result.append(current_q)

            for neighbor_id in adj_list[current_id]:
                in_degree[neighbor_id] -= 1
                if in_degree[neighbor_id] == 0:
                    neighbor_q = next(q for q in questions if q.id == neighbor_id)
                    if neighbor_q.order not in answered_orders:
                        queue.append(neighbor_id)

        return result

    @classmethod
    def get_exams_with_stats(cls):
        """Optimized query with prefetch for better performance"""
        return cls.objects.prefetch_related(
            Prefetch("questions", queryset=Question.objects.order_by("order"))
        ).annotate(
            question_count=models.Count("questions"),
            total_points=models.Sum("questions__points"),
        )


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=50,
        choices=[("pilihan_ganda", "Pilihan Ganda")],
        default="pilihan_ganda",
    )
    points = models.IntegerField(default=1)
    order = models.IntegerField(help_text="Urutan soal dalam ujian")

    # Option fields using hash-based structure
    option_a = models.CharField(max_length=255, help_text="Pilihan A")
    option_b = models.CharField(max_length=255, help_text="Pilihan B")
    option_c = models.CharField(max_length=255, help_text="Pilihan C")
    option_d = models.CharField(max_length=255, help_text="Pilihan D")

    # Correct answer
    correct_answer = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        help_text="Pilihan jawaban yang benar",
    )

    class Meta:
        ordering = ["order"]
        unique_together = ("exam", "order")
        indexes = [
            models.Index(fields=["exam", "order"]),
            models.Index(fields=["points"]),
        ]

    def __str__(self):
        return f"Soal {self.order}: {self.question_text[:50]}"

    def get_options_hash(self):
        """Return options as OrderedDict for O(1) lookup with guaranteed order"""
        return OrderedDict(
            [
                (
                    "A",
                    {
                        "label": "A",
                        "text": self.option_a,
                        "is_correct": self.correct_answer == "A",
                    },
                ),
                (
                    "B",
                    {
                        "label": "B",
                        "text": self.option_b,
                        "is_correct": self.correct_answer == "B",
                    },
                ),
                (
                    "C",
                    {
                        "label": "C",
                        "text": self.option_c,
                        "is_correct": self.correct_answer == "C",
                    },
                ),
                (
                    "D",
                    {
                        "label": "D",
                        "text": self.option_d,
                        "is_correct": self.correct_answer == "D",
                    },
                ),
            ]
        )

    def get_options(self):
        """Return all options as a list using hash map conversion"""
        return list(self.get_options_hash().values())

    def get_option_text(self, label):
        """Get option text by label using hash map for O(1) lookup"""
        options_map = {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }
        return options_map.get(label, "")

    def get_difficulty_score(self):
        """Calculate difficulty score using weighted algorithm"""
        # Base difficulty on points and position
        position_weight = self.order / self.exam.get_total_questions()
        return self.points * (1 + position_weight)

    def save(self, *args, **kwargs):
        """Auto-assign order using binary search for optimal insertion"""
        if not self.order:
            existing_orders = list(
                Question.objects.filter(exam=self.exam)
                .order_by("order")
                .values_list("order", flat=True)
            )
            self.order = self._find_optimal_order(existing_orders)
        super().save(*args, **kwargs)

    def _find_optimal_order(self, existing_orders):
        """Find optimal order using binary search on gaps"""
        if not existing_orders:
            return 1

        # Binary search for gaps in sequence
        left, right = 1, len(existing_orders) + 1

        while left <= right:
            mid = (left + right) // 2
            if mid <= len(existing_orders) and existing_orders[mid - 1] == mid:
                left = mid + 1
            else:
                right = mid - 1

        return left


class StudentAnswer(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        null=True,
        blank=True,
    )
    marked_for_review = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    time_spent = models.IntegerField(default=0, help_text="Time spent in seconds")

    class Meta:
        ordering = ["-timestamp"]
        unique_together = ("student", "question")
        indexes = [
            models.Index(fields=["student", "question"]),
            models.Index(fields=["student", "marked_for_review"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"{self.student.username} - Soal {self.question.order}"

    def is_correct(self):
        """Check if the selected answer is correct using O(1) comparison"""
        return self.selected_option == self.question.correct_answer

    @classmethod
    def get_answers_hash_map(cls, student, exam):
        """Create hash map of answers for O(1) lookup by question order"""
        answers = cls.objects.select_related("question").filter(
            student=student, question__exam=exam
        )
        return {answer.question.order: answer for answer in answers}

    @classmethod
    def get_answer_statistics(cls, exam):
        """Generate answer statistics using efficient aggregation"""
        from django.db.models import Count, Q

        stats = {}
        questions = exam.questions.all()

        for question in questions:
            answer_distribution = cls.objects.filter(question=question).aggregate(
                total_answers=Count("id"),
                correct_answers=Count(
                    "id", filter=Q(selected_option=question.correct_answer)
                ),
                option_a_count=Count("id", filter=Q(selected_option="A")),
                option_b_count=Count("id", filter=Q(selected_option="B")),
                option_c_count=Count("id", filter=Q(selected_option="C")),
                option_d_count=Count("id", filter=Q(selected_option="D")),
            )

            stats[question.id] = {
                "question": question,
                "accuracy": (
                    answer_distribution["correct_answers"]
                    / answer_distribution["total_answers"]
                    * 100
                    if answer_distribution["total_answers"] > 0
                    else 0
                ),
                "distribution": answer_distribution,
            }

        return stats

    @classmethod
    def get_student_progress_tree(cls, student, exam):
        """Build progress tree using DFS traversal"""
        answers_map = cls.get_answers_hash_map(student, exam)
        questions = list(exam.questions.order_by("order"))

        def build_progress_node(question_list, start, end):
            if start > end:
                return None

            mid = (start + end) // 2
            question = question_list[mid]
            answer = answers_map.get(question.order)

            return {
                "question": question,
                "answered": answer is not None,
                "correct": answer.is_correct() if answer else None,
                "time_spent": answer.time_spent if answer else 0,
                "left": build_progress_node(question_list, start, mid - 1),
                "right": build_progress_node(question_list, mid + 1, end),
            }

        return build_progress_node(questions, 0, len(questions) - 1)
