from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController
from core.tools.errors import ToolProviderCredentialValidationError

from core.tools.provider.builtin.time.tools.current_time import CurrentTimeTool

from typing import Any, Dict, List

class WikiPediaProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: Dict[str, Any]) -> None:
        try:
            CurrentTimeTool().invoke(
                user_id='',
                tool_paramters={},
                credentials=credentials,
                prompt_messages=[]
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))