# 接口自动化测试项目

## 项目简介
基于 Python + Requests + Postman + JMeter 的接口自动化测试框架，对天气查询 API 进行功能验证和性能测试。

## 功能特性
- Requests 脚本：多城市参数化测试、状态码校验、响应结构校验
- Postman：接口调试、断言验证、Collection 管理
- JMeter：10用户并发性能测试，验证响应时间和错误率
- 自动生成 HTML 测试报告

## 发现的问题
测试发现，API 对于不存在的城市（如"不存在的城市123"）返回 200 状态码而非预期的 404，说明 API 的异常处理可以进一步优化。

## 环境配置
```bash
pip install requests
```

## 运行测试
```bash
python test_weather_api.py
```

## 测试报告
执行后会在 reports/ 目录生成 HTML 报告。

## JMeter性能测试
- 线程数：10
- 循环次数：2
- 平均响应时间：<1000ms
- 错误率：0%
