import re
import os

def generate_anchor_link(title):
    # GitHub 錨點生成規則：
    # 1. 移除 ### ❓ 等標記
    # 2. 保留中文字符、英文字母、數字、空格和連字符
    # 3. 移除其他標點符號
    # 4. 轉換為小寫（僅對英文）
    # 5. 將空格替換為連字符
    
    # 移除 markdown 標記
    title = re.sub(r'^#+\s*❓\s*', '', title)
    
    # 保留中文字符、英文字母、數字、空格和連字符，移除其他符號
    title = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbfa-zA-Z0-9\s-]', '', title)
    
    # 清理多餘空格
    title = re.sub(r'\s+', ' ', title).strip()
    
    # 轉換為小寫（僅對英文字符）
    title = ''.join(c.lower() if c.isascii() else c for c in title)
    
    # 將空格替換為連字符
    title = title.replace(' ', '-')
    
    return f"#{title}"

def renumber_and_update_links(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到目錄開始位置
    toc_start_pattern = r'## 📑 (?:Quick Navigation Directory|快速導航目錄)'
    toc_start_match = re.search(toc_start_pattern, content)
    if not toc_start_match:
        print("Could not find Table of Contents section.")
        return

    # 找到目錄結束位置（第一個 --- 後的換行）
    toc_end_pattern = r'---\n'
    toc_end_match = re.search(toc_end_pattern, content[toc_start_match.start():])
    if not toc_end_match:
        print("Could not find end of Table of Contents section.")
        return

    # 分離內容
    before_toc = content[:toc_start_match.start()]
    toc_header = toc_start_match.group(0)
    content_body = content[toc_start_match.start() + toc_end_match.end():]

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
            original_title = re.sub(r'^問題\s*\d+[：:]\s*', '', original_title)
            original_title = re.sub(r'^問題\s*\d+-\d+[：:]\s*', '', original_title)
            
            new_line = f"### ❓ 問題 {part_counter}-{question_counter}：{original_title}"
            new_content_body.append(new_line)
            
            # 為目錄生成連結
            question_anchor = generate_anchor_link(new_line)
            new_toc_links.append(f"- [問題 {part_counter}-{question_counter}：{original_title}]({question_anchor})")
        else:
            new_content_body.append(line)

    # 重建完整內容
    new_toc_section = toc_header + '\n\n' + '\n'.join(new_toc_links) + '\n\n---\n'
    final_content = before_toc + new_toc_section + '\n'.join(new_content_body)

    # 寫回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Successfully updated {file_path}")

if __name__ == '__main__':
    # 檔案路徑
    zh_path = os.path.join('docs', 'zh', 'Six-Keys_Criticality_QA.md')
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