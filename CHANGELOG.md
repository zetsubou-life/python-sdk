# Changelog

All notable changes to the Zetsubou.life Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2024-01-XX

### Changed
- **BREAKING**: Chat API methods now use `conversation_uuid` (string) instead of `conversation_id` (integer)
  - `get_conversation(conversation_uuid: str)` - Updated parameter name and type
  - `delete_conversation(conversation_uuid: str)` - Updated parameter name and type
  - `get_messages(conversation_uuid: str)` - Updated parameter name and type
  - `send_message(conversation_uuid: str, ...)` - Updated parameter name and type
  - `export_conversation(conversation_uuid: str)` - Updated parameter name and type
  - `create_and_send_message(conversation_uuid: str, ...)` - Updated parameter name and type

### Fixed
- Updated `ChatConversation` and `ChatMessage` models to use `uuid` field instead of `id`
- All chat-related API calls now correctly use UUID-based conversation identifiers

### Migration Guide
If you're upgrading from version 1.1.0 or earlier:

```python
# Old code (v1.1.0)
conversation = client.chat.get_conversation(conversation_id=123)
messages = client.chat.get_messages(conversation_id=123)

# New code (v1.1.1)
conversation = client.chat.get_conversation(conversation_uuid="550e8400-e29b-41d4-a716-446655440000")
messages = client.chat.get_messages(conversation_uuid="550e8400-e29b-41d4-a716-446655440000")
```

## [1.1.0] - 2024-01-XX

### Added
- Initial release of Python SDK
- Support for API v2 endpoints
- Chat API integration
- Tool execution and job management
- VFS (Virtual File System) operations
- Webhook management
- Account and usage tracking

