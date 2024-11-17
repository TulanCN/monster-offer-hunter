from dashscope import Generation


preprompt = """任务：- 你需要进行文本信息提取和分类的任务。
工作流：
-先对文本进行分类，分为两类：面试经验分享、求助问答
-提取信息时，如果涉及多个公司，则则每个公司分开提取。
-如果是【面试经验分享】的文本，提取出如下角度的信息：公司、岗位、薪资以及福利待遇、评价。
-如果是【求助问答】的文本，提取出如下角度的信息：公司、岗位、薪资、问题
回答限制：
- 回答请尽量精简。如果没有某个角度的信息，则该角度不输出。回答中的主语使用我。以下是文本："""

def call_with_messages(api_key, prompt):

    messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': preprompt + "[" + prompt + "]"}
    ]

    response = Generation.call(
        api_key=api_key,
        model="qwen-turbo",
        messages=messages,
        result_format="message"
    )

    if response.status_code == 200:
        return response.output.choices[0].message.content
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

def read_text_from_file(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line.strip())
    return lines

def save_responses_to_file(api_key, input_texts, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for text in input_texts:
            response = call_with_messages(api_key, text)
            f.write(response + '\n')

if __name__ == "__main__":
    api_key = input("Enter the API key: ")
    file_path = "../Data/cleaned/cleaned_校招.txt"   #input filename
    output_file_path = "extracted_校招.txt"  #output filename
    input_texts = read_text_from_file(file_path)
    save_responses_to_file(api_key, input_texts, output_file_path)