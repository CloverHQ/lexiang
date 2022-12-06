# lexiang

main分支可以异步执行多人任务。
### 使用说明
设置github action secrets
```
// 多人设置
LX_CONFIG:[{"cookie":"xxx","bark_key":"xxx"}, {"cookie":"yyy","bark_key":"yyy"}]
```

### HTTP协议代理设置
1、使用命令直接设置代理
--global 表示全局，不需要可以不加
```
git config --global https.proxy ***
```
例子:
```
# socks
git config --global http.proxy 'socks5://127.0.0.1:1080' 
git config --global https.proxy 'socks5://127.0.0.1:1080'
# http
git config --global http.proxy http://127.0.0.1:1080 
git config --global https.proxy https://127.0.0.1:1080

# 只对github.com使用代理，其他仓库不走代理
git config --global http.https://github.com.proxy socks5://127.0.0.1:1080
git config --global https.https://github.com.proxy socks5://127.0.0.1:1080
# 取消github代理
git config --global --unset http.https://github.com.proxy
git config --global --unset https.https://github.com.proxy
```
2、直接修改~/.gitconfig文件
```
[http]
proxy = socks5://127.0.0.1:1080
[https]
proxy = socks5://127.0.0.1:1080
```
3、取消代理
```
git config --global --unset http.proxy
git config --global --unset https.proxy
```