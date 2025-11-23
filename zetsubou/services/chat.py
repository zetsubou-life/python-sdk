"""
Chat Service

Handles chat conversations and message management.
"""

from typing import List, Dict, Any, Optional, Union
from ..models import ChatConversation, ChatMessage
from ..exceptions import ZetsubouError


class ChatService:
    """Service for managing chat conversations and messages."""
    
    def __init__(self, client):
        self.client = client
    
    def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ChatConversation]:
        """
        List all chat conversations.
        
        Args:
            limit: Number of results per page
            offset: Pagination offset
            
        Returns:
            List of ChatConversation objects
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        
        response = self.client.get('/api/v2/chat/conversations', params=params)
        data = response.json()
        return [ChatConversation.from_dict(conv) for conv in data['conversations']]
    
    def create_conversation(
        self,
        title: str,
        model: str = "llama3.2",
        system_prompt: Optional[str] = None
    ) -> ChatConversation:
        """
        Create a new chat conversation.
        
        Args:
            title: Conversation title
            model: AI model to use
            system_prompt: Optional system prompt
            
        Returns:
            ChatConversation object
        """
        data = {
            'title': title,
            'model': model
        }
        if system_prompt:
            data['system_prompt'] = system_prompt
        
        response = self.client.post('/api/v2/chat/conversations', data=data)
        result = response.json()
        return ChatConversation.from_dict(result['conversation'])
    
    def get_conversation(self, conversation_uuid: str) -> ChatConversation:
        """
        Get details for a specific conversation.
        
        Args:
            conversation_uuid: Conversation UUID
            
        Returns:
            ChatConversation object
        """
        response = self.client.get(f'/api/v2/chat/conversations/{conversation_uuid}')
        data = response.json()
        return ChatConversation.from_dict(data)
    
    def delete_conversation(self, conversation_uuid: str) -> bool:
        """
        Delete a chat conversation.
        
        Args:
            conversation_uuid: Conversation UUID
            
        Returns:
            True if deletion was successful
        """
        response = self.client.delete(f'/api/v2/chat/conversations/{conversation_uuid}')
        data = response.json()
        return data.get('success', False)
    
    def get_messages(self, conversation_uuid: str) -> List[ChatMessage]:
        """
        Get all messages for a conversation.
        
        Args:
            conversation_uuid: Conversation UUID
            
        Returns:
            List of ChatMessage objects
        """
        response = self.client.get(f'/api/v2/chat/conversations/{conversation_uuid}/messages')
        data = response.json()
        return [ChatMessage.from_dict(msg) for msg in data['messages']]
    
    def send_message(
        self,
        conversation_uuid: str,
        content: str
    ) -> ChatMessage:
        """
        Send a message to a conversation.
        
        Args:
            conversation_uuid: Conversation UUID
            content: Message content
            
        Returns:
            ChatMessage object
        """
        data = {'content': content}
        
        response = self.client.post(
            f'/api/v2/chat/conversations/{conversation_uuid}/messages',
            data=data
        )
        result = response.json()
        return ChatMessage.from_dict(result['message'])
    
    def export_conversation(
        self,
        conversation_uuid: str,
        format: str = "json",
        output_path: Optional[str] = None
    ) -> Union[Dict[str, Any], str, bytes]:
        """
        Export a conversation in various formats.
        
        Args:
            conversation_uuid: Conversation UUID
            format: Export format ('json', 'md', 'html', or 'pdf')
            output_path: Optional path to save the exported file (for html/pdf)
            
        Returns:
            Exported conversation data (dict for json, str for md/html, bytes for pdf)
        """
        params = {'format': format}
        response = self.client.get(
            f'/api/v2/chat/conversations/{conversation_uuid}/export',
            params=params,
            stream=(format in ['html', 'pdf'])
        )
        
        if format == 'json':
            return response.json()
        elif format == 'md':
            return response.text
        elif format == 'html':
            content = response.text
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return output_path
            return content
        elif format == 'pdf':
            content = response.content
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(content)
                return output_path
            return content
        else:
            raise ValueError(f"Unsupported export format: {format}. Use 'json', 'md', 'html', or 'pdf'")
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available AI models.
        
        Returns:
            List of model names
        """
        # Note: This would require a separate API endpoint
        # For now, return common models
        return [
            "llama3.2",
            "qwen2.5-vl",
            "glm-4.6:cloud",
            "auto"
        ]
    
    def create_and_send_message(
        self,
        title: str,
        content: str,
        model: str = "llama3.2",
        system_prompt: Optional[str] = None
    ) -> tuple[ChatConversation, ChatMessage]:
        """
        Create a new conversation and send the first message.
        
        Args:
            title: Conversation title
            content: First message content
            model: AI model to use
            system_prompt: Optional system prompt
            
        Returns:
            Tuple of (ChatConversation, ChatMessage) objects
        """
        conversation = self.create_conversation(title, model, system_prompt)
        message = self.send_message(conversation.uuid, content)
        return conversation, message