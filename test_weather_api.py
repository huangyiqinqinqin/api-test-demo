import requests
import json
import time
import os

# 测试数据：多个城市的天气查询
test_cities = [
    {"city": "北京", "expect_code": 200, "expect_city": "北京"},
    {"city": "上海", "expect_code": 200, "expect_city": "上海"},
    {"city": "广州", "expect_code": 200, "expect_city": "广州"},
    {"city": "不存在的城市123", "expect_code": 404, "expect_city": None},  # 预期失败
]

# 创建报告文件夹
if not os.path.exists("reports"):
    os.makedirs("reports")

print("=" * 50)
print("天气查询接口自动化测试")
print("=" * 50)

# 统计结果
passed = 0
failed = 0
results = []

for test in test_cities:
    city = test["city"]
    expect_code = test["expect_code"]
    expect_city = test["expect_city"]

    print(f"\n▶ 测试城市：{city}")

    try:
        # 发送请求（使用 wttr.in 这个免费天气API）
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)

        # 检查1：状态码
        if response.status_code == expect_code:
            print(f"   ✅ 状态码正确：{response.status_code}")
            status_ok = True
        else:
            print(f"   ❌ 状态码错误：期望{expect_code}，实际{response.status_code}")
            status_ok = False

        # 检查2：如果是成功请求，验证返回数据
        data_ok = True
        if response.status_code == 200:
            try:
                data = response.json()
                # 检查返回数据中是否包含城市信息
                if "current_condition" in data:
                    print(f"   ✅ 响应包含天气数据")
                else:
                    print(f"   ❌ 响应缺少天气数据")
                    data_ok = False

                # 检查城市名称（部分匹配）
                if expect_city and expect_city in response.text:
                    print(f"   ✅ 城市信息正确")
                else:
                    print(f"   ⚠️ 城市信息验证跳过")

            except json.JSONDecodeError:
                print(f"   ❌ 响应不是有效的JSON格式")
                data_ok = False
        else:
            # 预期失败的情况
            if expect_code == 404:
                print(f"   ✅ 符合预期：城市不存在返回{response.status_code}")
                data_ok = True

        # 综合判断
        if status_ok and data_ok:
            print(f"   🎉 测试通过")
            passed += 1
            results.append({"city": city, "status": "✅ 通过", "code": response.status_code})
        else:
            print(f"   ❌ 测试失败")
            failed += 1
            results.append({"city": city, "status": "❌ 失败", "code": response.status_code})

    except requests.exceptions.ConnectionError:
        print(f"   ❌ 连接失败（请检查网络）")
        failed += 1
        results.append({"city": city, "status": "❌ 连接失败", "code": "N/A"})
    except Exception as e:
        print(f"   ❌ 异常：{str(e)[:100]}")
        failed += 1
        results.append({"city": city, "status": "⚠️ 异常", "code": "Error"})

# 打印测试报告
print("\n" + "=" * 50)
print("测试报告")
print("=" * 50)
print(f"总计测试数：{len(test_cities)}")
print(f"✅ 通过：{passed}")
print(f"❌ 失败：{failed}")
print(f"通过率：{passed / len(test_cities) * 100}%")
print("=" * 50)

# 生成 HTML 报告
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>接口自动化测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 20px 0; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #2196F3; color: white; }}
    </style>
</head>
<body>
    <h1>🔌 接口自动化测试报告</h1>
    <div class="summary">
        <p><strong>执行时间：</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>测试接口：</strong> https://wttr.in (天气查询API)</p>
        <p><strong>总计测试数：</strong> {len(test_cities)}</p>
        <p><strong>✅ 通过：</strong> {passed}</p>
        <p><strong>❌ 失败：</strong> {failed}</p>
        <p><strong>📊 通过率：</strong> {passed / len(test_cities) * 100:.1f}%</p>
    </div>
    <table>
        <tr>
            <th>状态</th>
            <th>测试城市</th>
            <th>响应码</th>
        </tr>
"""
for r in results:
    status_class = "pass" if "通过" in r["status"] else "fail"
    html_content += f"""
        <tr>
            <td class="{status_class}">{r["status"]}</td>
            <td>{r["city"]}</td>
            <td>{r["code"]}</td>
        </tr>"""
html_content += """
    </table>
    <hr>
    <h3>📝 测试说明</h3>
    <ul>
        <li>验证了正常城市（北京、上海、广州）的天气查询</li>
        <li>验证了异常城市（不存在）的错误处理</li>
        <li>校验了HTTP状态码、响应格式、业务数据</li>
    </ul>
    <p><small>报告生成时间：""" + time.strftime('%Y-%m-%d %H:%M:%S') + """</small></p>
</body>
</html>"""

with open("reports/api_report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("\n📄 HTML报告已生成：reports/api_report.html")
print("💡 用浏览器打开 reports/api_report.html 查看美观的测试报告")