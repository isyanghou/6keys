import re
import os

def generate_anchor_link(title):
    # 移除標點符號、空格，並轉換為小寫
    # 這是 GitHub 生成錨點連結的通用規則
    title = re.sub(r'[^一-龥a-zA-Z0-9\s-]', '', title).strip()
    title = title.lower().replace(' ', '-')
    return f"#{title}"

def renumber_and_update_links(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分離目錄和主要內容
    # 我們假設目錄以 `## 📑 Quick Navigation Directory` 或 `## 📑 快速導航目錄` 開始
    # 並以 `---` 分隔線結束
    toc_pattern = re.compile(r'(## 📑 (?:Quick Navigation Directory|快速導航目錄).*?)(---)', re.DOTALL)
    match = toc_pattern.search(content)
    if not match:
        print("Could not find Table of Contents section.")
        return

    toc_header = match.group(1)
    content_body = content[match.end(2):]

    part_counter = 0
    question_counter = 0
    new_content_body = []
    new_toc_links = []

    # 處理主要內容，重新編號並收集連結
    for line in content_body.split('\n'):
        part_match = re.match(r'## (.*?)Part (\w+):(.*)', line)
        question_match = re.match(r'### ❓ (.*)', line)

        if part_match:
            part_counter += 1
            question_counter = 0
            new_content_body.append(line)
            # 添加 Part 到目錄
            part_title = line.strip()
            part_anchor = generate_anchor_link(part_title)
            new_toc_links.append(f"### [{part_title}]({part_anchor})")
        elif question_match:
            question_counter += 1
            original_title = question_match.group(1).strip()
            # 移除舊編號 (如果有的話)
            original_title = re.sub(r'^\d+-\d+\.\s*', '', original_title)
            
            new_title_text = f"{part_counter}-{question_counter}. {original_title}"
            new_line = f"### ❓ {new_title_text}"
            new_content_body.append(new_line)
            
            # 為目錄生成連結
            question_anchor = generate_anchor_link(new_line)
            new_toc_links.append(f"- [{new_title_text}]({question_anchor})")
        else:
            new_content_body.append(line)

    # 重建目錄
    new_toc_section = toc_header + '\n' + '\n'.join(new_toc_links) + '\n\n---\n'

    # 合併新的目錄和內容
    final_content = new_toc_section + '\n'.join(new_content_body)

    # 寫回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Successfully updated {file_path}")

if __name__ == '__main__':
    # 檔案路徑
    zh_path = os.path.join('..', '六鑰臨界問與答.md')
    en_path = os.path.join('docs', 'en', 'Six-Keys_Criticality_QA.md')

    # 檢查並處理中文文件
    if os.path.exists(zh_path):
        renumber_and_update_links(zh_path)
    else:
        print(f"Chinese file not found at {zh_path}")

    # 檢查並處理英文文件
    if os.path.exists(en_path):
        renumber_and_update_links(en_path)
    else:
        print(f"English file not found at {en_path}")