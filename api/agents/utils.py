import json


def get_bot_response(client, model_name, messages, temperature=0):
    input_messages = []
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.0, 
        top_p=0.8,
        max_tokens=2000

    )

# Access the `content` field of the first choice
    content_str = response.choices[0].message.content

    # Parse the JSON string from `content`

    # Access the "message" field within the parsed JSON data
    print(content_str)
    response_message = content_str

    # Print or return only the extracted "message" value
    print(response_message)
    return response_message




def get_emedding(embedding_client, model, text_input):
    output = embedding_client.embeddings.create(
        input=text_input,
        model=model
    )
    embeddings= []
    for embedding_object in output.data:
        embeddings.append(embedding_object.embedding)
    return embeddings    
