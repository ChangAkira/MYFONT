import os
import shutil

# ================= 配置区 =================
# 你的汉字表文件名
CHAR_FILE = "chars.txt"
# 你的原始图片前缀（Krita 导出的动画序列通常是 frame_xxxx.png）
IMG_PREFIX = "frame" 
# 图片格式
IMG_EXT = ".png"
# =========================================

def main():
    # 1. 读取汉字表
    try:
        with open(CHAR_FILE, "r", encoding="utf-8") as f:
            # 读取所有内容，并去掉换行符、空格，只保留字符
            content = f.read().replace('\n', '').replace('\r', '').replace(' ', '')
    except FileNotFoundError:
        print(f"❌ 错误：找不到 {CHAR_FILE}，请确认文件在当前目录下。")
        return

    # 2. 获取所有对应的图片文件
    # 逻辑：列出当前目录下所有以 frame_ 开头的 png，并按名称排序
    files = [f for f in os.listdir('.') if f.startswith(IMG_PREFIX) and f.endswith(IMG_EXT)]
    files.sort() # 关键！确保 frame_0001 对应第一个字

    print(f"📊 统计：找到 {len(files)} 张图片，字符表中有 {len(content)} 个字。")

    # 安全检查
    if len(files) == 0:
        print("❌ 错误：没找到图片，请检查 Krita 导出的文件名是否正确。")
        return

    # 3. 开始重命名
    count = 0
    for i, filename in enumerate(files):
        # 如果图片多于汉字，就停止，防止报错
        if i >= len(content):
            print(f"⚠️ 警告：图片比汉字多，第 {i+1} 张图片及之后将不被处理。")
            break
        
        char = content[i]
        
        # === 核心：获取 Unicode 编码 ===
        # ord('我') = 25105
        # hex(25105) = '0x6211'
        # [2:] 去掉 '0x' -> '6211'
        # .upper() -> '6211' (FontForge 习惯大写)
        unicode_hex = hex(ord(char))[2:].upper()
        
        # 新文件名：Unicode.png (例如 6211.png)
        new_name = f"u{unicode_hex}{IMG_EXT}" # 有些脚本喜欢加 'u' 前缀，有些不用。
        # 这里我们用纯数字+字母，或者为了保险起见，用 u6211.png
        # 建议使用纯十六进制：
        new_name = f"{unicode_hex}{IMG_EXT}"

        try:
            # 为了防止覆盖，我们不直接重命名，而是复制到一个新文件夹 'output'
            if not os.path.exists('output'):
                os.makedirs('output')
            
            src = filename
            dst = os.path.join('output', new_name)
            
            shutil.copy(src, dst)
            print(f"✅ [{i+1}] {char} -> {new_name}")
            count += 1
        except Exception as e:
            print(f"❌ 处理 {char} 时出错: {e}")

    print(f"\n🎉 完成！请去 'output' 文件夹查看结果。")
    print(f"共生成 {count} 个以 Unicode 命名的文件。")

if __name__ == "__main__":
    main()