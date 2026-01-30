import os
import subprocess
from PIL import Image

# ================= 配置区 =================
# 输入文件夹 ('.' 表示当前文件夹)
INPUT_DIR = '.'
# 输出文件夹
OUTPUT_DIR = './svg_output'
# Potrace 的路径 (如果就在当前文件夹，不用改)
POTRACE_PATH = 'potrace.exe'
# =========================================

def main():
    # 1. 检查 Potrace 是否存在
    if not os.path.exists(POTRACE_PATH):
        print(f"❌ 错误：找不到 {POTRACE_PATH}。")
        print("请去 http://potrace.sourceforge.net/ 下载 Windows 版，")
        print("并将 potrace.exe 复制到这个文件夹里。")
        return

    # 2. 创建输出文件夹
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 3. 扫描所有 PNG 文件
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.png')]
    
    if not files:
        print("❌ 没有找到 PNG 图片，请检查文件夹。")
        return

    print(f"🚀 开始处理，共 {len(files)} 张图片...")

    count = 0
    for file in files:
        # 文件名不含后缀
        name_no_ext = os.path.splitext(file)[0]
        
        input_png = os.path.join(INPUT_DIR, file)
        temp_bmp = os.path.join(OUTPUT_DIR, "temp_for_trace.bmp")
        output_svg = os.path.join(OUTPUT_DIR, name_no_ext + ".svg")

        try:
            # A. 用 Pillow 把 PNG 转为 BMP (Potrace 只能吃 BMP)
            img = Image.open(input_png)
            # 转换为黑白二值图像 (1-bit pixels, black and white)
            # threshold 可以让字迹更清晰，这里用默认转换
            img = img.convert("1") 
            img.save(temp_bmp)

            # B. 调用 Potrace 将 BMP 转为 SVG
            # -s: 输出 SVG
            # --flat: 优化曲线
            subprocess.run([POTRACE_PATH, temp_bmp, "-s", "-o", output_svg], check=True)
            
            print(f"✅ [{count+1}/{len(files)}] 已转换: {output_svg}")
            count += 1
            
        except Exception as e:
            print(f"❌ 处理 {file} 失败: {e}")

    # 清理临时文件
    if os.path.exists(temp_bmp):
        os.remove(temp_bmp)

    print("\n🎉 全部完成！")
    print(f"SVG 文件都在 '{OUTPUT_DIR}' 文件夹里。")

if __name__ == "__main__":
    main()