import os
import json

def process_directory(directory):
    """递归处理给定目录下的所有 JSON 文件。"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                process_file(file_path)

def process_file(file_path):
    """读取 JSON 文件，将 'teacher_score' 重命名为 'model_score' 并保存。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        modified = False
        
        # 检查 'example' 是否在 data 中并且是一个列表
        if 'example' in data and isinstance(data['example'], list):
            for item in data['example']:
                if isinstance(item, dict):
                    if 'model_score' in item:
                        # 重命名字段同时保留其值
                        item['teacher_score'] = item.pop('model_score')
                        modified = True
                    
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"已更新: {file_path}")
            
    except json.JSONDecodeError:
        print(f"解码 JSON 文件时出错: {file_path}")
    except Exception as e:
        print(f"处理文件时出错 {file_path}: {e}")

if __name__ == "__main__":
    # 获取项目根目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    subresults_dir = os.path.join(project_root, 'subresults')
    
    if os.path.exists(subresults_dir):
        print(f"开始处理目录中的文件: {subresults_dir}")
        process_directory(subresults_dir)
        print("处理成功完成。")
    else:
        print(f"错误: 目录不存在: {subresults_dir}")
