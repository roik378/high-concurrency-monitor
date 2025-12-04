import time
import random
from playwright.sync_api import sync_playwright
from config import TARGETS, BROWSER_CONFIG, SCAN_INTERVAL
from notifier import send_email

class Monitor:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None

    def start(self):
        """启动浏览器资源"""
        self.playwright = sync_playwright().start()
        # 启动浏览器 (Chromium)
        self.browser = self.playwright.chromium.launch(
            headless=BROWSER_CONFIG['headless']
        )
        # 注入伪装信息，假装是 Mac 电脑上的 Chrome
        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        print("🚀 监控引擎已启动...")

    def check_item(self, target):
        """检查单个商品是否有货"""
        page = self.context.new_page()
        product_name = target['name']
        
        try:
            print(f"🔎 [{time.strftime('%H:%M:%S')}] 正在检查: {product_name}")
            
            # 1. 访问页面
            page.goto(target['url'], timeout=BROWSER_CONFIG['timeout'])
            
            # 2. 随机等待 (模拟人类浏览行为，防封号核心！)
            time.sleep(random.uniform(1.5, 3.5))

            # 3. 寻找购买按钮
            # 使用 wait_for_selector 确保页面加载完成
            try:
                # 尝试等待按钮出现，最多等 5 秒
                page.wait_for_selector(target['selector'], timeout=5000)
                btn = page.locator(target['selector'])
                
                # 4. 判断逻辑
                if btn.is_visible() and btn.is_enabled():
                    return True # ✅ 有货！
            except:
                pass # 找不到按钮，说明没货

            return False # ❌ 无货

        except Exception as e:
            print(f"⚠️ 检测出错: {e}")
            return False
        finally:
            page.close() # 记得关闭页面，释放内存

    def run_loop(self):
        """主循环"""
        self.start()
        try:
            while True:
                for target in TARGETS:
                    is_in_stock = self.check_item(target)
                    
                    if is_in_stock:
                        msg = f"🎉 {target['name']} 补货了！<br>链接：<a href='{target['url']}'>{target['url']}</a>"
                        print("发现库存，正在发送邮件...")

                        # 👇 调用邮件发送
                        send_email(title="🔥发现库存！速抢！", content=msg)

                        return

                    else:
                        print(f"💤 {target['name']} 暂时无货...")
                    
                    # 避免请求过于频繁
                    time.sleep(random.uniform(1, 3))
                
                print(f"⏳ 休息 {SCAN_INTERVAL} 秒进入下一轮...\n")
                time.sleep(SCAN_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n🛑 监控已停止")
        finally:
            self.browser.close()
            self.playwright.stop()

if __name__ == "__main__":
    bot = Monitor()
    bot.run_loop()