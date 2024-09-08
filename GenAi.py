from groq import Groq

client = Groq(
    api_key="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"
)
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "summerize india's news for today"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
