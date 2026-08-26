import requests
from typing import Optional, Dict, Any

class ClickUpClient:
    """
    Cliente simples para interagir com a API v2 do ClickUp.
    Documentação: https://clickup.com/api/
    """
    BASE_URL = "https://api.clickup.com/api/v2"

    def __init__(self, api_token: str):
        """
        Inicializa o cliente com o Personal Access Token (ou token OAuth).
        """
        self.api_token = api_token
        self.headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json"
        }

    def create_task(self, list_id: str, name: str, description: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Cria uma task (card) em uma lista específica do ClickUp.
        
        Args:
            list_id: ID da Lista (List) onde a task será criada.
            name: Nome da task.
            description: Descrição em texto da task (opcional).
            **kwargs: Outros parâmetros suportados pela API (ex: status, priority, due_date, assignees).
            
        Returns:
            Dict com os dados da task criada em formato JSON.
        """
        url = f"{self.BASE_URL}/list/{list_id}/task"
        
        payload = {
            "name": name,
        }
        
        if description:
            payload["markdown_description"] = description # Usa markdown para formatação
            
        # Adiciona quaisquer outros campos fornecidos (ex: status, priority, etc)
        payload.update(kwargs)
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        # Levanta exceção se o status HTTP for de erro (4xx ou 5xx)
        response.raise_for_status()
        
        return response.json()
