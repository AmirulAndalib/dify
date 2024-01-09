from core.tools.provider.tool_provider import Tool
from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.errors import ToolProviderCredentialValidationError, ToolInvokeError
from core.model_runtime.entities.message_entities import PromptMessage

from typing import Any, Dict, List, Union, Optional, Tuple

from httpx import get

class WolframAlphaTool(Tool):
    _base_url = 'https://api.wolframalpha.com/v2/query'

    def _invoke(self, 
                user_id: str, 
               tool_paramters: Dict[str, Any], 
               credentials: Dict[str, Any], 
               prompt_messages: List[PromptMessage]
        ) -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
            invoke tools
        """
        query = tool_paramters.get('query', '')
        if not query:
            return self.create_text_message('Please input query')
        appid = credentials.get('appid', '')
        if not appid:
            raise ToolProviderCredentialValidationError('Please input appid')
        
        params = {
            'appid': appid,
            'input': query,
            'includepodid': 'Result',
            'format': 'plaintext',
            'output': 'json'
        }

        finished = False
        result = None
        # try 3 times at most
        counter = 0

        while not finished and counter < 3:
            counter += 1
            try:
                response = get(self._base_url, params=params)
                response.raise_for_status()
                response_data = response.json()
            except Exception as e:
                raise ToolInvokeError(str(e))
            
            if 'didyoumeans' in response_data['queryresult']:
                # get the most likely interpretation
                query = ''
                max_score = 0
                for didyoumean in response_data['queryresult']['didyoumeans']:
                    if float(didyoumean['score']) > max_score:
                        query = didyoumean['val']
                        max_score = float(didyoumean['score'])

                params['input'] = query
            else:
                finished = True
                if 'souces' in response_data['queryresult']:
                    return self.create_link_message(response_data['queryresult']['sources']['url'])
                elif 'pods' in response_data['queryresult']:
                    result = response_data['queryresult']['pods'][0]['subpods'][0]['plaintext']

        if not finished or not result:
            return self.create_text_message('No result found')

        return self.create_text_message(result)
    
    def validate_credentials(self, credentails: Dict[str, Any], parameters: Dict[str, Any]) -> None:
        pass