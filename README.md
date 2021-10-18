# Python script for creating advices(may be demotivator later)
FOR __ENGLISH__ TEXT JUST COPY PASTE THIS TEXT TO GOOGLE TRANSLATOR  
Скрипт работает на Windows и на Linux, тестировался на python 3.7  
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
