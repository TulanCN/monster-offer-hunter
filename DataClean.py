import re

def process_files(input_files, output_file_path):
    all_results = []
    for file_path in input_files:
        result = []
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith('Full Post Text:'):
                    full_post_text = lines[i].split('Full Post Text: ')[1].strip()
                    if full_post_text!= "No post content available":
                        # Use regular expressions to remove links and labels.
                        full_post_text = re.sub(r'http\S+', '', full_post_text)
                        full_post_text = re.sub(r'#\S+#', '', full_post_text)
                        result.append(full_post_text)
                i += 1
            all_results.extend(result)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for text in all_results:
            output_file.write(text + '\n')

if __name__ == "__main__":
    file_path = ['秋招.txt', '校招.txt', '面经.txt']
    output_file_path = 'document.txt'
    process_files(file_path, output_file_path)
