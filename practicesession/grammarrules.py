from typing import List, Set, Tuple
from uuid import UUID

from django.db.models import QuerySet

from users.models import User
from quiz.models import QuizQuestion
from quiz.grammarrules import (
    get_questions_by_asking_date,
    get_usable_grammar_rule_examples,
    get_grammar_rule_questions_queryset_for_user
)

def get_grammar_rule_questions(
    user: User,
    number_of_questions: int = 6
) -> List[Tuple[UUID, UUID]]:
    num_questions_for_group = number_of_questions // 3
    possible_examples = get_usable_grammar_rule_examples(user)
    grammar_rules: Set[UUID] = set([])
    examples: Set[UUID] = set([])
    for (
        days_since_asked_lower_bound,
        days_since_asked_upper_bound,
        should_include_unasked
    ) in [
        (1, 5, True),
        (5, 10, False),
        (10, 30, False)
    ]:
        questions = get_questions_by_asking_date(
            user,
            days_since_asked_lower_bound,
            days_since_asked_upper_bound,
            should_include_unasked
        )
        grammar_rules, examples = _get_questions(
            possible_examples, grammar_rules, examples, questions, num_questions_for_group
        )
    all_grammar_rules = get_grammar_rule_questions_queryset_for_user(user)
    grammar_rules, examples = _get_questions(
        possible_examples, grammar_rules, examples, all_grammar_rules, number_of_questions - len(grammar_rules)
    )
    return list(zip(grammar_rules, examples))


def _get_questions(
    possible_examples: QuerySet,
    grammar_rules: Set[UUID],
    examples: Set[UUID],
    questions: QuerySet,
    number_of_questions_per_group: int
) -> Tuple[Set[UUID], Set[UUID]]:
    stopping_length = len(grammar_rules) + number_of_questions_per_group
    grammar_rules: Set[str] = grammar_rules
    while (
        len(grammar_rules) < stopping_length and
        questions
    ):
        question = questions[0]
        if not question.user_grammar_rule_entry in grammar_rules:
            grammar_rules.add(question.user_grammar_rule_entry.id)
            example = (
                possible_examples.filter(
                    grammar_rule=question.user_grammar_rule_entry.grammar_rule
                )
                .order_by("?")
                .first()
            )
            examples.add(example.id)
        questions = questions[1:]
    return grammar_rules, examples
