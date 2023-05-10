> 运行环境推荐使用Windows平台

# 条件

- **Python 3.8** (Python 3.9会出错)

- `pip` 版本或者更高

  如果有必要可以升级 `pip`:

  ```shell
  python -m pip install --upgrade pip
  ```
## 相关库

### pytorch

  ```sh
pip install torch==1.5.0+cpu torchvision==0.6.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
  ```

### gRPC

### gRPC

```sh
python -m pip install grpcio
```

#### gRPC tools

Python的gRPC工具包括协议缓冲区编译器`protoc `和用于生成服务器和客户端代码的特殊插件，更多内容查看相关工具的文档。

安装gRPC工具集，运行：

```sh
python -m pip install grpcio-tools
```

### 生成gRPC代码

```sh
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. grpc.proto 
```

如果"grpc_pb2.py"和"grpc_pb2_grpc.py"已经存在，你可以忽略这一步。

### PyCryptodome

PyCryptodome是一个Python的密码学包，包含低级密码原语。它支持Python 2.7、Python 3.5及更新版本。

安装:

```sh
pip install pycryptodome
```

### 其他

```sh
pip install scikit-learnm,scikit-image,pandas,matplotlib,scipy
```



## 准备数据集

### MNIST

下载数据集http://yann.lecun.com/exdb/mnist/

安装 mnist

```sh
$ pip install mnist
```

统一解析mnist数据集

```sh
cd mnist_data
python3 mnist_parser
```



# 运行

## 生成密钥与准备ip列表

```sh
#打开文件，设置主函数中makejson()的参数为5
python key_Generate.py
```

## 参数调整

调用不同的方案在`main.py`中更换主函数中的`MNIST_training_DP/MNIST_training_pure/MNIST_training_krum`，参数表示拜占庭节点所占比例



## 运行

```sh
打开终端1, 运行
$python3 main.py 127.0.0.1:50051 50051
打开终端2, 运行
$python3 main.py 127.0.0.1:50053 50053
打开终端一3, 运行
$python3 main.py 127.0.0.1:50053 50053
```

或运行`test.bat`文件（需要修改代码中的文件路径）

## 生成图像

```sh
$ cd log
$ python figure.py 
$ python timefigure.py 
```



### 附录

也许你需要的设置

```shell
#更换pip-py镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

# DIPDL
