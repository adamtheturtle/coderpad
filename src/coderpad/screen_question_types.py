"""Typed Screen question library responses."""

from typing import ClassVar, Literal

from beartype import beartype
from pydantic import BaseModel, ConfigDict

from coderpad.json_types import JsonValue
from coderpad.screen_types import ScreenPagination


class _QuestionModel(BaseModel):
    """Strict immutable response fields for the Screen library."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        strict=True,
        extra="ignore",
    )


@beartype
class ScreenQuestionSummary(_QuestionModel):
    """Typed question summary returned by the question library."""

    id: str
    version: int | None = None
    title: dict[str, str] | None = None
    type: (
        Literal[
            "MCQ",
            "CODE",
            "TEXT",
            "MULTI",
            "GAME",
            "CLASH",
            "COURSE",
            "FILE_UPLOAD",
            "PROJECT",
            "VIDEO",
        ]
        | None
    ) = None
    difficulty: Literal["EASY", "MEDIUM", "HARD"] | None = None
    domain: str | None = None
    skill: str | None = None
    product: Literal["SCREEN", "QUALIFY"] | None = None
    duration_seconds: int | None = None
    programming_language_id: str | None = None
    modification_time: str | None = None
    from_coderpad_question_bank: bool | None = None


@beartype
class ScreenQuestionResourceDetails(_QuestionModel):
    """Typed question resource details returned by the question
    library.
    """

    filename: str | None = None
    mime_type: str | None = None
    download_url: str | None = None


@beartype
class ScreenRubricCriterionDetails(_QuestionModel):
    """Typed rubric criterion details returned by the question library."""

    label: dict[str, str] | None = None
    skill: str | None = None
    points: int | None = None
    weight: int | None = None
    review_mode: (
        Literal["HUMAN_ONLY", "AI_SUGGESTIONS", "AI_GRADING"] | None
    ) = None
    description: str | None = None


@beartype
class ScreenRubricDetails(_QuestionModel):
    """Typed rubric details returned by the question library."""

    criteria: list[ScreenRubricCriterionDetails] | None = None


@beartype
class ScreenTestReportTestCaseDetails(_QuestionModel):
    """Typed test report test case details returned by the question
    library.
    """

    key: str | None = None
    test_identifier: str | None = None
    label: dict[str, str] | None = None
    skill: str | None = None
    points: int | None = None
    weight: int | None = None


@beartype
class ScreenTestReportDetails(_QuestionModel):
    """Typed test report details returned by the question library."""

    test_cases: list[ScreenTestReportTestCaseDetails] | None = None


@beartype
class ScreenValidationCodeTestCaseDetails(_QuestionModel):
    """Typed validation code test case details returned by the question
    library.
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
class ScreenValidationCodeDetails(_QuestionModel):
    """Typed validation code details returned by the question library."""

    test_cases: list[ScreenValidationCodeTestCaseDetails] | None = None


