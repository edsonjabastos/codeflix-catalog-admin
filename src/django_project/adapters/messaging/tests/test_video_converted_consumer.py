"""
Unit tests for VideoConvertedRabbitMQConsumer.on_message method.
"""
import json
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from core.video.application.use_cases.process_audio_video_media import (
    ProcessAudioVideoMedia,
)
from core.video.domain.value_objects import MediaStatus, MediaType
from django_project.adapters.messaging.video_converted_consumer import (
    VideoConvertedRabbitMQConsumer,
)


@pytest.fixture
def mock_use_case() -> MagicMock:
    return MagicMock(spec=ProcessAudioVideoMedia)


@pytest.fixture
def consumer(mock_use_case: MagicMock) -> VideoConvertedRabbitMQConsumer:
    return VideoConvertedRabbitMQConsumer(
        use_case=mock_use_case,
        host="localhost",
        queue="videos.converted",
    )


class TestVideoConvertedRabbitMQConsumerOnMessage:
    def test_on_message_parses_video_message_and_calls_use_case(
        self,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
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

        consumer.on_message(message_bytes)

        mock_use_case.execute.assert_called_once()
        input_data: ProcessAudioVideoMedia.Input = mock_use_case.execute.call_args.kwargs[
            "request"
        ]

        assert input_data.video_id == video_id
        assert input_data.media_type == MediaType.VIDEO
        assert input_data.encoded_location == encoded_location
        assert input_data.status == MediaStatus.COMPLETED

    def test_on_message_parses_trailer_message_correctly(
        self,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
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

        consumer.on_message(message_bytes)

        input_data: ProcessAudioVideoMedia.Input = mock_use_case.execute.call_args.kwargs[
            "request"
        ]

        assert input_data.video_id == video_id
        assert input_data.media_type == MediaType.TRAILER
        assert input_data.encoded_location == encoded_location
        assert input_data.status == MediaStatus.COMPLETED

    def test_on_message_handles_error_status(
        self,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
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

        consumer.on_message(message_bytes)

        input_data: ProcessAudioVideoMedia.Input = mock_use_case.execute.call_args.kwargs[
            "request"
        ]

        assert input_data.status == MediaStatus.ERROR
        assert input_data.encoded_location == ""

    @patch("django_project.adapters.messaging.video_converted_consumer.logger")
    def test_on_message_with_error_field_does_not_call_use_case(
        self,
        mock_logger: MagicMock,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
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

        consumer.on_message(message_bytes)

        mock_use_case.execute.assert_not_called()
        mock_logger.error.assert_called_once()
        log_message = mock_logger.error.call_args[0][0]
        assert str(video_id) in log_message
        assert error_msg in log_message

    @patch("django_project.adapters.messaging.video_converted_consumer.logger")
    def test_on_message_with_invalid_json_logs_error(
        self,
        mock_logger: MagicMock,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        consumer.on_message(b"not valid json")

        mock_use_case.execute.assert_not_called()
        mock_logger.error.assert_called_once()

    @patch("django_project.adapters.messaging.video_converted_consumer.logger")
    def test_on_message_with_missing_keys_logs_error(
        self,
        mock_logger: MagicMock,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        message = {
            "error": "",
            "status": "COMPLETED",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        consumer.on_message(message_bytes)

        mock_use_case.execute.assert_not_called()
        mock_logger.error.assert_called_once()

    @patch("django_project.adapters.messaging.video_converted_consumer.logger")
    def test_on_message_with_invalid_uuid_logs_error(
        self,
        mock_logger: MagicMock,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
        message = {
            "error": "",
            "video": {
                "resource_id": "not-a-valid-uuid.VIDEO",
                "encoded_video_folder": "/encoded/videos/output.mp4",
            },
            "status": "COMPLETED",
        }
        message_bytes = json.dumps(message).encode("utf-8")

        consumer.on_message(message_bytes)

        mock_use_case.execute.assert_not_called()
        mock_logger.error.assert_called_once()

    @patch("django_project.adapters.messaging.video_converted_consumer.logger")
    def test_on_message_with_invalid_media_type_logs_error(
        self,
        mock_logger: MagicMock,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
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

        consumer.on_message(message_bytes)

        mock_use_case.execute.assert_not_called()
        mock_logger.error.assert_called_once()

    @patch("django_project.adapters.messaging.video_converted_consumer.logger")
    def test_on_message_with_invalid_status_logs_error(
        self,
        mock_logger: MagicMock,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
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

        consumer.on_message(message_bytes)

        mock_use_case.execute.assert_not_called()
        mock_logger.error.assert_called_once()

    def test_on_message_handles_processing_status(
        self,
        mock_use_case: MagicMock,
        consumer: VideoConvertedRabbitMQConsumer,
    ) -> None:
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

        consumer.on_message(message_bytes)

        input_data: ProcessAudioVideoMedia.Input = mock_use_case.execute.call_args.kwargs[
            "request"
        ]

        assert input_data.status == MediaStatus.PROCESSING
