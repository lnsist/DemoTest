"""
    selenium设置代理
date: 18-10-11 下午8:05
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile


def proxy_Chrome():
    """
        设置谷歌浏览器代理 -- 无需账号密码验证
    :return:
    """
    # 代理
    proxy = "127.0.0.1:9473"
    # 谷歌浏览器选项
    chrome_options = webdriver.ChromeOptions()
    # 添加代理服务
    chrome_options.add_argument("--proxy-server=http://" + proxy)
    # 创建谷歌浏览器
    browser = webdriver.Chrome(chrome_options)
    # 请求访问
    browser.get("http://httpbin.org/get")


def proxy_Chrome_proofness():
    """
        设置谷歌浏览器代理 -- 需账号密码验证
    :return:
    """
    # ip
    ip = "127.0.0.1"
    # 端口
    port = "9473"
    # 用户名
    username = "lnsist@yeah.net"
    # 密码
    password = "123456"
    # manifest.json配置文件
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """
    # background.js脚本
    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%(ip)s",
                port: %(port)s
            }
        }
    }
    
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
    function callbackFn(details){
        return {
            authCredentials: {
                username: "%(username)s",
                password: "%(password)s"
            }
        }
    }
    
    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ["blocking"]
    )
    """ % {"ip": ip, "port": port, "username": username, "password": password}
    # 文件名, 保存当前配置
    plugin_file = "proxy_auth_plugin.zip"
    # 写入文件
    with zipfile.ZipFile(plugin_file, "w") as zp:
        # manifest.json配置文件
        zp.writestr("manifest.json", manifest_json)
        # background.js脚本
        zp.writestr("background.js", background_js)
    # 获取浏览器选项
    chrom_options = Options()
    # 添加选项
    chrom_options.add_argument("--start-maximized")
    # 设置
    chrom_options.add_extension(plugin_file)
    # 打开谷歌浏览器, 设置选项
    browser = webdriver.Chrome(chrom_options=chrom_options)
    # 请求访问
    browser.get("http://httpbin.org/get")


def proxy_PhantomJS():
    """
        PhantomJS设置代理
    :return:
    """
    # 设置代理
    service_args = [
        "--proxy=127.0.0.1:9473",
        "--proxy-type=http",
        "--proxy-auth=username:password"    # 验证  用户名:密码
    ]
    # 添加代理
    browser = webdriver.PhantomJS(service_args=service_args)
    # 请求访问
    browser.get("http://httpbin.org/get")
    # 输出响应报文
    print(browser.page_source)


if __name__ == '__main__':
    # 设置谷歌浏览器代理 -- 无需账号密码验证
    proxy_Chrome()
    # 设置谷歌浏览器代理 -- 需账号密码验证
    proxy_Chrome_proofness()
