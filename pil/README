
### 验证码图像识别参考：
    https://www.cnblogs.com/qqandfqr/p/7866650.html
    https://www.jianshu.com/p/41127bf90ca9
    [OpenCV安装参考](https://blog.csdn.net/qq_41185868/article/details/79675875)

### Win7 64位导入opencv提示“ImportError: DLL load failed: 找不到指定的模块。”
    解决方案参考：https://blog.csdn.net/cskywit/article/details/81513066#commentBox
    找出依赖，添加依赖的dll，依赖的dll放在Lib/site-packages/cv2/ 目录下
    api-ms-win-downlevel-shlwapi-l1-1-0.rar/win7/System32/api-ms-win-downlevel-shlwapi-l1-1-0.dll

### 安装Tesseract，
	https://blog.csdn.net/wang_hugh/article/details/80760940
	https://www.cnblogs.com/hupeng1234/p/7136442.html
	去https://github.com/tesseract-ocr/tesseract/wiki下载对应的版本，修改 pytesseract.py文件中
	tesseract_cmd = 'tesseract'
	将tesseract修改为安装路径,或在代码中声明

### 验证码图像一般流程
    step1: 图像采集
    step2: 图像处理   灰度化--> 二值化 --> 去噪 --> 倾斜度矫正 --> 字符切割 --> 归一化
    step3: 图像识别   提取字符特征 --> 样本训练 --> 识别
    step4: 输出结果

    (1)自适应阈值二值化 ：效果不错
    (2)去除边框 ：效果不错
    (3)对图片进行干扰线降噪   ：部分图片去噪效果不怎么理想，需要进一步优化
    (4)对图片进行点降噪 ：效果不错
    (5)切割的位置
       如果有粘连字符，如果一个字符的长度过长就认为是粘连字符，并从中间进行切割
       切割字符，要想切得好就得配置参数，通常 1 or 2 就可以   ： 切割效果不太理想(切割有大问题)
    (8)识别验证码：非常不理想

    1，修改切割效果，改为按固定宽度和高度切割
    2，识别改为按libsvm分类训练识别(0-9,a-z)

    图片属性：
        每张图片宽高： 100px，42px
        图片整体字符宽高：69px,29px 69px 42px
        单个字符宽高：18px,29px      16px,42px


    n样本有问题