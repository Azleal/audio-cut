# 音频裁切(云函数版)
> 该工程使用了`ffmpeg`进行音频裁切, 并上传腾讯cos
> 工程部署至腾讯云函数

### 原理说明
1. 后端使用`ffmpeg`对音频进行裁切. 
2. 由于裁切可能耗时较长, 因此裁切是异步进行的. 提前生成将要上传的`key`.
3. 前端拿到裁切之后的`key`必须先进行文件存在性检测. 使用`query action`接口进行检查


### 准备工作 

#### 1. 申请具有cos读写权限, 云函数读写权限的子账号(ak/sk)

#### 2. 配置, 环境变量
> 以下变量需要配置到环境变量中
- cos ak/sk: 可以访问cos的secretId, secretKey,
    - COS_SECRETID
    - COS_SECRETKEY
- region 区域: 要访问的bucket所在的区域
    - COS_REGION
- cos appId: 
    - COS_APPID
  
#### 3. 获取`ffmpeg`可执行程序
> 从 [这里](https://raw.githubusercontent.com/tencentyun/serverless-demo/master/Python3.6-VideoToRTMP/src/ffmpeg) 下载`ffmpeg`可执行程序. 
> 重命名为`ffmpeg`. 放置在`~/Desktop/serverless/usr/bin/`文件夹下.

#### 4. 准备python依赖
> 1. 将项目中的`requirements.txt`文件放在`~/Desktop/serverless/requirements/`文件夹下.
> 2. `cd ~/Desktop/serverless/requirements/`
> 3. `pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ -t .`


### 云函数部署步骤 

#### 1. 新建层
> 1. 控制台->云函数->高级能力->层->新建
> 2. 新建第一个层(ffmpeg), 以上传文件夹的形式,上传`~/Desktop/serverless/usr/`目录. 该层的作用: 提供`ffmpeg`可执行程序.
> 3. 新建第二个层(audio_cut_requirements), 以上传文件夹的形式,上传`~/Desktop/serverless/requirements/`目录. 该层的作用: 提供工程依赖的python包.

#### 2. 新建云函数
> 1. 控制台->云函数->函数服务->新建->自定义创建
> 2. 基础配置: 注意环境选择`Python 3.6`. 其他项自定义.
> 3. 函数代码: 执行方法选择`audio_cut_handler_index.main_handler`. 提交方法, 选择文件夹方式上传, 上传该工程.
> 4. 环境变量按照**准备工作**中的环境变量要求配置.
> 5. 点击完成

#### 3. 配置触发器
> 1. 进入刚创建好的云函数
> 2. 左侧`触发管理` -> `创建触发器`. 触发方式选择: `API网关触发`. 提交确认.
> 3. 获取到**访问路径**: 这里假设`https://access-url`

#### 4. 访问验证

> ##### 1. 裁切验证(cut action)
```shell
curl --location --request POST 'https://access-url?action=cut' \
--header 'Content-Type: application/json' \
--data-raw '{
"bucket":"BUCKET_NAME_WITH_APPID",
"key":"FILE_KEY",
"start":10,
"duration":20}
'
```
> 替换其中的`https://access-url`, `bucket`, `key`
成功示例返回值
```json
{
    "bucket": "BUCKET_NAME_WITH_APPID",
    "key": "ALTERED_FILE_KEY",
    "message": "success"
}
```

> ##### 2. 裁切结果验证(query action)
```shell
curl --location --request GET 'https://access-url?action=query' \
--header 'Content-Type: application/json' \
--data-raw '{
    "bucket": "BUCKET_NAME_WITH_APPID",
    "key": "ALTERED_FILE_KEY"
}'
```

> 成功示例返回值
```json
{
    "bucket": "BUCKET_NAME_WITH_APPID",
    "key": "ALTERED_FILE_KEY",
    "message": "success"
}
```

> 失败示例返回值
```json
{
    "bucket": null,
    "key": null,
    "message": "fail"
}
```

### 参考
> 1. [ffmpeg.org](http://ffmpeg.org/ffmpeg.html) 
> 2. [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)