from typing import Any
import pytest
from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import shutil


@pytest.mark.django_db
class TestCreateVideoWithoutMediaAPI:
    def test_create_video_without_media(
        self,
        api_client: APIClient,
    ) -> None:
        # Create a video without media flux
        video_url: str = "/api/videos/"
        category_url: str = "/api/categories/"
        genre_url: str = "/api/genres/"
        cast_member_url: str = "/api/cast_members/"

        category_data: dict[str, Any] = {
            "name": "Movie",
            "description": "Movie category",
            "is_active": True,
        }

        genre_data: dict[str, Any] = {
            "name": "Action",
            "is_active": True,
            "categories": [],
        }

        cast_member_data: dict[str, Any] = {
            "name": "Denzel Washington",
            "type": "ACTOR",
        }

        video_data: dict[str, Any] = {
            "title": "Test Video",
            "description": "Test Description",
            "launch_year": 2023,
            "duration": "120.00",
            "rating": "AGE_14",
            "categories": [],
            "genres": [],
            "cast_members": [],
        }

        # Create a category
        category_response: Any = api_client.post(category_url, data=category_data)
        assert category_response.status_code == HTTP_201_CREATED
        category_id: str = category_response.data["id"]

        # Get category by ID
        category_response: Any = api_client.get(f"{category_url}{category_id}/")
        assert category_response.status_code == HTTP_200_OK
        assert category_response.data["data"]["id"] == category_id
        assert category_response.data["data"]["name"] == category_data["name"]
        assert (
            category_response.data["data"]["description"]
            == category_data["description"]
        )
        assert category_response.data["data"]["is_active"] == category_data["is_active"]

        # Create a genre
        genre_data["categories"].append(category_id)
        genre_response: Any = api_client.post(genre_url, data=genre_data)
        assert genre_response.status_code == HTTP_201_CREATED
        genre_id: str = genre_response.data["id"]

        # List genres

        genre_response: Any = api_client.get(genre_url)
        assert genre_response.status_code == HTTP_200_OK
        assert genre_response.data["data"][0]["id"] == genre_id
        assert genre_response.data["data"][0]["name"] == genre_data["name"]
        assert genre_response.data["data"][0]["is_active"] == genre_data["is_active"]
        assert genre_response.data["data"][0]["categories"] == [category_id]

        # Create a cast member
        cast_member_response: Any = api_client.post(
            cast_member_url, data=cast_member_data
        )
        assert cast_member_response.status_code == HTTP_201_CREATED
        cast_member_id: str = cast_member_response.data["id"]

        # List cast members
        cast_member_response: Any = api_client.get(cast_member_url)
        assert cast_member_response.status_code == HTTP_200_OK
        assert cast_member_response.data["data"][0]["id"] == cast_member_id
        assert cast_member_response.data["data"][0]["name"] == cast_member_data["name"]
        assert cast_member_response.data["data"][0]["type"] == cast_member_data["type"]

        # Create a video
        video_data["categories"].append(category_id)
        video_data["genres"].append(genre_id)
        video_data["cast_members"].append(cast_member_id)

        video_response: Any = api_client.post(video_url, data=video_data)
        assert video_response.status_code == HTTP_201_CREATED
        video_id: str = video_response.data["id"]

        # Get video by ID
        video_response: Any = api_client.get(f"{video_url}{video_id}/")
        assert video_response.status_code == HTTP_200_OK
        assert video_response.data["data"]["id"] == video_id
        assert video_response.data["data"]["title"] == video_data["title"]
        assert video_response.data["data"]["description"] == video_data["description"]
        assert video_response.data["data"]["launch_year"] == video_data["launch_year"]
        assert video_response.data["data"]["duration"] == video_data["duration"]
        assert video_response.data["data"]["published"] is False
        assert video_response.data["data"]["rating"] == video_data["rating"]
        assert video_response.data["data"]["categories"] == [category_id]
        assert video_response.data["data"]["genres"] == [genre_id]
        assert video_response.data["data"]["cast_members"] == [cast_member_id]

    def test_create_video_without_media_fail(
        self,
        api_client: APIClient,
    ) -> None:
        # Create a video without media flux
        video_url: str = "/api/videos/"
        category_url: str = "/api/categories/"
        genre_url: str = "/api/genres/"
        cast_member_url: str = "/api/cast_members/"

        category_data: dict[str, Any] = {
            "name": "Movie",
            "description": "Movie category",
            "is_active": True,
        }

        genre_data: dict[str, Any] = {
            "name": "Action",
            "is_active": True,
            "categories": [],
        }

        cast_member_data: dict[str, Any] = {
            "name": "Denzel Washington",
            "type": "ACTOR",
        }

        video_data: dict[str, Any] = {
            "title": "Test Video",
            "description": "Test Description",
            "launch_year": 2023,
            "duration": "120.00",
            "rating": "AGE_14",
            "categories": [],
            "genres": [],
            "cast_members": [],
        }

        # Create a category
        category_response: Any = api_client.post(category_url, data=category_data)
        assert category_response.status_code == HTTP_201_CREATED
        category_id: str = category_response.data["id"]

        # Get category by ID
        category_response: Any = api_client.get(f"{category_url}{category_id}/")
        assert category_response.status_code == HTTP_200_OK
        assert category_response.data["data"]["id"] == category_id
        assert category_response.data["data"]["name"] == category_data["name"]
        assert (
            category_response.data["data"]["description"]
            == category_data["description"]
        )
        assert category_response.data["data"]["is_active"] == category_data["is_active"]

        # Create a genre
        genre_data["categories"].append(category_id)
        genre_response: Any = api_client.post(genre_url, data=genre_data)
        assert genre_response.status_code == HTTP_201_CREATED
        genre_id: str = genre_response.data["id"]

        # List genres

        genre_response: Any = api_client.get(genre_url)
        assert genre_response.status_code == HTTP_200_OK
        assert genre_response.data["data"][0]["id"] == genre_id
        assert genre_response.data["data"][0]["name"] == genre_data["name"]
        assert genre_response.data["data"][0]["is_active"] == genre_data["is_active"]
        assert genre_response.data["data"][0]["categories"] == [category_id]

        # Create a cast member
        cast_member_response: Any = api_client.post(
            cast_member_url, data=cast_member_data
        )
        assert cast_member_response.status_code == HTTP_201_CREATED
        cast_member_id: str = cast_member_response.data["id"]

        # List cast members
        cast_member_response: Any = api_client.get(cast_member_url)
        assert cast_member_response.status_code == HTTP_200_OK
        assert cast_member_response.data["data"][0]["id"] == cast_member_id
        assert cast_member_response.data["data"][0]["name"] == cast_member_data["name"]
        assert cast_member_response.data["data"][0]["type"] == cast_member_data["type"]

        # Create a video with invalid category ID formart
        video_data["categories"].append("invalid-category-id")
        video_data["genres"].append(genre_id)
        video_data["cast_members"].append(cast_member_id)
        video_response: Any = api_client.post(video_url, data=video_data)
        assert video_response.status_code == HTTP_400_BAD_REQUEST
        assert "Must be a valid UUID." in video_response.data["categories"][0]

        video_data["categories"].clear()

        # Create a video with invalid category ID
        last_digit = category_id[-1]
        new_digit = "0" if last_digit != "0" else "1"
        modified_category_id = category_id[:-1] + new_digit
        video_data["categories"].append(modified_category_id)
        video_response: Any = api_client.post(video_url, data=video_data)
        assert video_response.status_code == HTTP_400_BAD_REQUEST
        assert video_response.data == {
            "categories": [
                f"Invalid categorie(s) with provided ID(s) not found: '{modified_category_id}'"
            ]
        }

        video_data["categories"].clear()

        # Create a video with invalid genre ID
        video_data["categories"].append(category_id)
        last_digit = genre_id[-1]
        new_digit = "0" if last_digit != "0" else "1"
        modified_genre_id = genre_id[:-1] + new_digit
        video_data["genres"].append(modified_genre_id)
        video_response: Any = api_client.post(video_url, data=video_data)
        assert video_response.status_code == HTTP_400_BAD_REQUEST
        assert video_response.data == {
            "genres": [
                f"Invalid genre(s) with provided ID(s) not found: '{modified_genre_id}'"
            ]
        }
        video_data["genres"].clear()

        # Create a video with invalid cast member ID
        video_data["genres"].append(genre_id)
        last_digit = cast_member_id[-1]
        new_digit = "0" if last_digit != "0" else "1"
        modified_cast_member_id = cast_member_id[:-1] + new_digit
        video_data["cast_members"].append(modified_cast_member_id)
        video_response: Any = api_client.post(video_url, data=video_data)
        assert video_response.status_code == HTTP_400_BAD_REQUEST
        assert video_response.data == {
            "cast_members": [
                f"Invalid cast member(s) with provided ID(s) not found: '{modified_cast_member_id}'"
            ]
        }
        video_data["cast_members"].clear()

        # Create a video
        video_data["cast_members"].append(cast_member_id)

        video_response: Any = api_client.post(video_url, data=video_data)
        assert video_response.status_code == HTTP_201_CREATED
        video_id: str = video_response.data["id"]

        # Get video by ID
        video_response: Any = api_client.get(f"{video_url}{video_id}/")
        assert video_response.status_code == HTTP_200_OK
        assert video_response.data["data"]["id"] == video_id
        assert video_response.data["data"]["title"] == video_data["title"]
        assert video_response.data["data"]["description"] == video_data["description"]
        assert video_response.data["data"]["launch_year"] == video_data["launch_year"]
        assert video_response.data["data"]["duration"] == video_data["duration"]
        assert video_response.data["data"]["published"] is False
        assert video_response.data["data"]["rating"] == video_data["rating"]
        assert video_response.data["data"]["categories"] == [category_id]
        assert video_response.data["data"]["genres"] == [genre_id]
        assert video_response.data["data"]["cast_members"] == [cast_member_id]


