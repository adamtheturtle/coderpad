"""Tests for the CoderPad types."""

from coderpad_api import PadEnvironment


class TestPadEnvironment:
    """Tests for ``PadEnvironment``."""

    @staticmethod
    def test_from_dict() -> None:
        """A PadEnvironment can be created from a dictionary."""
        data = {
            "id": 1,
            "pad_id": 2,
            "question_id": None,
            "example_question_id": None,
            "language": "python",
            "file_contents": [
                {
                    "path": "main.py",
                    "contents": "",
                    "history": "",
                },
            ],
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
        }
        result = PadEnvironment.from_dict(data=data)
        assert result.id == 1
        assert result.language == "python"
        assert len(result.file_contents) == 1
