# Python script for creating advices(may be demotivator later)
FOR __ENGLISH__ TEXT JUST COPY PASTE THIS TEXT TO GOOGLE TRANSLATOR  
Скрипт работает на Windows и на Linux, тестировался на python 3.7  
***
![temp](https://user-images.githubusercontent.com/90105380/137776669-3486609f-2ee2-48b5-bfdb-238832d9cdc4.png)
![temp](https://user-images.githubusercontent.com/90105380/137777312-528bc352-a865-47a1-926c-76d4c18e23fa.gif)
***
__Необходимые библиотеки:__  
+ textwrap    
+ BytesIO  
+ requests  
+ pillow  
+ pyvips  
+ imageio  
+ os (гений)  
+ shutil (уже не помню нахуя, ну пусть будет :D)  
***
__Методы для обработки:__  
advice_slow:  
```Для медленной обработки фото/gif(Сохраняет только в файл!). ПОТРЕБЛЯЕТ МАЛО ОПЕРАТИВНОЙ ПАМЯТИ.```  
advice_fast:  
```Для быстрой обработки маленьких фото/gif. ПОТРЕБЛЯЕТ МНОГО ОПЕРАТИВНОЙ ПАМЯТИ, но очень быстр.```  
***
Аргументы:  
(WATERMARK НЕ РЕАЛИЗОВАН!!!)
|Метод|Аргументы|
|-----|--------|
|advice_slow|path, bottom_text, top_text, font_path, font_size, stroke_width, url, RESULT_FILENAME, TEMP_FOLDER, watermark, gt_bytes, can_resize|
|advice_fast|path, bottom_text, top_text, font_path, font_size, stroke_width, url, RESULT_FILENAME, watermark, rt_bytes, can_resize|