# TODO: Implement tests for upload video API


@pytest.mark.django_db
class TestUploadVideoMediaAPI:
    def test_upload_video_media(
        self,
        api_client: APIClient,
    ) -> None:
        # Create a video without media flux
        video_url: str = "/api/videos/"
        category_url: str = "/api/categories/"
        genre_url: str = "/api/genres/"
        cast_member_url: str = "/api/cast_members/"

        category_data: dict[str, Any] = {
            "name": "Movie",
            "description": "Movie category",
            "is_active": True,
        }

        genre_data: dict[str, Any] = {
            "name": "Action",
            "is_active": True,
            "categories": [],
        }

        cast_member_data: dict[str, Any] = {
            "name": "Denzel Washington",
            "type": "ACTOR",
        }

        video_data: dict[str, Any] = {
            "title": "Test Video",
            "description": "Test Description",
            "launch_year": 2023,
            "duration": "120.00",
            "rating": "AGE_14",
            "categories": [],
            "genres": [],
            "cast_members": [],
        }

        # Create a category
        category_response: Any = api_client.post(category_url, data=category_data)
        assert category_response.status_code == HTTP_201_CREATED
        category_id: str = category_response.data["id"]

        # Get category by ID
        category_response: Any = api_client.get(f"{category_url}{category_id}/")
        assert category_response.status_code == HTTP_200_OK
        assert category_response.data["data"]["id"] == category_id
        assert category_response.data["data"]["name"] == category_data["name"]
        assert (
            category_response.data["data"]["description"]
            == category_data["description"]
        )
        assert category_response.data["data"]["is_active"] == category_data["is_active"]

        # Create a genre
        genre_data["categories"].append(category_id)
        genre_response: Any = api_client.post(genre_url, data=genre_data)
        assert genre_response.status_code == HTTP_201_CREATED
        genre_id: str = genre_response.data["id"]

        # List genres

        genre_response: Any = api_client.get(genre_url)
        assert genre_response.status_code == HTTP_200_OK
        assert genre_response.data["data"][0]["id"] == genre_id
        assert genre_response.data["data"][0]["name"] == genre_data["name"]
        assert genre_response.data["data"][0]["is_active"] == genre_data["is_active"]
        assert genre_response.data["data"][0]["categories"] == [category_id]

        # Create a cast member
        cast_member_response: Any = api_client.post(
            cast_member_url, data=cast_member_data
        )
        assert cast_member_response.status_code == HTTP_201_CREATED
        cast_member_id: str = cast_member_response.data["id"]

        # List cast members
        cast_member_response: Any = api_client.get(cast_member_url)
        assert cast_member_response.status_code == HTTP_200_OK
        assert cast_member_response.data["data"][0]["id"] == cast_member_id
        assert cast_member_response.data["data"][0]["name"] == cast_member_data["name"]
        assert cast_member_response.data["data"][0]["type"] == cast_member_data["type"]

        # Create a video
        video_data["categories"].append(category_id)
        video_data["genres"].append(genre_id)
        video_data["cast_members"].append(cast_member_id)

        video_response: Any = api_client.post(video_url, data=video_data)
        assert video_response.status_code == HTTP_201_CREATED
        video_id: str = video_response.data["id"]

        # Get video by ID
        video_response: Any = api_client.get(f"{video_url}{video_id}/")
        assert video_response.status_code == HTTP_200_OK
        assert video_response.data["data"]["id"] == video_id
        assert video_response.data["data"]["title"] == video_data["title"]
        assert video_response.data["data"]["description"] == video_data["description"]
        assert video_response.data["data"]["launch_year"] == video_data["launch_year"]
        assert video_response.data["data"]["duration"] == video_data["duration"]
        assert video_response.data["data"]["published"] is False
        assert video_response.data["data"]["rating"] == video_data["rating"]
        assert video_response.data["data"]["categories"] == [category_id]
        assert video_response.data["data"]["genres"] == [genre_id]
        assert video_response.data["data"]["cast_members"] == [cast_member_id]

        # Upload video media
        # Get the project root directory
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        file_name: str = "ShowDaXuxa.mp4"
        video_file_path: str = os.path.join(project_root, file_name)

        with open(video_file_path, "rb") as f:
            file_content: bytes = f.read()

        upload_file = SimpleUploadedFile(
            name=file_name, content=file_content, content_type="video/mp4"
        )

        # Make the PATCH request with the file
        media_response = api_client.patch(
            f"{video_url}{video_id}/",
            data={"video_file": upload_file},
            format="multipart",
        )

        assert media_response.status_code == HTTP_200_OK
        # Verify the file was saved in the correct location
        expected_file_path = f"/tmp/codeflix-storage/videos/{video_id}/{file_name}"
        assert os.path.exists(expected_file_path), f"File not found at {expected_file_path}"

        # Verify the file content matches what was uploaded
        with open(expected_file_path, "rb") as f:
            saved_content = f.read()
        assert saved_content == file_content, "File content doesn't match the uploaded content"

        # Clean up by deleting the video folder
        video_folder_path = f"/tmp/codeflix-storage/videos/{video_id}"
        if os.path.exists(video_folder_path):
            shutil.rmtree(video_folder_path)

        # Verify the folder was deleted
        assert not os.path.exists(video_folder_path), f"Failed to delete video folder at {video_folder_path}"
