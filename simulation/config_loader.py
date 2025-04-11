import yaml

def load_config(file_path):
    """加载配置文件"""
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config