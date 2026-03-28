#!/usr/bin/env bash
set -euo pipefail

# Configuration
BASE_URL="${BASE_URL:-http://localhost:8000}"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq to run this script." >&2
    echo "On Ubuntu/Debian: sudo apt-get install jq" >&2
    echo "On macOS: brew install jq" >&2
    exit 1
fi

# Load messages file
MESSAGES_FILE="$SCRIPT_DIR/messages.json"
if [[ ! -f "$MESSAGES_FILE" ]]; then
    echo "Error: messages.json not found at $MESSAGES_FILE" >&2
    exit 1
fi

# Get total message count
TOTAL=$(jq 'length' "$MESSAGES_FILE")

# Print header
echo "Seeding $TOTAL messages to $BASE_URL/chat"

# Counter for iteration
COUNT=0

# Loop over each message
while read -r message; do
    COUNT=$((COUNT + 1))

    # Extract id and patient
    ID=$(echo "$message" | jq -r '.id')
    PATIENT=$(echo "$message" | jq -r '.patient')
    MSG_TEXT=$(echo "$message" | jq -r '.message')

    # Print progress
    printf "[%d/%d] %s: " "$COUNT" "$TOTAL" "$PATIENT"

    # Prepare JSON payload
    PAYLOAD=$(jq -n --arg msg "$MSG_TEXT" '{user_message: $msg}')

    # Make request and capture response body + HTTP status code
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD" \
        "$BASE_URL/chat")

    # Split response into body and status code
    HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
    BODY=$(echo "$RESPONSE" | head -n -1)

    # Handle response
    if [[ "$HTTP_CODE" == "200" ]]; then
        echo "OK - $BODY"
    else
        echo "FAIL (HTTP $HTTP_CODE) - $BODY" >&2
    fi
done < <(jq -c '.[]' "$MESSAGES_FILE")

echo "Done."
