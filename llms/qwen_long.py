import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, BadRequestError
from prompts.extract_file import prompt_file_to_text

class QwenLong():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处替换您的API-KEY
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务base_url
        )

    def call_llm_with_file(self,prompt, file_path):

        file_object = self.client.files.create(file=Path(file_path), purpose="file-extract")

        try:
            # 初始化messages列表
            completion = self.client.chat.completions.create(
                model="qwen-long",
                messages=[
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    # 请将 '{FILE_ID}'替换为您实际对话场景所使用的 fileid
                    {'role': 'system', 'content': f'fileid://{file_object.id}'},
                    {'role': 'user', 'content': prompt}
                ],
                # 所有代码示例均采用流式输出，以清晰和直观地展示模型输出过程。如果您希望查看非流式输出的案例，请参见https://help.aliyun.com/zh/model-studio/text-generation
                stream=True,
                stream_options={"include_usage": True}
            )

            full_content = ""
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content:
                    # 拼接输出内容
                    full_content += chunk.choices[0].delta.content
                    # print(chunk.model_dump())

            return full_content

        except BadRequestError as e:
            print(f"错误信息：{e}")
            print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    load_dotenv()
    qwen = QwenLong()
    file_path = r'D:\照片\b07dee0426598f16535bf78354567b5.jpg'
    rs =qwen.call_llm_with_file(prompt_file_to_text, file_path)
    print(rs)