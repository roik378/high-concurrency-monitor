import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr  # <--- 引入这个标准工具

# ================= 配置区域 (请务必修改为你的真实信息) =================
MAIL_HOST = "smtp.qq.com"
MAIL_USER = "411231859@qq.com"   # ⚠️ 必须是你开启 SMTP 服务的那个 QQ 邮箱
MAIL_PASS = "vtkenyqtundzbjef"         # ⚠️ 必须是授权码 (不是 QQ 密码)
RECEIVERS = ["411231859@qq.com"]  # 接收者
# =================================================================

def send_email(title, content):
    try:
        # 1. 创建邮件对象
        message = MIMEText(content, 'html', 'utf-8')
        
        # 2. 设置标准信头 (RFC Compliant Headers)
        # formataddr 会自动处理特殊字符和编码，生成类似 "NikeBot <abc@qq.com>" 的标准格式
        message['From'] = formataddr(["Nike监控助手", MAIL_USER])
        message['To'] = formataddr(["管理员", RECEIVERS[0]])
        message['Subject'] = title

        # 3. 连接服务器并发送
        server = smtplib.SMTP_SSL(MAIL_HOST, 465)
        server.login(MAIL_USER, MAIL_PASS)
        server.sendmail(MAIL_USER, RECEIVERS, message.as_string())
        server.quit()
        
        print("✅ 邮件通知发送成功！")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

# --- 单独运行这个文件测试 ---
if __name__ == "__main__":
    print(f"正在尝试使用账号 {MAIL_USER} 发送测试邮件...")
    send_email("最终测试", "<h1>恭喜！</h1><p>标准协议测试通过！可以去抢鞋了！</p>")