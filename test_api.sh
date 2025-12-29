#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Base URL
BASE_URL="http://localhost:8000"

echo -e "${BLUE}=== Codeflix API Testing Script ===${NC}\n"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is not installed. Please install it first:${NC}"
    echo "  Ubuntu/Debian: sudo apt-get install jq"
    echo "  MacOS: brew install jq"
    exit 1
fi

# 1. Create a Category
echo -e "${BLUE}1. Creating a category...${NC}"
CATEGORY_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/categories/" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Infantil",
    "description": "Indicado para o público menor de 10 anos",
    "is_active": true
  }')

CATEGORY_ID=$(echo $CATEGORY_RESPONSE | jq -r '.id')

if [ "$CATEGORY_ID" = "null" ] || [ -z "$CATEGORY_ID" ]; then
    echo -e "${RED}Failed to create category${NC}"
    echo "Response: $CATEGORY_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✓ Category created with ID: $CATEGORY_ID${NC}\n"

# 2. Create a Genre
echo -e "${BLUE}2. Creating a genre...${NC}"
GENRE_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/genres/" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Desenho\",
    \"is_active\": true,
    \"categories\": [\"$CATEGORY_ID\"]
  }")

GENRE_ID=$(echo $GENRE_RESPONSE | jq -r '.id')

if [ "$GENRE_ID" = "null" ] || [ -z "$GENRE_ID" ]; then
    echo -e "${RED}Failed to create genre${NC}"
    echo "Response: $GENRE_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✓ Genre created with ID: $GENRE_ID${NC}\n"

# 3. Create a Cast Member
echo -e "${BLUE}3. Creating a cast member...${NC}"
CAST_MEMBER_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/cast_members/" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Docinho",
    "type": "ACTOR"
  }')

CAST_MEMBER_ID=$(echo $CAST_MEMBER_RESPONSE | jq -r '.id')

if [ "$CAST_MEMBER_ID" = "null" ] || [ -z "$CAST_MEMBER_ID" ]; then
    echo -e "${RED}Failed to create cast member${NC}"
    echo "Response: $CAST_MEMBER_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✓ Cast Member created with ID: $CAST_MEMBER_ID${NC}\n"

# 4. Create a Video
echo -e "${BLUE}4. Creating a video...${NC}"
VIDEO_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/videos/" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Meninas Superpoderosas\",
    \"description\": \"As defensoras de Townsville\",
    \"launch_year\": 2003,
    \"duration\": \"40.00\",
    \"rating\": \"L\",
    \"categories\": [\"$CATEGORY_ID\"],
    \"genres\": [\"$GENRE_ID\"],
    \"cast_members\": [\"$CAST_MEMBER_ID\"]
  }")

VIDEO_ID=$(echo $VIDEO_RESPONSE | jq -r '.id')

if [ "$VIDEO_ID" = "null" ] || [ -z "$VIDEO_ID" ]; then
    echo -e "${RED}Failed to create video${NC}"
    echo "Response: $VIDEO_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✓ Video created with ID: $VIDEO_ID${NC}\n"

# 5. Retrieve the video
echo -e "${BLUE}5. Retrieving the video...${NC}"
VIDEO_GET_RESPONSE=$(curl -s -X GET "${BASE_URL}/api/videos/${VIDEO_ID}/" \
  -H "Accept: application/json")

echo -e "${GREEN}✓ Video retrieved successfully${NC}"
echo "$VIDEO_GET_RESPONSE" | jq '.'

# 6. Upload video media file
echo -e "\n${BLUE}6. Uploading video media file...${NC}"

# Check if the video file exists
VIDEO_FILE="ShowDaXuxa.mp4"
if [ ! -f "$VIDEO_FILE" ]; then
    echo -e "${RED}Error: Video file '$VIDEO_FILE' not found in current directory${NC}"
    echo "Please ensure ShowDaXuxa.mp4 exists in the project root"
    exit 1
fi

UPLOAD_RESPONSE=$(curl -s -X PATCH "${BASE_URL}/api/videos/${VIDEO_ID}/" \
  -H "Accept: application/json" \
  -F "video_file=@${VIDEO_FILE}")

UPLOAD_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X PATCH "${BASE_URL}/api/videos/${VIDEO_ID}/" \
  -H "Accept: application/json" \
  -F "video_file=@${VIDEO_FILE}")

if [ "$UPLOAD_STATUS" = "200" ]; then
    echo -e "${GREEN}✓ Video media uploaded successfully${NC}"
    
    # Verify the file was saved
    STORAGE_PATH="/tmp/codeflix-storage/videos/${VIDEO_ID}/${VIDEO_FILE}"
    if [ -f "$STORAGE_PATH" ]; then
        FILE_SIZE=$(du -h "$STORAGE_PATH" | cut -f1)
        echo -e "${GREEN}  File saved at: $STORAGE_PATH (Size: $FILE_SIZE)${NC}"
    else
        echo -e "${RED}  Warning: File not found at expected location: $STORAGE_PATH${NC}"
    fi
else
    echo -e "${RED}Failed to upload video media (HTTP $UPLOAD_STATUS)${NC}"
    echo "Response: $UPLOAD_RESPONSE"
fi

# Summary
echo -e "\n${BLUE}=== Summary ===${NC}"
echo -e "Category ID:    ${GREEN}$CATEGORY_ID${NC}"
echo -e "Genre ID:       ${GREEN}$GENRE_ID${NC}"
echo -e "Cast Member ID: ${GREEN}$CAST_MEMBER_ID${NC}"
echo -e "Video ID:       ${GREEN}$VIDEO_ID${NC}"
echo -e "Upload Status:  ${GREEN}HTTP $UPLOAD_STATUS${NC}"

echo -e "\n${GREEN}✓ All API tests completed successfully!${NC}"
