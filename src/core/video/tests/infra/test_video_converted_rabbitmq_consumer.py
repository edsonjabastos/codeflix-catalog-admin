"""
Unit tests for VideoConvertedRabbitMQConsumer.on_message method.

Tests that the consumer properly:
1. Parses incoming byte messages
2. Converts them to proper ProcessAudioVideoMedia.Input
3. Calls the use case correctly
4. Handles error messages appropriately
"""
import json
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from core.video.application.use_cases.process_audio_video_media import (
    ProcessAudioVideoMedia,
)
from core.video.domain.value_objects import MediaStatus, MediaType
from core.video.infra.video_converted_rabbitmq_consumer import (
    VideoConvertedRabbitMQConsumer,
)


@pytest.fixture
def consumer() -> VideoConvertedRabbitMQConsumer:
    return VideoConvertedRabbitMQConsumer(host="localhost", queue="videos.converted")


@pytest.fixture
def valid_video_message() -> dict:
    """Creates a valid video conversion completed message."""
    video_id = str(uuid4())
    return {
        "error": "",
        "video": {
            "resource_id": f"{video_id}.VIDEO",
            "encoded_video_folder": "/encoded/videos/output.mp4",
        },
        "status": "COMPLETED",
    }


@pytest.fixture
def valid_trailer_message() -> dict:
    """Creates a valid trailer conversion completed message."""
    video_id = str(uuid4())
    return {
        "error": "",
        "video": {
            "resource_id": f"{video_id}.TRAILER",
            "encoded_video_folder": "/encoded/trailers/output.mp4",
        },
        "status": "COMPLETED",
    }


@pytest.fixture
def error_message() -> dict:
    """Creates an error message from the video converter."""
    video_id = str(uuid4())
    return {
        "error": "Encoding failed: invalid codec",
        "message": {
            "resource_id": f"{video_id}.VIDEO",
        },
        "status": "ERROR",
    }


