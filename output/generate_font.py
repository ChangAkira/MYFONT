import fontforge
import os

# ================= 配置区 =================
# 再次改个名，确保万无一失 (避免缓存)
FONT_FAMILY_EN = "MyHandwritingFixed"
FONT_NAME_CN = "我的手写体修复版"
SVG_DIR = "./svg_output"
# =========================================

def main():
    print(f"🚑 正在执行 V4.1 最终修复: {FONT_NAME_CN} ...")
    
    # 1. 新建字体
    font = fontforge.font()
    
    # 2. 【核心修复】强制设置编码环境为 Unicode
    # 这一步能解决“记事本显示不出来”的问题
    font.encoding = 'UnicodeFull'
    
    # 3. 设置基础信息
    font.fontname = FONT_FAMILY_EN
    font.familyname = FONT_FAMILY_EN
    font.fullname = FONT_NAME_CN 
    
    # 4. 设置中文字体名 (让 Word 识别)
    font.appendSFNTName(0x804, 1, FONT_NAME_CN)
    font.appendSFNTName(0x804, 4, FONT_NAME_CN)
    
    # 英文兼容名
    font.appendSFNTName(0x409, 1, FONT_FAMILY_EN)
    font.appendSFNTName(0x409, 4, FONT_FAMILY_EN)

    # 5. 设置排版度量
    font.em = 1000
    font.ascent = 800
    font.descent = 200
    
    # 6. 导入 SVG
    files = [f for f in os.listdir(SVG_DIR) if f.endswith(".svg")]
    total = len(files)
    print(f"📂 正在封装 {total} 个字形...")

    for filename in files:
        try:
            codepoint = int(filename.split(".")[0], 16)
            char = font.createChar(codepoint)
            char.importOutlines(os.path.join(SVG_DIR, filename))
            char.removeOverlap()
            char.width = 1000 
        except Exception:
            pass 

    # 7. 生成 (去掉报错的 flag)
    output_ttf = FONT_NAME_CN + ".ttf"
    
    # 这里的 generate 不需要任何花哨的 flag，默认即可
    # 只要之前的 encoding 设置对了，TTF 就能用
    try:
        font.generate(output_ttf)
        print(f"✅ 成功生成！文件名为：{output_ttf}")
        print("👉 步骤：")
        print("1. 去 C:\\Windows\\Fonts 删除旧的‘我的手写体’系列")
        print("2. 安装这个新字体")
        print("3. 重启 Word，选择【我的手写体修复版】测试")
    except Exception as e:
        print(f"❌ 生成失败: {e}")

if __name__ == "__main__":
    main()