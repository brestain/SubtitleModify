# 功能
## 平移字幕
- 操纵字幕文件, 实现字幕的平移, 以和视频匹配. 
    有时候下载好了视频和字幕, 却发现找到的字幕和视频没有对齐, 而是有几秒的不同步, 于是写了一个小脚本来处理不同步的字幕.  
- 我测试了*.srt *.ass都可以用.    
- 已打包.exe文件, 不需要安装python环境.
## 自动修改字幕文件名
- 选择字幕文件或文件夹(相当于选择文件夹下所有字幕文件*.srt *.sub *.ass *.ssa), 去同级文件夹下根据文件夹名的SxxExx匹配对应的视频文件, 将字幕文件的文件名修改为和匹配的视频文件相同.

# 使用
## 平移字幕
1. **在release中下载并双击打开SubtitleModify.exe文件**
   ![image](https://github.com/brestain/SubtitleModify/blob/main/pics/Snipaste_2024-06-06_00-48-41.png)
   ![image](https://github.com/brestain/SubtitleModify/blob/main/pics/Snipaste_2024-12-21_18-31-33.png)
2. **确定时间偏移量, 我用的是potplayer, 在里面可以手动临时调整字幕偏移量, 快捷键是逗号和句号, 调整到匹配后就获得了正确的时间偏移量**
   ![image](https://github.com/brestain/SubtitleModify/blob/main/pics/Snipaste_2024-06-05_21-17-44.png)
3. **选择字幕文件和输入时间偏移量(秒)如想要提前2.5秒则输入-2.5**
   ![image](https://github.com/brestain/SubtitleModify/blob/main/pics/Snipaste_2024-06-05_21-12-01.png)
4. **应用时间偏移**
   ![image](https://github.com/brestain/SubtitleModify/blob/main/pics/Snipaste_2024-06-05_21-12-43.png)
5. **偏移后的字幕文件会和原字幕文件在相同的位置,命名为源文件名+时间偏移量**
   ![image](https://github.com/brestain/SubtitleModify/blob/main/pics/Snipaste_2024-06-05_21-17-07.png)
## 自动修改字幕文件名
1. **在release中下载并双击打开changeSrtName.exe文件**
2. **字幕文件和视频文件名字不同,但是都有S01E01**
  ![image](https://github.com/brestain/SubtitleModify/blob/main/pics/Snipaste_2024-12-21_18-36-50.png)
3. **选择文件或者文件夹,点击开始调整自动启动**
  ![image](https://github.com/brestain/SubtitleModify/blob/main/pics/Snipaste_2024-12-21_18-34-29.png)
