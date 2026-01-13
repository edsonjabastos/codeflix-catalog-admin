"""
End-to-end test for the complete video conversion flow:
1. Create Category, Genre, and CastMember via APIs
2. Create a Video via API
3. Upload video media file via API
4. Publish message to RabbitMQ videos.converted queue
5. Verify the video status is COMPLETED and video is published

IMPORTANT: This test requires the consumer to be running against the SAME database.
Since pytest-django creates a separate test database, this test needs special handling.

To run this test properly:
1. Start RabbitMQ: docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
2. Start the consumer: python manage.py startconsumer
3. Run the test: pytest tests_e2e/test_video_conversion_e2e.py -v -s
"""
import json
import os
import shutil
import time
from typing import Any
from uuid import UUID

import pika
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient


RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
VIDEOS_CONVERTED_QUEUE = "videos.converted"


def send_video_converted_message(
    video_id: str,
    media_type: str = "VIDEO",
    encoded_location: str = "/path/to/encoded/video",
    status: str = "COMPLETED",
    error: str = "",
) -> None:
    """
    Send a message to the videos.converted queue simulating
    a completed video encoding process.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
        ),
    )
    channel = connection.channel()
    channel.queue_declare(queue=VIDEOS_CONVERTED_QUEUE)

    message = {
        "error": error,
        "video": {
            "resource_id": f"{video_id}.{media_type}",
            "encoded_video_folder": encoded_location,
        },
        "status": status,
    }

    channel.basic_publish(
        exchange="",
        routing_key=VIDEOS_CONVERTED_QUEUE,
        body=json.dumps(message),
    )
    connection.close()


def wait_for_video_status(
    video_id: str,
    expected_status: str,
    timeout: int = 10,
    poll_interval: float = 0.5,
) -> bool:
    """
    Poll the database until the video media status matches the expected status
    or timeout is reached.

    Uses a fresh database connection each time to avoid stale data from
    transaction isolation.
    """
    from django.db import connection
    from django_project.video_app.models import Video as VideoORM

    start_time = time.time()
    while time.time() - start_time < timeout:
        # Close old connection to get fresh data
        connection.close()
        try:
            video = VideoORM.objects.get(id=video_id)
            if video.video and video.video.status == expected_status:
                return True
        except VideoORM.DoesNotExist:
            pass
        time.sleep(poll_interval)
    return False


def get_video_from_db(video_id: str):
    """Get video from database with a fresh connection."""
    from django.db import connection
    from django_project.video_app.models import Video as VideoORM

    connection.close()
    return VideoORM.objects.get(id=video_id)



class TestVideoConversionFlowRealDB:
    """
    End-to-end test for video conversion flow using the REAL database.
    
    This test bypasses pytest's test database to allow the external consumer
    to see the data created by the test.

    Prerequisites:
    - RabbitMQ server running
    - Consumer running: python manage.py startconsumer
    
    Run with: pytest tests_e2e/test_video_conversion_e2e.py::TestVideoConversionFlowRealDB -v -s
    """

    @pytest.fixture(autouse=True)
    def enable_db_access_for_all_tests(self, django_db_blocker):
        """
        Enable database access without using test database.
        This uses django_db_blocker to allow access to the real database.
        """
        # Unblock database access to use the real database
        with django_db_blocker.unblock():
            yield

    def test_complete_video_conversion_flow_real_db(self) -> None:
        """
        Test the complete video lifecycle using the real database.
        """
        import django
        from django.conf import settings
        
        # Force using the real database
        api_client: APIClient = APIClient()

        # API endpoints
        video_url: str = "/api/videos/"
        category_url: str = "/api/categories/"
        genre_url: str = "/api/genres/"
        cast_member_url: str = "/api/cast_members/"

        video_id: str | None = None
        category_id: str | None = None
        genre_id: str | None = None
        cast_member_id: str | None = None

        try:
            # ============================================================
            # Step 1: Create prerequisite entities
            # ============================================================

            # Create a Category
            category_data: dict[str, Any] = {
                "name": f"Documentary E2E Test",
                "description": "Documentary films for E2E test",
                "is_active": True,
            }
            category_response: Any = api_client.post(category_url, data=category_data)
            assert category_response.status_code == HTTP_201_CREATED, (
                f"Failed to create category: {category_response.data}"
            )
            category_id = category_response.data["id"]

            # Create a Genre (linked to the category)
            genre_data: dict[str, Any] = {
                "name": f"Science E2E Test",
                "is_active": True,
                "categories": [category_id],
            }
            genre_response: Any = api_client.post(genre_url, data=genre_data)
            assert genre_response.status_code == HTTP_201_CREATED, (
                f"Failed to create genre: {genre_response.data}"
            )
            genre_id = genre_response.data["id"]

            # Create a CastMember
            cast_member_data: dict[str, Any] = {
                "name": f"David Attenborough E2E Test",
                "type": "ACTOR",
            }
            cast_member_response: Any = api_client.post(
                cast_member_url, data=cast_member_data
            )
            assert cast_member_response.status_code == HTTP_201_CREATED, (
                f"Failed to create cast member: {cast_member_response.data}"
            )
            cast_member_id = cast_member_response.data["id"]

            # ============================================================
            # Step 2: Create a Video
            # ============================================================

            video_data: dict[str, Any] = {
                "title": f"Planet Earth E2E Test",
                "description": "A nature documentary series for E2E test",
                "launch_year": 2023,
                "duration": "120.00",
                "rating": "AGE_10",
                "categories": [category_id],
                "genres": [genre_id],
                "cast_members": [cast_member_id],
            }
            video_response: Any = api_client.post(video_url, data=video_data)
            assert video_response.status_code == HTTP_201_CREATED, (
                f"Failed to create video: {video_response.data}"
            )
            video_id = video_response.data["id"]

            # Verify video was created with published=False
            get_video_response: Any = api_client.get(f"{video_url}{video_id}/")
            assert get_video_response.status_code == HTTP_200_OK
            assert get_video_response.data["data"]["published"] is False

            # ============================================================
            # Step 3: Upload video media file
            # ============================================================

            # Get the project root directory and video file path
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            file_name: str = "ShowDaXuxa.mp4"
            video_file_path: str = os.path.join(project_root, file_name)

            # Read the video file
            with open(video_file_path, "rb") as f:
                file_content: bytes = f.read()

            upload_file = SimpleUploadedFile(
                name=file_name,
                content=file_content,
                content_type="video/mp4",
            )

            # Upload the video file via PATCH
            media_response = api_client.patch(
                f"{video_url}{video_id}/",
                data={"video_file": upload_file},
                format="multipart",
            )
            assert media_response.status_code == HTTP_200_OK, (
                f"Failed to upload video media: {media_response.data}"
            )

            # Verify the file was saved
            expected_file_path = f"/tmp/codeflix-storage/videos/{video_id}/{file_name}"
            assert os.path.exists(expected_file_path), (
                f"Video file not found at {expected_file_path}"
            )

            # Verify initial video media status is PENDING
            video_orm = get_video_from_db(video_id)
            assert video_orm.video is not None, "Video media was not created"
            assert video_orm.video.status == "PENDING", (
                f"Expected PENDING status, got {video_orm.video.status}"
            )
            assert video_orm.video.media_type == "VIDEO"

            # ============================================================
            # Step 4: Publish message to RabbitMQ videos.converted queue
            # ============================================================

            encoded_location = f"/encoded/videos/{video_id}"
            send_video_converted_message(
                video_id=video_id,
                media_type="VIDEO",
                encoded_location=encoded_location,
                status="COMPLETED",
            )

            # ============================================================
            # Step 5: Verify video status is COMPLETED
            # ============================================================

            # Wait for the consumer to process the message
            status_updated = wait_for_video_status(
                video_id=video_id,
                expected_status="COMPLETED",
                timeout=10,
            )
            assert status_updated, (
                "Video status was not updated to COMPLETED within timeout. "
                "Make sure the consumer is running: python manage.py startconsumer"
            )

            # Refresh and verify final state
            video_orm = get_video_from_db(video_id)
            assert video_orm.video.status == "COMPLETED", (
                f"Expected COMPLETED status, got {video_orm.video.status}"
            )
            assert video_orm.video.encoded_location == encoded_location, (
                f"Expected encoded_location '{encoded_location}', "
                f"got '{video_orm.video.encoded_location}'"
            )
            assert video_orm.published is True, (
                "Video should be published after conversion completes"
            )

            # Also verify via API
            final_video_response: Any = api_client.get(f"{video_url}{video_id}/")
            assert final_video_response.status_code == HTTP_200_OK
            assert final_video_response.data["data"]["published"] is True

            print(f"\n✅ E2E Test PASSED: Video {video_id} was successfully processed")
            print(f"   - Video status: COMPLETED")
            print(f"   - Video published: True")
            print(f"   - Encoded location: {encoded_location}")

        finally:
            # ============================================================
            # Cleanup - Delete created entities from real database
            # ============================================================
            from django_project.video_app.models import Video as VideoORM
            from django_project.category_app.models import Category as CategoryORM
            from django_project.genre_app.models import Genre as GenreORM
            from django_project.castmember_app.models import CastMember as CastMemberORM

            if video_id:
                try:
                    video = VideoORM.objects.get(id=video_id)
                    # Delete associated media
                    if video.video:
                        video.video.delete()
                    video.delete()
                except VideoORM.DoesNotExist:
                    pass

                # Clean up file storage
                video_folder_path = f"/tmp/codeflix-storage/videos/{video_id}"
                if os.path.exists(video_folder_path):
                    shutil.rmtree(video_folder_path)

            if genre_id:
                try:
                    GenreORM.objects.filter(id=genre_id).delete()
                except Exception:
                    pass

            if cast_member_id:
                try:
                    CastMemberORM.objects.filter(id=cast_member_id).delete()
                except Exception:
                    pass

            if category_id:
                try:
                    CategoryORM.objects.filter(id=category_id).delete()
                except Exception:
                    pass
