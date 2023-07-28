from typing import Dict, NamedTuple, Set
from uuid import UUID

from .words import get_word_questions_for_practice_session
from .grammarrules import get_grammar_rule_questions_for_practice_session
from .utils import (
    get_finished_quiz_question_ids,
    get_correctly_answered_questions_for_practice_session,
    FINISHED_CORRECT_TIMES
)

from users.models import User
from quiz.models import QuestionType


class SessionMasteryStatistics(NamedTuple):
    terms_mastered: int
    total_number_of_terms: int
    number_of_questions_answered_correctly: int
    total_number_of_questions: int


def get_mastery_for_session_id(
    user: User,
    practice_session_id: UUID
) -> SessionMasteryStatistics:
    mastered_question_ids = set(get_finished_quiz_question_ids(practice_session_id))
    word_mastery = _get_word_question_mastery(user, mastered_question_ids, practice_session_id)
    grammar_rule_mastery = _get_grammar_rule_question_mastery(user, mastered_question_ids, practice_session_id)
    total_number_of_terms = word_mastery.total_number_of_terms + grammar_rule_mastery.total_number_of_terms
    return SessionMasteryStatistics(
        terms_mastered=word_mastery.terms_mastered + grammar_rule_mastery.terms_mastered,
        total_number_of_terms=total_number_of_terms,
        total_number_of_questions=(total_number_of_terms * FINISHED_CORRECT_TIMES * len(QuestionType)),
        number_of_questions_answered_correctly=len(get_correctly_answered_questions_for_practice_session(practice_session_id)),
    )

def _get_word_question_mastery(
    user: User,
    mastered_question_ids: Set[UUID],
    practice_session_id: UUID
) -> SessionMasteryStatistics:
    mastered_terms: Dict[UUID, int] = {}
    word_questions = get_word_questions_for_practice_session(user, practice_session_id)
    for q in word_questions:
        mastery = 0 if q.id not in mastered_question_ids else 1
        mastered_terms[q.user_vocabulary_entry.id] = mastered_terms.get(q.user_vocabulary_entry.id, 0) + mastery
    return SessionMasteryStatistics(
        terms_mastered=sum([1 if value == len(QuestionType) else 0 for value in mastered_terms.values() ]),
        total_number_of_terms=len(mastered_terms),
        total_number_of_questions=0,
        number_of_questions_answered_correctly=0
    )


def _get_grammar_rule_question_mastery(
    user: User,
    mastered_question_ids: Set[UUID],
    practice_session_id: UUID
) -> SessionMasteryStatistics:
    mastered_terms: Dict[UUID, int] = {}
    grammar_rule_questions = get_grammar_rule_questions_for_practice_session(user, practice_session_id)
    for q in grammar_rule_questions:
        mastery = 0 if q.id not in mastered_question_ids else 1
        mastered_terms[q.user_grammar_rule_entry.id] = mastered_terms.get(q.user_grammar_rule_entry.id, 0) + mastery
    return SessionMasteryStatistics(
        terms_mastered=sum([1 if value == len(QuestionType) else 0 for value in mastered_terms.values() ]),
        total_number_of_terms=len(mastered_terms),
        total_number_of_questions=0,
        number_of_questions_answered_correctly=0
    )
