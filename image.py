from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is the name of this tank? All of the provided images contain the same tank."},
                {
                    "type": "image_url",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Mounted_Soldier_System_%28MSS%29.jpg/1200px-Mounted_Soldier_System_%28MSS%29.jpg",
                },
                {
                    "type": "image_url",
                    "image_url": "https://aerospace.honeywell.com/content/dam/aerobt/en/images/horizontal/M1-Abrams-Tank-Banner.jpg",
                },
            ],

        }
    ],
    max_tokens=4096,
)

print(response.choices[0])