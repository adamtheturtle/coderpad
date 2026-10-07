"""Typed Screen question save payloads."""

from typing import ClassVar, Literal

from beartype import beartype
from pydantic import BaseModel, ConfigDict

from coderpad.json_types import JsonValue


class _QuestionModel(BaseModel):
    """Strict save payload fields for the Screen library."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
    )


@beartype
class ScreenRubricCriterionInput(_QuestionModel):
    """Typed rubric criterion input accepted when saving a question."""

    label: dict[str, str] | None = None
    skill: str | None = None
    points: int | None = None
    weight: int | None = None
    review_mode: (
        Literal["HUMAN_ONLY", "AI_SUGGESTIONS", "AI_GRADING"] | None
    ) = None
    description: str | None = None


@beartype
class ScreenRubricInput(_QuestionModel):
    """Typed rubric input accepted when saving a question."""

    criteria: list[ScreenRubricCriterionInput] | None = None


@beartype
class ScreenValidationCodeTestCaseInput(_QuestionModel):
    """Typed validation code test case input accepted when saving a
    question.
    """

    label: dict[str, str] | None = None
    test_identifier: str | None = None
    skill: str | None = None
    points: int | None = None
    weight: int | None = None
    difficulty: int | None = None
    contributes_to_score: bool | None = None
    visible_to_candidate: bool | None = None


@beartype
class ScreenValidationCodeInput(_QuestionModel):
    """Typed validation code input accepted when saving a question."""

    test_cases: list[ScreenValidationCodeTestCaseInput] | None = None


@beartype
class ScreenInputOutputTestCaseInput(_QuestionModel):
    """Typed input output test case input accepted when saving a
    question.
    """

    label: dict[str, str] | None = None
    input: str | None = None
    output: str | None = None
    skill: str | None = None
    points: int | None = None
    weight: int | None = None
    difficulty: int | None = None
    contributes_to_score: bool | None = None
    visible_to_candidate: bool | None = None
    timeout_ms_by_programming_language_id: dict[str, int] | None = None


@beartype
class ScreenInputOutputEvaluationInput(_QuestionModel):
    """Typed input output input accepted when saving a question."""

    test_cases: list[ScreenInputOutputTestCaseInput] | None = None


@beartype
class ScreenQueryComparisonRulesInput(_QuestionModel):
    """Typed query comparison rules input accepted when saving a
    question.
    """

    row_order_matters: bool | None = None
    column_order_matters: bool | None = None
    compare_all_tables: bool | None = None


@beartype
class ScreenSQLQueryResultComparisonInput(_QuestionModel):
    """Typed SQL query result comparison input accepted when saving a
    question.
    """

    reference_query: str | None = None
    comparison: ScreenQueryComparisonRulesInput | None = None


@beartype
class ScreenEvaluationAcceptedAnswerInput(_QuestionModel):
    """Typed evaluation accepted answer input accepted when saving a
    question.
    """

    value: str | None = None
    match_type: Literal["EXACT", "REGEX"] | None = None


@beartype
class ScreenTextAnswerMatchingInput(_QuestionModel):
    """Typed text answer matching input accepted when saving a
    question.
    """

    accepted_answers: list[ScreenEvaluationAcceptedAnswerInput] | None = None


@beartype
class ScreenChoiceSelectionInput(_QuestionModel):
    """Typed choice selection input accepted when saving a question."""

    correct_choice_indexes: list[int] | None = None


@beartype
class ScreenEvaluationInput(_QuestionModel):
    """Typed evaluation input accepted when saving a question."""

    rubric: ScreenRubricInput | None = None
    validation_code: ScreenValidationCodeInput | None = None
    input_output: ScreenInputOutputEvaluationInput | None = None
    sql_query_result_comparison: ScreenSQLQueryResultComparisonInput | None = (
        None
    )
    text_answer_matching: ScreenTextAnswerMatchingInput | None = None
    choice_selection: ScreenChoiceSelectionInput | None = None


@beartype
class ScreenEnvironmentInput(_QuestionModel):
    """Typed environment input accepted when saving a question."""

    version: str | None = None
    environment_id: str | None = None


@beartype
class ScreenDatabaseEngineInput(_QuestionModel):
    """Typed database engine input accepted when saving a question."""

    version: str | None = None
    engine_id: str | None = None


@beartype
class ScreenFunctionSignatureInput(_QuestionModel):
    """Typed function signature input accepted when saving a question."""

    name: str | None = None
    parameters: list[dict[str, JsonValue]] | None = None
    return_type: dict[str, JsonValue] | None = None


@beartype
class ScreenPossibleSolutionInput(_QuestionModel):
    """Typed possible solution input accepted when saving a question."""

    code: str | None = None
    programming_language_id: str | None = None


@beartype
class ScreenCodeInput(_QuestionModel):
    """Typed code input accepted when saving a question."""

    environment: ScreenEnvironmentInput | None = None
    mode: Literal["SINGLE_LANGUAGE", "MULTI_LANGUAGE"] | None = None
    programming_language_id: str | None = None
    candidate_test_code: str | None = None
    validator_code: str | None = None
    timeout_ms: int | None = None
    database_engine: ScreenDatabaseEngineInput | None = None
    database_setup_script: str | None = None
    starter_code: str | None = None
    function_signature: ScreenFunctionSignatureInput | None = None
    possible_solution: ScreenPossibleSolutionInput | None = None
    show_function_signature_in_statement: bool | None = None


@beartype
class ScreenQuestionChoiceInput(_QuestionModel):
    """Typed question choice input accepted when saving a question."""

    label: dict[str, str] | None = None


@beartype
class ScreenMCQInput(_QuestionModel):
    """Typed multiple choice input accepted when saving a question."""

    choices: list[ScreenQuestionChoiceInput] | None = None
    selection_mode: Literal["SINGLE", "MULTIPLE"] | None = None
    randomize_choices: bool | None = None


@beartype
class ScreenTextInput(_QuestionModel):
    """Typed text input accepted when saving a question."""

    evaluation_mode: Literal["MANUAL", "AUTOMATIC"] | None = None


@beartype
class ScreenVideoInput(_QuestionModel):
    """Typed video input accepted when saving a question."""

    recording_media: Literal["VIDEO", "AUDIO"] | None = None


@beartype
class ScreenProjectResourceInput(_QuestionModel):
    """Typed project resource input accepted when saving a question."""

    version: str | None = None
    resource_id: str | None = None


@beartype
class ScreenProjectInput(_QuestionModel):
    """Typed project input accepted when saving a question."""

    environment: ScreenEnvironmentInput | None = None
    resources: list[ScreenProjectResourceInput] | None = None
    ai_assist_additional_instructions: str | None = None
    ai_assist_allowed: bool | None = None
    temporary_file_id: str | None = None


@beartype
class ScreenQuestionSave(_QuestionModel):
    """Writable fields for creating or updating a Screen question."""

    type: Literal["MCQ", "CODE", "TEXT", "FILE_UPLOAD", "VIDEO", "PROJECT"]
    domain: str | None = None
    duration_seconds: int | None = None
    difficulty: Literal["EASY", "MEDIUM", "HARD"] | None = None
    points: int | None = None
    title: dict[str, str] | None = None
    statement: dict[str, str] | None = None
    locales: list[str] | None = None
    skill: str | None = None
    team_id: str | None = None
    automatically_selectable: bool | None = None
    comment: str | None = None
    evaluation: ScreenEvaluationInput | None = None
    code_details: ScreenCodeInput | None = None
    mcq_details: ScreenMCQInput | None = None
    text_details: ScreenTextInput | None = None
    video_details: ScreenVideoInput | None = None
    project_details: ScreenProjectInput | None = None
