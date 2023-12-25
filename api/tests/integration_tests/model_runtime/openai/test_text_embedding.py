import os

import pytest

from core.model_runtime.entities.text_embedding_entities import TextEmbeddingResult
from core.model_runtime.errors.validate import CredentialsValidateFailedError
from core.model_runtime.model_providers.openai.text_embedding.text_embedding import OpenAITextEmbeddingModel


def test_validate_credentials():
    model = OpenAITextEmbeddingModel()

    with pytest.raises(CredentialsValidateFailedError):
        model.validate_credentials(
            model='text-embedding-ada-002',
            credentials={
                'openai_api_key': 'invalid_key'
            }
        )

    model.validate_credentials(
        model='text-embedding-ada-002',
        credentials={
            'openai_api_key': os.environ.get('OPENAI_API_KEY')
        }
    )


def test_invoke_model():
    model = OpenAITextEmbeddingModel()

    result = model.invoke(
        model='text-embedding-ada-002',
        credentials={
            'openai_api_key': os.environ.get('OPENAI_API_KEY'),
            'openai_api_base': 'https://api.openai.com'
        },
        texts=[
            "hello",
            "world"
        ],
        user="abc-123"
    )

    assert isinstance(result, TextEmbeddingResult)
    assert len(result.embeddings) == 2
    assert result.usage.total_tokens == 2


def test_get_num_tokens():
    model = OpenAITextEmbeddingModel()

    num_tokens = model.get_num_tokens(
        model='text-embedding-ada-002',
        texts=[
            "hello",
            "world"
        ]
    )

    assert num_tokens == 2
