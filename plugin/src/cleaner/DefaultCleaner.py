import re
import time
import emoji
import jieba

def process_files(input_files, output_prefix):
    all_results = []
    for file_path in input_files:
        result = []
        now = time.strftime("%Y-%m-%d", time.localtime())
        file_name = f"{file_path}_{now}.txt"
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith('Full Post Text:'):
                    full_post_text = clean_text(lines[i].split('Full Post Text: ')[1].strip())
                    if full_post_text:
                        result.append(full_post_text)
                i += 1
            all_results.extend(result)
        output_file_name = output_prefix + file_path + '.txt'
        with open(output_file_name, 'w', encoding='utf-8') as output_file:
            for text in all_results:
                output_file.write(text + '\n')


def clean_text(text):
    if text != "No post content available":
        # Use regular expressions to remove links and labels.
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'#\S+#', '', text)
        # 移除emoji
        text = remove_emojis(text)
        # 移除特殊字符
        # text = re.sub(r'[^\w\s]', '', text)
        # 去掉多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return None

def remove_emojis(text):
    return emoji.demojize(text).replace(':', '')

def change_company_name(text):
    # 加载自定义词典
    jieba.load_userdict("user_dict.txt")

    # 示例文本
    text = "公司:字节跳动岗位:算法工程师薪资:30k✖️15Base地:北京"

    # 分词
    words = jieba.cut(text)

    # 将分词结果转换为列表
    words_list = list(words)

    # 定义需要替换的词语及其替换内容
    replace_dict = {
        "字节跳动": "某科技公司",
        "算法工程师": "工程师"
    }

    # 替换词语
    replaced_text = [replace_dict.get(word, word) for word in words_list]


if __name__ == "__main__":
    file_path = ["秋招", "校招", "面经", "算法工程师","Java后端开发","前端开发","硬件开发","软件开发"]   #input filename
    output_prefix = 'cleaned_'   #output filename
    process_files(file_path, output_prefix)
