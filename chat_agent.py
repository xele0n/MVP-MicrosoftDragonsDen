"""
AI Chat Agent Module for SPTool
Provides intelligent troubleshooting assistance using OpenAI
"""
import openai
from config import Config
from system_diagnostics import SystemDiagnostics
import json

class ChatAgent:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        if self.api_key:
            openai.api_key = self.api_key
        self.diagnostics = SystemDiagnostics()
        self.conversation_history = []
        
    def is_configured(self):
        """Check if OpenAI API key is configured"""
        return bool(self.api_key and self.api_key.strip())
    
    def get_system_context(self):
        """Get current system state for context"""
        try:
            data = self.diagnostics.get_full_diagnostic()
            
            # Create a concise summary for the AI
            context = {
                'os': data.get('system_info', {}).get('os', 'Unknown'),
                'cpu_usage': data.get('cpu', {}).get('usage', 0),
                'memory_usage': data.get('memory', {}).get('percent', 0),
                'disk_usage': [d.get('percent', 0) for d in data.get('disk', [])],
                'top_processes': [
                    {'name': p.get('name'), 'cpu': p.get('cpu_percent'), 'memory': p.get('memory_percent')}
                    for p in data.get('processes', {}).get('top_cpu', [])[:5]
                ]
            }
            return context
        except Exception as e:
            return {'error': str(e)}
    
    def chat(self, user_message, include_system_context=True):
        """
        Send a message to the AI agent and get a response
        
        Args:
            user_message: The user's message
            include_system_context: Whether to include current system diagnostics
            
        Returns:
            Dictionary with response and metadata
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'OpenAI API key not configured. Please set OPENAI_API_KEY in .env file.',
                'response': None
            }
        
        try:
            # Build system prompt
            system_prompt = """You are SPTool Assistant, an expert system administrator and troubleshooting agent. 
You help users diagnose and fix computer performance issues.

Your capabilities:
- Diagnose CPU, memory, disk, and network issues
- Suggest specific fixes and commands
- Explain technical concepts clearly
- Provide step-by-step troubleshooting guidance

When responding:
- Be concise and professional
- Provide actionable advice
- Reference specific metrics when available
- Suggest SPTool features when relevant (like "Run Full Diagnosis" or viewing Top Processes)
- If suggesting commands, explain what they do

Keep responses under 200 words unless detailed explanation is needed."""

            # Add system context if requested
            if include_system_context:
                context = self.get_system_context()
                if 'error' not in context:
                    system_prompt += f"\n\nCurrent system state:\n{json.dumps(context, indent=2)}"
            
            # Build messages array
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history (last 10 messages to stay within limits)
            messages.extend(self.conversation_history[-10:])
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return {
                'success': True,
                'response': assistant_message,
                'tokens_used': response.usage.total_tokens
            }
            
        except openai.error.AuthenticationError:
            return {
                'success': False,
                'error': 'Invalid OpenAI API key. Please check your OPENAI_API_KEY in .env file.',
                'response': None
            }
        except openai.error.RateLimitError:
            return {
                'success': False,
                'error': 'OpenAI rate limit exceeded. Please try again in a moment.',
                'response': None
            }
        except openai.error.APIError as e:
            return {
                'success': False,
                'error': f'OpenAI API error: {str(e)}',
                'response': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'response': None
            }
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        return {'success': True, 'message': 'Conversation history cleared'}
    
    def get_quick_analysis(self):
        """Get a quick AI analysis of current system state"""
        context = self.get_system_context()
        
        if 'error' in context:
            return {
                'success': False,
                'error': 'Could not retrieve system information',
                'response': None
            }
        
        prompt = f"""Based on this system state, provide a brief analysis (2-3 sentences):

CPU: {context.get('cpu_usage')}%
Memory: {context.get('memory_usage')}%
Disk: {context.get('disk_usage')}

Top processes: {json.dumps(context.get('top_processes', []), indent=2)}

Is there anything concerning? Any recommendations?"""
        
        return self.chat(prompt, include_system_context=False)