class TestVideoConvertedRabbitMQConsumerOnMessage:
    """Tests for the on_message method."""

    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_parses_video_message_and_calls_use_case(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange
        video_id = uuid4()
        encoded_location = "/encoded/videos/output.mp4"
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.VIDEO",
                "encoded_video_folder": encoded_location,
            },
            "status": "COMPLETED",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        mock_repository = MagicMock()
        mock_repository_class.return_value = mock_repository

        # Act
        consumer.on_message(message_bytes)

        # Assert
        mock_repository_class.assert_called_once()
        mock_execute.assert_called_once()

        # Verify the input passed to execute
        call_args = mock_execute.call_args
        input_data: ProcessAudioVideoMedia.Input = call_args.kwargs["request"]

        assert input_data.video_id == video_id
        assert input_data.media_type == MediaType.VIDEO
        assert input_data.encoded_location == encoded_location
        assert input_data.status == MediaStatus.COMPLETED

    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_parses_trailer_message_correctly(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange
        video_id = uuid4()
        encoded_location = "/encoded/trailers/output.mp4"
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.TRAILER",
                "encoded_video_folder": encoded_location,
            },
            "status": "COMPLETED",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        mock_repository = MagicMock()
        mock_repository_class.return_value = mock_repository

        # Act
        consumer.on_message(message_bytes)

        # Assert
        call_args = mock_execute.call_args
        input_data: ProcessAudioVideoMedia.Input = call_args.kwargs["request"]

        assert input_data.video_id == video_id
        assert input_data.media_type == MediaType.TRAILER
        assert input_data.encoded_location == encoded_location
        assert input_data.status == MediaStatus.COMPLETED

    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_handles_error_status(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange
        video_id = uuid4()
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.VIDEO",
                "encoded_video_folder": "",
            },
            "status": "ERROR",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        mock_repository = MagicMock()
        mock_repository_class.return_value = mock_repository

        # Act
        consumer.on_message(message_bytes)

        # Assert
        call_args = mock_execute.call_args
        input_data: ProcessAudioVideoMedia.Input = call_args.kwargs["request"]

        assert input_data.status == MediaStatus.ERROR
        assert input_data.encoded_location == ""

    @patch("core.video.infra.video_converted_rabbitmq_consumer.logger")
    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_with_error_field_does_not_call_use_case(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        mock_logger: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange
        video_id = uuid4()
        error_msg = "Encoding failed: invalid codec"
        message = {
            "error": error_msg,
            "message": {
                "resource_id": f"{video_id}.VIDEO",
            },
            "status": "ERROR",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        # Act
        consumer.on_message(message_bytes)

        # Assert - use case should NOT be called when error is present
        mock_repository_class.assert_not_called()
        mock_execute.assert_not_called()

        # Verify error was logged
        mock_logger.error.assert_called_once()
        log_message = mock_logger.error.call_args[0][0]
        assert str(video_id) in log_message
        assert error_msg in log_message

    @patch("core.video.infra.video_converted_rabbitmq_consumer.logger")
    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_with_invalid_json_logs_error(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        mock_logger: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange
        invalid_message = b"not valid json"

        # Act
        consumer.on_message(invalid_message)

        # Assert - use case should NOT be called
        mock_repository_class.assert_not_called()
        mock_execute.assert_not_called()

        # Verify error was logged
        mock_logger.error.assert_called_once()

    @patch("core.video.infra.video_converted_rabbitmq_consumer.logger")
    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_with_missing_keys_logs_error(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        mock_logger: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange - message missing required "video" key
        message = {
            "error": "",
            "status": "COMPLETED",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        # Act
        consumer.on_message(message_bytes)

        # Assert - use case should NOT be called
        mock_repository_class.assert_not_called()
        mock_execute.assert_not_called()

        # Verify error was logged
        mock_logger.error.assert_called_once()

    @patch("core.video.infra.video_converted_rabbitmq_consumer.logger")
    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_with_invalid_uuid_logs_error(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        mock_logger: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange
        message = {
            "error": "",
            "video": {
                "resource_id": "not-a-valid-uuid.VIDEO",
                "encoded_video_folder": "/encoded/videos/output.mp4",
            },
            "status": "COMPLETED",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        # Act
        consumer.on_message(message_bytes)

        # Assert - use case should NOT be called
        mock_repository_class.assert_not_called()
        mock_execute.assert_not_called()

        # Verify error was logged
        mock_logger.error.assert_called_once()

    @patch("core.video.infra.video_converted_rabbitmq_consumer.logger")
    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_with_invalid_media_type_logs_error(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        mock_logger: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange
        video_id = uuid4()
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.INVALID_TYPE",
                "encoded_video_folder": "/encoded/videos/output.mp4",
            },
            "status": "COMPLETED",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        # Act
        consumer.on_message(message_bytes)

        # Assert - use case should NOT be called
        mock_repository_class.assert_not_called()
        mock_execute.assert_not_called()

        # Verify error was logged
        mock_logger.error.assert_called_once()

    @patch("core.video.infra.video_converted_rabbitmq_consumer.logger")
    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_with_invalid_status_logs_error(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        mock_logger: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange
        video_id = uuid4()
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.VIDEO",
                "encoded_video_folder": "/encoded/videos/output.mp4",
            },
            "status": "INVALID_STATUS",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        # Act
        consumer.on_message(message_bytes)

        # Assert - use case should NOT be called
        mock_repository_class.assert_not_called()
        mock_execute.assert_not_called()

        # Verify error was logged
        mock_logger.error.assert_called_once()

    @patch(
        "core.video.infra.video_converted_rabbitmq_consumer.DjangoORMVideoRepository"
    )
    @patch.object(ProcessAudioVideoMedia, "execute")
    def test_on_message_handles_processing_status(
        self,
        mock_execute: MagicMock,
        mock_repository_class: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        # Arrange
        video_id = uuid4()
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_id}.VIDEO",
                "encoded_video_folder": "",
            },
            "status": "PROCESSING",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        mock_repository = MagicMock()
        mock_repository_class.return_value = mock_repository

        # Act
        consumer.on_message(message_bytes)

        # Assert
        call_args = mock_execute.call_args
        input_data: ProcessAudioVideoMedia.Input = call_args.kwargs["request"]

        assert input_data.status == MediaStatus.PROCESSING
