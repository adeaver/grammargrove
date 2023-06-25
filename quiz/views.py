from random import choices, shuffle
from typing import Optional, NamedTuple
import datetime

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError
)

from .words import get_queryset_from_user_vocabulary
from .grammarrules import select_next_grammar_rule_question, get_grammar_rule_question_from_all
from grammarrules.examples import get_examples_for_grammar_rule, get_example_by_id

from .models import QuizQuestion, QuestionType, get_word_from_question
from uservocabulary.models import UserVocabularyEntry
from usergrammarrules.models import UserGrammarRuleEntry

from words.models import Word, Definition, LanguageCode
from grammarrules.models import GrammarRule

from .serializers import QuizQuestionSerializer

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizQuestionSerializer

    def get_queryset(self):
        return get_queryset_from_user_vocabulary(self.request.user)


#      def get_permissions(self):
#          if self.action == 'next':
#              return [IsAuthenticated(), ]
#          elif self.action == 'check':
#              return [IsAuthenticated(), ]
#          return []
#
#      @action(detail=False, methods=['get'])
#      def next(self, request: HttpRequest) -> HttpResponse:
#          class QuestionResponse(NamedTuple):
#              question_id: str
#              vocabulary_entry_id: Optional[str]
#              grammar_rule_entry_id: Optional[str]
#              example_id: Optional[str]
#              display: str
#              question_type: int
#              answer_spaces: Optional[int]
#
#          question_funcs = [
#              lambda: select_next_word_question(request),
#              lambda: select_next_grammar_rule_question(request),
#          ]
#          shuffle(question_funcs)
#          fallback_question_funcs = [
#              lambda: get_word_question_from_all(request, False),
#              lambda: get_grammar_rule_question_from_all(request, False),
#          ]
#          shuffle(fallback_question_funcs)
#          question: Optional[QuizQuestion] = None
#          for f in (question_funcs + fallback_question_funcs):
#              question = f()
#              if question is not None:
#                  break
#          if not question:
#              # TODO: gracefully handle this case
#              return HttpResponseBadRequest()
#          question.number_of_times_displayed += 1
#          question.last_displayed_at = timezone.now()
#          question.save()
#          display = _get_display_from_question(question)
#          return JsonResponse(
#              QuestionResponse(
#                  question_id=question.id,
#                  display=display.display,
#                  question_type=question.question_type,
#                  answer_spaces=display.answer_spaces,
#                  vocabulary_entry_id=display.vocabulary_entry_id,
#                  grammar_rule_entry_id=display.grammar_rule_entry_id,
#                  example_id=display.example_id,
#              )._asdict()
#          )
#
#      @action(detail=False, methods=['post'])
#      def check(self, request: HttpRequest) -> HttpResponse:
#          class CheckQuestionResponse(NamedTuple):
#              correct: bool
#              correct_answer: Optional[str]
#
#          question_id = request.data.get("question_id")
#          if not question_id:
#              return HttpResponseBadRequest()
#          answer = request.data.get("answer")
#          if not answer:
#              return HttpResponseBadRequest()
#          questions = QuizQuestion.objects.filter(
#              user=request.user, id=question_id
#          )
#          if not questions:
#              return HttpResponseBadRequest()
#          question = questions[0]
#          if question.user_vocabulary_entry:
#              word_payload = get_word_from_question(question, LanguageCode.ENGLISH)
#              if question.question_type == QuestionType.HanziFromEnglish:
#                  return JsonResponse(
#                      CheckQuestionResponse(
#                          correct=(answer == word_payload.word.display),
#                          correct_answer=word_payload.word.display
#                      )._asdict()
#                  )
#              elif question.question_type == QuestionType.AccentsFromHanzi:
#                  accents = answer.split(" ")
#                  correct_answer = [w[-1] for w in word_payload.word.pronunciation.split(" ")]
#                  correct = len(accents) == len(correct_answer)
#                  if correct:
#                      for idx, accent in enumerate(accents):
#                          correct = correct_answer[idx] == accent
#                          if not correct:
#                              break
#                  return JsonResponse(
#                      CheckQuestionResponse(
#                          correct=correct,
#                          correct_answer=" ".join(correct_answer)
#                      )._asdict()
#                  )
#              elif question.question_type == QuestionType.DefinitionsFromHanzi:
#                  correct_answer = (
#                      word_payload.user_vocabulary_entry.notes
#                      if word_payload.user_vocabulary_entry.notes is not None
#                      else " ".join([ d.definition for d in word_payload.definitions])
#                  )
#                  return JsonResponse(
#                      CheckQuestionResponse(
#                          correct=(answer == correct_answer),
#                          correct_answer=correct_answer
#                      )._asdict()
#                  )
#              else:
#                  return HttpResponseServerError()
#          elif question.user_grammar_rule_entry:
#              example_id = request.data.get("example_id")
#              if not example_id:
#                  return HttpResponseBadRequest()
#              example = get_example_by_id(example_id)
#              if not example:
#                  return HttpResponseBadRequest()
#              if question.question_type == QuestionType.HanziFromEnglish:
#                  correct_answer = example.hanzi
#              elif question.question_type == QuestionType.AccentsFromHanzi:
#                  correct_answer = " ".join([ p[-1] for p in example.pronunciation.split(" ") ])
#              elif question.question_type == QuestionType.DefinitionsFromHanzi:
#                  correct_answer = example.definition
#              else:
#                  raise ValueError(f"Unrecognized question type {question.question_type}")
#              return JsonResponse(
#                  CheckQuestionResponse(
#                      correct=(answer == correct_answer),
#                      correct_answer=correct_answer
#                  )._asdict()
#              )
#          else:
#              return HttpResponseServerError()
#
#  class QuestionDisplay(NamedTuple):
#      answer_spaces: Optional[int]
#      display: str
#      vocabulary_entry_id: Optional[str]
#      grammar_rule_entry_id: Optional[str]
#      example_id: Optional[str]
#
#  def _get_display_from_question(question: QuizQuestion) -> QuestionDisplay:
#      if question.user_vocabulary_entry is not None:
#          return _get_display_for_vocabulary_entry(question)
#      elif question.user_grammar_rule_entry is not None:
#          return _get_display_from_grammar_rule_entry(question)
#      else:
#          raise ValueError(f"Question {question.id} has neither grammar rule nor vocabulary entry")
#
#
#  def _get_display_for_vocabulary_entry(question: QuizQuestion) -> QuestionDisplay:
#      assert question.user_vocabulary_entry
#      vocabulary_entry = UserVocabularyEntry.objects.filter(id=question.user_vocabulary_entry.id).all()
#      if not vocabulary_entry:
#          raise AssertionError(f"User vocabulary {question.user_vocabulary_entry.id} does not exist")
#      word: Word = Word.objects.filter(id=vocabulary_entry[0].word.id)
#      if not word:
#          raise AssertionError(f"Word {vocabulary_entry.word.id} does not exist")
#      display: str = ""
#      answer_spaces: Optional[int] = None
#      if question.question_type in [QuestionType.AccentsFromHanzi, QuestionType.DefinitionsFromHanzi]:
#          # Some words are displayed with fewer characters than they are said with
#          # So the normal pronunciation screen won't work
#          answer_spaces = None if (
#              question.question_type != QuestionType.AccentsFromHanzi or
#              len(word[0].pronunciation.split(" ")) == len(word[0].display)
#          ) else len(word[0].pronunciation.split(" "))
#          display = word[0].display
#      elif question.question_type == QuestionType.HanziFromEnglish:
#          answer_spaces = None
#          if vocabulary_entry[0].notes:
#              display = vocabulary_entry.notes
#          else:
#              definitions = Definition.objects.filter(word=word[0].id, language_code=LanguageCode.ENGLISH).all()
#              display = "\n".join([ d.definition for d in definitions ]), None
#      else:
#          raise AssertionError(f"Unsupported Question Type {question.question_type}")
#      return QuestionDisplay(
#          answer_spaces=answer_spaces,
#          display=display,
#          vocabulary_entry_id=vocabulary_entry[0].id,
#          grammar_rule_entry_id=None,
#          example_id=None,
#      )
#
#
#  # TODO: handle case in which this doesn't return anything
#  # or make sure that user grammar rules has examples
#  def _get_display_from_grammar_rule_entry(question: QuizQuestion) -> QuestionDisplay:
#      assert question.user_grammar_rule_entry
#      user_grammar_rule_entry = UserGrammarRuleEntry.objects.filter(id=question.user_grammar_rule_entry.id)
#      assert user_grammar_rule_entry, (
#          f"User grammar rule {question.user_grammar_rule_entry.id} does not exist"
#      )
#      grammar_rule = GrammarRule.objects.filter(id=user_grammar_rule_entry[0].grammar_rule.id)
#      assert grammar_rule, (
#          f"Grammar rule {user_grammar_rule_entry[0].grammar_rule.id} does not exist"
#      )
#      grammar_rule_examples = get_examples_for_grammar_rule(grammar_rule[0].id)
#      assert grammar_rule_examples
#      example = choices(grammar_rule_examples, k=1)[0]
#      display: str = ""
#      if question.question_type in [QuestionType.AccentsFromHanzi, QuestionType.DefinitionsFromHanzi]:
#          # Some words are displayed with fewer characters than they are said with
#          # So the normal pronunciation screen won't work
#          answer_spaces = None if (
#              question.question_type != QuestionType.AccentsFromHanzi or
#              len(example.pronunciation.split(" ")) == len(example.hanzi)
#          ) else len(example.pronunciation.split(" "))
#          display = example.hanzi
#      elif question.question_type == QuestionType.HanziFromEnglish:
#          answer_spaces = None
#          display = example.definition
#      else:
#          raise AssertionError(f"Unsupported Question Type {question.question_type}")
#      return QuestionDisplay(
#          answer_spaces=None,
#          display=display,
#          vocabulary_entry_id=None,
#          grammar_rule_entry_id=question.user_grammar_rule_entry.id,
#          example_id=example.example_id,
#      )
