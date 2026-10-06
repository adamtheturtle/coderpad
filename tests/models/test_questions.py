"""Tests for `coderpad` questions models."""

from coderpad._dict_types import (
    CandidateInstructionDict,
    CustomDatabaseDict,
    CustomFileDict,
    QuestionDict,
    TestCaseDict,
)
from coderpad.types import (
    CandidateInstruction,
    CustomDatabase,
    CustomFile,
    Question,
    TestCase,
)


def _candidate_instruction_dict() -> CandidateInstructionDict:
    """Sample CandidateInstructionDict."""
    return {"instructions": "Do the thing", "default_visible": True}


def _test_case_dict() -> TestCaseDict:
    """Sample TestCaseDict."""
    return {
        "id": 10,
        "return_value": "42",
        "visible": True,
        "arguments": ["1", "2"],
    }


def _custom_file_dict() -> CustomFileDict:
    """Sample CustomFileDict."""
    return {
        "id": "cf-1",
        "title": "Data",
        "description": "Test data",
        "filename": "data.csv",
        "filesize": "1024",
    }


def _custom_database_dict() -> CustomDatabaseDict:
    """Sample CustomDatabaseDict."""
    return {
        "id": 12,
        "title": "Products",
        "description": "Product catalog",
        "language": "postgresql",
        "schema": "CREATE TABLE products (id integer);",
        "schema_json": {
            "arrangement": "horizontal",
            "tables": [
                {
                    "name": "products",
                    "columns": [
                        {
                            "name": "id",
                            "type": "integer",
                            "pk": True,
                            "nn": True,
                        },
                    ],
                },
            ],
        },
    }


_PUBLIC_TAKE_HOME_SETTING_ID = 7


def _question_dict() -> QuestionDict:
    """Sample QuestionDict."""
    return {
        "id": 5,
        "title": "FizzBuzz",
        "owner_email": "owner@example.com",
        "language": "python",
        "description": "Write FizzBuzz",
        "candidate_instructions": [_candidate_instruction_dict()],
        "contents": "def fizzbuzz(): ...",
        "shared": False,
        "used": 3,
        "take_home": False,
        "test_cases_enabled": True,
        "solution": "def fizzbuzz(): pass",
        "pad_type": "standard",
        "is_draft": False,
        "author_name": "Author",
        "organization_name": "Org",
        "custom_files": [_custom_file_dict()],
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
        "public_take_home_setting_id": _PUBLIC_TAKE_HOME_SETTING_ID,
        "contents_for_test_cases": "test code",
        "test_cases": [_test_case_dict()],
        "custom_database": _custom_database_dict(),
        "ai_assist_custom_system_prompt": "Only provide hints.",
    }


def test_candidate_instruction_from_dict() -> None:
    """A CandidateInstruction can be created from a dictionary."""
    data = _candidate_instruction_dict()
    result = CandidateInstruction.from_dict(data=data)
    assert result.instructions == data["instructions"]
    assert result.default_visible is True


def test_model_validate_normalizes_null_visibility() -> None:
    """Pydantic parsing retains legacy null visibility handling."""
    result = CandidateInstruction.model_validate(
        obj={"instructions": "Do the thing", "default_visible": None},
    )
    assert result.default_visible is False


def test_test_case_from_dict() -> None:
    """A TestCase can be created from a dictionary."""
    data = _test_case_dict()
    result = TestCase.from_dict(data=data)
    assert result.id == data["id"]
    assert result.return_value == data["return_value"]
    assert result.visible == data["visible"]
    assert result.arguments == data["arguments"]


def test_custom_file_from_dict() -> None:
    """A CustomFile can be created from a dictionary."""
    data = _custom_file_dict()
    result = CustomFile.from_dict(data=data)
    assert result.id == data["id"]
    assert result.title == data["title"]
    assert result.description == data["description"]
    assert result.filename == data["filename"]
    assert result.filesize == data["filesize"]


