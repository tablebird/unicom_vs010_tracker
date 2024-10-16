# 联通华盛路由器-VS010 设备追踪

在Home Assistant里使用的联通华盛路由器-VS010进行设备追踪

[![hacs_badge](https://img.shields.io/badge/Home-Assistant-%23049cdb)](https://www.home-assistant.io/)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## 安装

打开HACS下载**联通华盛路由器vs010**

[![Download repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository?owner=tablebird&repository=unicom_vs010_tracker&category=Integration)

在`configuration.yaml`添加如下内容配置路由信息进行设备追踪
```yaml
device_tracker:
  - platform: unicom_vs010_tracker   # 插件名称
    host: 192.168.1.1                # vs010路由的ip或域名 
    username: user                   # 登录用户名
    password: admin                  # 登录密码
    only_wireless: false             # 可选 是否只包含无线设备 (默认为true 只有无线设备)
    alias:                           # 可选 设备别名 部分设备访问网络不提供名称 
      8A:A9:12:23:33:12: android     # 格式  mac地址: 别名
```