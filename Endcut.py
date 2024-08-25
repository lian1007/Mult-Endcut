import cv2
import os
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter.messagebox as messagebox 
import shutil  # 用於移動文件
from PIL import Image  # 用於壓縮圖片

ctk.set_appearance_mode("light")
font_style = ("Microsoft JhengHei", 16, "bold")

def extract_last_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    ret, frame = cap.read()

    if ret:
        # 獲取當前腳本所在目錄
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 生成以 _last_frame 結尾的文件名
        img_name = os.path.splitext(os.path.basename(video_path))[0] + "_last_frame.jpg"
        
        # 使用腳本所在目錄和圖片名稱生成臨時保存路徑
        temp_img_path = os.path.join(script_dir, img_name)

        # 將圖片編碼為 jpg 格式
        success, encoded_image = cv2.imencode('.jpg', frame)

        if success:
            # 將編碼的圖片數據保存到文件
            with open(temp_img_path, 'wb') as f:
                f.write(encoded_image.tobytes())

            # 生成目標路徑，即視頻所在的目錄
            target_dir = os.path.dirname(video_path)
            final_img_path = os.path.join(target_dir, img_name)

            # 移動圖片到視頻所在目錄，覆蓋同名文件（如果存在）
            if os.path.exists(final_img_path):
                os.remove(final_img_path)

            # 移動圖片到視頻所在目錄
            shutil.move(temp_img_path, temp_img_path)
            
            # 生成最終文件名，將 _last_frame 替換為 _尾卡
            final_img_name = img_name.replace("_last_frame", "_尾卡")
            final_new_path = os.path.join(target_dir, final_img_name)
            
            if os.path.exists(final_new_path):
                os.remove(final_new_path)

            # 重命名文件
            os.rename( temp_img_path, final_new_path)
            print(f"圖片已重命名")
            
            # 壓縮圖片
            compress_image(final_new_path)

            print( temp_img_path,final_img_name,final_new_path)
        else:
            print("圖片編碼失敗")

    else:
        print("無法提取最後一幀")

    cap.release()

def compress_image(image_path, quality=75):
    """ 壓縮圖片並保持原名保存 """
    with Image.open(image_path) as img:
        img.save(image_path, quality=quality)
        print(f"圖片已壓縮並保存")

# 拖曳事件
def on_drop(event):
    video_paths = event.data.strip('{}').split('} {')
    for video_path in video_paths:
        if os.path.isfile(video_path):
            # 檢查文件擴展名是否為 mp4 或 mov
            ext = os.path.splitext(video_path)[1].lower()
            if ext in ['.mp4', '.mov']:
                extract_last_frame(video_path)
            else:
                # 彈出警告窗口，提示無效的文件類型
                messagebox.showwarning("無效類型", f"文件類型只支援mp4與mov檔")
        else:
            # 彈出警告窗口，提示無效的文件
            messagebox.showwarning("無效文件", f"無效的文件: {video_path}")

# 創建主視窗，設置背景顏色，加上開啟位置
root = TkinterDnD.Tk()
root.geometry("280x200+200+200")
root.title("影片尾卡擷取器")

# 使用 CustomTkinter 的 CTk 設置背景顏色
frame = ctk.CTkFrame(root, fg_color="#FF8AEB")  # 設置整個窗口背景顏色
frame.pack(fill="both", expand=True)

# 使用 CustomTkinter 創建標籤
label = ctk.CTkLabel(frame, text="請用影片打我", text_color="#f7f7f7", font=font_style)
label.pack(fill="both", expand=True)

# 綁定拖曳事件
frame.drop_target_register(DND_FILES)
frame.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