def test_question_from_dict() -> None:
    """A Question can be created from a dictionary."""
    data = _question_dict()
    result = Question.from_dict(data=data)
    assert result.id == data["id"]
    assert result.title == data["title"]
    assert result.owner_email == data["owner_email"]
    assert result.language == data["language"]
    assert result.description == data["description"]
    assert len(result.candidate_instructions) == len(
        data["candidate_instructions"],
    )
    assert result.contents == data["contents"]
    assert result.shared == data["shared"]
    assert result.used == data["used"]
    assert result.take_home == data["take_home"]
    assert result.test_cases_enabled == data["test_cases_enabled"]
    assert result.solution == data["solution"]
    assert result.pad_type == data["pad_type"]
    assert result.is_draft == data["is_draft"]
    assert result.author_name == data["author_name"]
    assert result.organization_name == data["organization_name"]
    assert len(result.custom_files) == len(data["custom_files"])
    assert result.created_at == data["created_at"]
    assert result.updated_at == data["updated_at"]
    assert result.public_take_home_setting_id == _PUBLIC_TAKE_HOME_SETTING_ID
    assert result.contents_for_test_cases == "test code"
    assert result.test_cases is not None
    assert len(result.test_cases) == 1
    assert result.custom_database is not None
    assert result.custom_database.title == "Products"
    assert result.custom_database.schema_json.tables[0].columns[0].pk
    assert result.ai_assist_custom_system_prompt == "Only provide hints."


def test_model_validate_without_optional_fields() -> None:
    """Pydantic parsing accepts omitted optional response fields."""
    payload: dict[str, object] = dict(_question_dict())
    for field_name in (
        "language",
        "description",
        "contents",
        "solution",
        "public_take_home_setting_id",
        "contents_for_test_cases",
        "test_cases",
        "custom_database",
        "ai_assist_custom_system_prompt",
    ):
        _ = payload.pop(field_name)
    payload["candidate_instructions"] = [
        {"instructions": "Do the thing", "default_visible": None},
    ]

    result = Question.model_validate(obj=payload)

    assert result.language is None
    assert result.solution is None
    assert result.candidate_instructions[0].default_visible is False


def test_from_dict_with_null_ai_assist_custom_system_prompt() -> None:
    """A Question can have no custom AI Assist system prompt."""
    data = _question_dict()
    data["ai_assist_custom_system_prompt"] = None
    result = Question.from_dict(data=data)
    assert result.ai_assist_custom_system_prompt is None


def test_from_dict_without_ai_assist_custom_system_prompt() -> None:
    """A Question can omit its custom AI Assist system prompt."""
    data = _question_dict()
    del data["ai_assist_custom_system_prompt"]
    result = Question.from_dict(data=data)
    assert result.ai_assist_custom_system_prompt is None


def test_from_dict_without_custom_database() -> None:
    """A Question can omit its empirically observed custom
    database.
    """
    data = _question_dict()
    del data["custom_database"]
    result = Question.from_dict(data=data)
    assert result.custom_database is None


def test_custom_database_from_dict() -> None:
    """A custom database can be created from a dictionary."""
    data = _custom_database_dict()
    result = CustomDatabase.from_dict(data=data)
    assert result.id == data["id"]
    # This API field intentionally shadows a deprecated Pydantic method;
    # the model instance contains the response string at runtime.
    assert result.schema == data["schema"]  # pylint: disable=comparison-with-callable
    assert result.schema_json.arrangement == "horizontal"
    assert result.schema_json.tables[0].name == "products"
    assert result.schema_json.tables[0].columns[0].nn


def test_candidate_instruction_name() -> None:
    """Step names retain their exact text, including empty names."""
    for name in [None, "", "Part one"]:
        instruction = CandidateInstruction.from_dict(
            data={"instructions": "Do the thing", "name": name}
        )
        assert instruction.name == name
    assert (
        CandidateInstruction.from_dict(data={"instructions": "Do it"}).name
        is None
    )
