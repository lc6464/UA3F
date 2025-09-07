import datetime
import ipaddress
from flask import Flask, request, jsonify

# 创建 Flask 应用实例
app = Flask(__name__)

@app.route('/')
def get_request_info():
    """
    处理根路径的GET请求，返回客户端的请求信息。
    """
    # --- 1. 获取时间 ---
    # 获取当前的UTC时间，并格式化为 ISO 8601 标准，以 'Z' 结尾
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    time_str = now_utc.isoformat().replace('+00:00', 'Z')

    # --- 2. 获取IP信息 ---
    # 注意：如果应用部署在反向代理（如 Nginx）之后，
    # request.remote_addr 可能是代理的IP。
    # 更可靠的方式是检查 'X-Forwarded-For' 头，但为简单起见，我们这里直接使用 remote_addr。
    client_ip = request.remote_addr

    # 判断IP地址是IPv4还是IPv6
    try:
        ip_obj = ipaddress.ip_address(client_ip)
        ip_family = f"IPv{ip_obj.version}"
    except ValueError:
        ip_family = "Unknown" # 如果IP地址无效

    # 获取请求协议
    protocol = request.environ.get('SERVER_PROTOCOL', 'Unknown')

    # --- 3. 获取User-Agent相关信息 ---
    # 从请求头中获取信息，如果某个头不存在，则返回 None
    ua_string = request.headers.get('User-Agent')
    sec_ch_ua = request.headers.get('Sec-Ch-Ua')
    sec_ch_ua_mobile = request.headers.get('Sec-Ch-Ua-Mobile')
    sec_ch_ua_platform = request.headers.get('Sec-Ch-Ua-Platform')

    # --- 4. 组装返回的JSON数据 ---
    response_data = {
        "time": time_str,
        "ip": {
            "address": client_ip,
            "family": ip_family,
            "protocol": protocol
        },
        "ua": {
            "user-agent": ua_string,
            "sec-ch-ua": sec_ch_ua,
            "sec-ch-ua-mobile": sec_ch_ua_mobile,
            "sec-ch-ua-platform": sec_ch_ua_platform
        }
    }

    # 使用 jsonify 将字典转换为JSON响应
    return jsonify(response_data)

# --- 主程序入口 ---
if __name__ == '__main__':
    # 启动应用，开启调试模式
    # 在生产环境中，应使用 Gunicorn 或 uWSGI 等WSGI服务器
    app.run(host='0.0.0.0', port=5000)