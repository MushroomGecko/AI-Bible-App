from typing import Union
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer

# Load the NoInstruct small embedding model
model = AutoModel.from_pretrained("avsolatorio/NoInstruct-small-Embedding-v0")
tokenizer = AutoTokenizer.from_pretrained("avsolatorio/NoInstruct-small-Embedding-v0")

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


def get_embedding(text: Union[str, list[str]], mode: str = "sentence"):
    """
    Get embeddings for text using NoInstruct-small-Embedding-v0 model.
    
    Args:
        text: String or list of strings to embed
        mode: Either "query" or "sentence" - determines the pooling strategy
    
    Returns:
        torch.Tensor containing the embeddings
    """
    model.eval()

    assert mode in ("query", "sentence"), f"mode={mode} was passed but only `query` and `sentence` are the supported modes."

    if isinstance(text, str):
        text = [text]

    inp = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    # Move input tensors to the same device as the model
    inp = {k: v.to(device) for k, v in inp.items()}

    with torch.no_grad():
        output = model(**inp)

    # The model is optimized to use the mean pooling for queries,
    # while the sentence / document embedding uses the [CLS] representation.

    if mode == "query":
        vectors = output.last_hidden_state * inp["attention_mask"].unsqueeze(2)
        vectors = vectors.sum(dim=1) / inp["attention_mask"].sum(dim=-1).view(-1, 1)
    else:
        vectors = output.last_hidden_state[:, 0, :]

    return vectors


def embed_documents(docs, embed_type="sentence"):
    """
    Compute embeddings for documents.
    
    Args:
        docs: List of document strings
        embed_type: Either "query" or "sentence"
    
    Returns:
        torch.Tensor containing the embeddings
    """
    # Compute embeddings
    embeds = get_embedding(docs, mode=embed_type)
    return embeds

