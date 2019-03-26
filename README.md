# generateCarPlate
generate Car Plate data for PR/OCR training

## 国内蓝色普通车牌生成脚本，忘了参考过哪里的代码

## 想法：
1.把生成的字符串写到蓝色车牌模版照片上，生成车牌；
2.把车牌照片放到背景照片上；
3.增加旋转、噪声，参见 def generate（）

## 用法：
python genCarPlate.py

### param：
```
--根据自己的训练要求 照片大小即背景照片(NoPlates/)设置为了256*128，按需修改
--为了使得车牌占比约为80% 设置车牌大小为(220, 70)，按需修改
--每个省份生成照片数量设置IMG_COUNT_PER_PROVINCE =
--为了使得每个省份中每个城市的车牌数量均衡，即车牌汉字后的第一个字母分布平均，
   参见 genplate.py：38行
   i = iter // IMG_COUNT_PER_PROVINCE
   iterChar = (iter % IMG_COUNT_PER_PROVINCE) // 9
```
