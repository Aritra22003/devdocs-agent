# API Error Handling

- 400 Bad Request: Invalid request input.
- 401 Unauthorized: Missing or invalid authentication.
- 403 Forbidden: Insufficient permissions.
- 404 Not Found: Resource does not exist.
- 429 Too Many Requests: Rate limit exceeded.
- 500 Internal Server Error: Unexpected server error.

For rate limits, use an appropriate retry delay and backoff.