@beartype
class ScreenInputOutputTestCaseDetails(_QuestionModel):
    """Typed input output test case details returned by the question
    library.
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
class ScreenInputOutputDetails(_QuestionModel):
    """Typed input output details returned by the question library."""

    test_cases: list[ScreenInputOutputTestCaseDetails] | None = None


@beartype
class ScreenQueryComparisonRulesDetails(_QuestionModel):
    """Typed query comparison rules details returned by the question
    library.
    """

    row_order_matters: bool | None = None
    column_order_matters: bool | None = None
    compare_all_tables: bool | None = None


@beartype
class ScreenSQLQueryResultComparisonDetails(_QuestionModel):
    """Typed SQL query result comparison details returned by the question
    library.
    """

    reference_query: str | None = None
    comparison: ScreenQueryComparisonRulesDetails | None = None


@beartype
class ScreenEvaluationAcceptedAnswerDetails(_QuestionModel):
    """Typed evaluation accepted answer details returned by the question
    library.
    """

    value: str | None = None
    match_type: Literal["EXACT", "REGEX"] | None = None


@beartype
class ScreenTextAnswerMatchingDetails(_QuestionModel):
    """Typed text answer matching details returned by the question library."""

    accepted_answers: list[ScreenEvaluationAcceptedAnswerDetails] | None = None


@beartype
class ScreenChoiceSelectionDetails(_QuestionModel):
    """Typed choice selection details returned by the question library."""

    correct_choice_indexes: list[int] | None = None


@beartype
class ScreenEvaluationDetails(_QuestionModel):
    """Typed evaluation details returned by the question library."""

    rubric: ScreenRubricDetails | None = None
    test_report: ScreenTestReportDetails | None = None
    validation_code: ScreenValidationCodeDetails | None = None
    input_output: ScreenInputOutputDetails | None = None
    sql_query_result_comparison: (
        ScreenSQLQueryResultComparisonDetails | None
    ) = None
    text_answer_matching: ScreenTextAnswerMatchingDetails | None = None
    choice_selection: ScreenChoiceSelectionDetails | None = None


@beartype
class ScreenQuestionChoiceDetails(_QuestionModel):
    """Typed question choice details returned by the question library."""

    label: dict[str, str] | None = None


@beartype
class ScreenMCQDetails(_QuestionModel):
    """Typed multiple choice details returned by the question library."""

    choices: list[ScreenQuestionChoiceDetails] | None = None
    selection_mode: Literal["SINGLE", "MULTIPLE"] | None = None
    randomize_choices: bool | None = None


@beartype
class ScreenEnvironmentDetails(_QuestionModel):
    """Typed environment details returned by the question library."""

    version: str | None = None
    environment_id: str | None = None


@beartype
class ScreenDatabaseEngineDetails(_QuestionModel):
    """Typed database engine details returned by the question library."""

    version: str | None = None
    engine_id: str | None = None


@beartype
class ScreenFunctionSignatureDetails(_QuestionModel):
    """Typed function signature details returned by the question
    library.
    """

    name: str | None = None
    parameters: list[dict[str, JsonValue]] | None = None
    return_type: dict[str, JsonValue] | None = None


@beartype
class ScreenPossibleSolutionDetails(_QuestionModel):
    """Typed possible solution details returned by the question
    library.
    """

    code: str | None = None
    programming_language_id: str | None = None


@beartype
class ScreenCodeDetails(_QuestionModel):
    """Typed code details returned by the question library."""

    environment: ScreenEnvironmentDetails | None = None
    mode: Literal["SINGLE_LANGUAGE", "MULTI_LANGUAGE"] | None = None
    programming_language_id: str | None = None
    candidate_test_code: str | None = None
    validator_code: str | None = None
    timeout_ms: int | None = None
    database_engine: ScreenDatabaseEngineDetails | None = None
    database_setup_script: str | None = None
    starter_code: str | None = None
    function_signature: ScreenFunctionSignatureDetails | None = None
    possible_solution: ScreenPossibleSolutionDetails | None = None
    show_function_signature_in_statement: bool | None = None
    available_programming_language_ids: list[str] | None = None


@beartype
class ScreenGameDetails(_QuestionModel):
    """Typed game details returned by the question library."""

    available_programming_language_ids: list[str] | None = None


@beartype
class ScreenTextDetails(_QuestionModel):
    """Typed text details returned by the question library."""

    evaluation_mode: Literal["MANUAL", "AUTOMATIC"] | None = None


@beartype
class ScreenFileUploadDetails(_QuestionModel):
    """Typed file upload details returned by the question library."""

    download_url: str | None = None


@beartype
class ScreenVideoDetails(_QuestionModel):
    """Typed video details returned by the question library."""

    recording_media: Literal["VIDEO", "AUDIO"] | None = None


@beartype
class ScreenProjectResourceDetails(_QuestionModel):
    """Typed project resource details returned by the question library."""

    version: str | None = None
    resource_id: str | None = None


@beartype
class ScreenProjectDetails(_QuestionModel):
    """Typed project details returned by the question library."""

    environment: ScreenEnvironmentDetails | None = None
    resources: list[ScreenProjectResourceDetails] | None = None
    ai_assist_additional_instructions: str | None = None
    ai_assist_allowed: bool | None = None
    download_url: str | None = None


@beartype
class ScreenQuestionDetails(_QuestionModel):
    """Typed question details returned by the question library."""

    id: str
    version: int | None = None
    type: (
        Literal[
            "MCQ",
            "CODE",
            "TEXT",
            "MULTI",
            "GAME",
            "CLASH",
            "COURSE",
            "FILE_UPLOAD",
            "PROJECT",
            "VIDEO",
        ]
        | None
    ) = None
    domain: str | None = None
    difficulty: Literal["EASY", "MEDIUM", "HARD"] | None = None
    points: int | None = None
    title: dict[str, str] | None = None
    statement: dict[str, str] | None = None
    locales: list[str] | None = None
    skill: str | None = None
    resources: list[ScreenQuestionResourceDetails] | None = None
    comment: str | None = None
    evaluation: ScreenEvaluationDetails | None = None
    duration_seconds: int | None = None
    creation_time: str | None = None
    modification_time: str | None = None
    from_coderpad_question_bank: bool | None = None
    team_id: str | None = None
    automatically_selectable: bool | None = None
    mcq_details: ScreenMCQDetails | None = None
    code_details: ScreenCodeDetails | None = None
    game_details: ScreenGameDetails | None = None
    text_details: ScreenTextDetails | None = None
    file_upload_details: ScreenFileUploadDetails | None = None
    video_details: ScreenVideoDetails | None = None
    project_details: ScreenProjectDetails | None = None


@beartype
class ScreenQuestionsPage(_QuestionModel):
    """An offset page of lightweight question summaries."""

    questions: list[ScreenQuestionSummary]
    pagination: ScreenPagination | None = None


@beartype
class ScreenCreatedQuestion(_QuestionModel):
    """Created question details and the response Location header."""

    question: ScreenQuestionDetails
    location: str | None = None


@beartype
class ScreenQuestionFilters(_QuestionModel):
    """Optional filters and ordering for every question library page."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True, strict=True, extra="forbid"
    )

    type: str | None = None
    duration_seconds_min: int | None = None
    duration_seconds_max: int | None = None
    difficulty: Literal["EASY", "MEDIUM", "HARD"] | None = None
    domain: str | None = None
    skill: str | None = None
    programming_language: str | None = None
    from_coderpad_question_bank: bool | None = None
    product: Literal["SCREEN", "QUALIFY"] | None = None
    sort: (
        Literal[
            "id",
            "title",
            "type",
            "duration_seconds",
            "difficulty",
            "domain",
            "skill",
            "programming_language",
            "modification_time",
            "from_coderpad_question_bank",
            "product",
        ]
        | None
    ) = None
    order: Literal["asc", "desc"] | None = None
