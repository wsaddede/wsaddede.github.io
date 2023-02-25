import pyttsx3
import openai

# 设置OpenAI API密钥
openai.api_key = "YOUR_API_KEY"

# 初始化语音合成引擎
engine = pyttsx3.init()

# 询问用户需要咨询什么问题
question = input("请问您需要咨询什么问题？")

# 获取AI回答
response = openai.Completion.create(
    engine="davinci",
    prompt=question,
    max_tokens=60
)

# 获取答案
answer = response.choices[0].text.strip()

# 输出答案
print(answer)

# 把答案转换为语音并输出
engine.say(answer)
engine.runAndWait()
