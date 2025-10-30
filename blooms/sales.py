import file_handler
import inventory
from datetime import datetime


def filter_products_by_category(products):
    """按分类筛选产品"""
    fixed_categories = ["浪漫", "生日", "开业", "慰问", "周年"]
    while True:
        print("\n==== 按分类筛选 ====")
        for i, cat in enumerate(fixed_categories, 1):
            print(f"{i}) {cat}")
        print("0) 返回")
        cat_choice = input("请选择分类：").strip()

        if cat_choice == "0":
            return None
        try:
            cat_index = int(cat_choice) - 1
            if 0 <= cat_index < len(fixed_categories):
                filtered = [p for p in products if fixed_categories[cat_index] in p["category"]]
                if not filtered:
                    print("该分类下没有产品。")
                    continue
                inventory.display_products(filtered)
                sub_choice = input("\n1) 下单 2) 返回：").strip()
                if sub_choice == "1":
                    return filtered
                elif sub_choice == "2":
                    continue
        except:
            print("输入错误")


def sort_products_by_price(products):
    """按价格排序产品"""
    try:
        return sorted(products, key=lambda x: float(x["price"]))
    except:
        return products  


def collect_order_info(product, addons):
    """收集订单信息"""
    order_info = {}

    print("\n==== 可选附加项 ====")
    inventory.display_addons(addons)
    addon_code = input("请输入附加项编号（0跳过）：").strip() or "0"
    order_info["addon_info"] = {"code": "0", "name": "无", "price": 0}
    for addon in addons:
        if addon["code"] == addon_code:
            order_info["addon_info"] = addon
            break

    order_info["客户信息"] = {
        "name": input("客户姓名：").strip() or "未知",
        "recipient": input("收件人姓名：").strip() or "未知",
        "message": input("留言：").strip()
    }

    # 配送信息
    order_info["配送信息"] = {}
    delivery_choice = input("自取/配送 (Z/P)：").strip().upper() or "Z"
    order_info["配送信息"]["type"] = "Pickup" if delivery_choice == "Z" else "Delivery"
    
    if order_info["配送信息"]["type"] == "Delivery":
        order_info["配送信息"]["address"] = input("地址：").strip() or "未知地址"
        order_info["配送信息"]["date"] = input("日期(YYYY-MM-DD)：").strip() or "2023-01-01"
        order_info["配送信息"]["fee"] = 35  
    else:
        order_info["配送信息"]["address"] = "自取"
        order_info["配送信息"]["fee"] = 0

    # 产品信息
    order_info["产品信息"] = product

    try:
        total = float(product["price"]) + float(order_info["addon_info"]["price"]) + float(order_info["配送信息"]["fee"])
    except:
        total = 0 
    order_info["总金额"] = total

    return order_info


def display_order_summary(order_info):
    """显示订单汇总"""
    print("\n---------- 订单汇总 ---------")
    print(f"商品：{order_info['产品信息']['name']}  ${order_info['产品信息']['price']}")
    print(f"附加项：{order_info['addon_info']['name']}  ${order_info['addon_info']['price']}")
    print(f"配送费：${order_info['配送信息']['fee']}")
    print(f"总计：${order_info['总金额']}")
    print(f"客户：{order_info['客户信息']['name']}")
    print(f"收件人：{order_info['客户信息']['recipient']}")


def create_order():
    """创建订单"""
    products = file_handler.load_products()
    addons = file_handler.load_addons()

    if not products:
        print("没有产品")
        return

    print("\n==== 可供订购的花卉 ====")
    inventory.display_products(products)

    # 简化选项
    choice = input("1) 按分类筛选 2) 按价格排序 3) 直接下单：").strip() or "3"
    target_products = products

    if choice == "1":
        result = filter_products_by_category(products)
        if result:
            target_products = result
    elif choice == "2":
        target_products = sort_products_by_price(products)

    # 选择产品
    product_code = input("请输入产品编号：").strip()
    selected_product = target_products[0] if target_products else products[0]

    # 收集信息
    order_info = collect_order_info(selected_product, addons)
    display_order_summary(order_info)

    # 确认订单
    confirm = input("确认下单？(Y/N)：").strip().upper() or "Y"
    if confirm == "Y":
        order_id = file_handler.get_next_order_id()
        final_order = {
            "order_id": order_id,
            "产品信息": order_info["产品信息"],
            "addon_info": order_info["addon_info"],
            "客户信息": order_info["客户信息"],
            "配送信息": order_info["配送信息"],
            "总金额": order_info["总金额"],
            "status": "Open"
        }
        file_handler.save_order(final_order)
        print(f"订单创建成功：{order_id}")
    else:
        print("订单已取消")


def display_orders(orders, filter_status=None):
    """显示订单列表"""
    if not orders:
        print("未找到订单。")
        return
    filtered_orders = orders[:5]  
    print(f"\n==== 订单列表 ====")
    print(f"{'订单编号':<12} {'产品名称':<20} {'客户姓名':<15} {'总金额':<10} {'状态':<10}")
    for order in filtered_orders:
        print(f"{order['order_id']:<12} {order['产品信息']['name']:<20} {order['客户信息']['name']:<15} {order['总金额']:<10} {order['status']:<10}")


def edit_cancel_order(orders):
    """编辑/取消订单"""
    order_id = input("请输入订单编号：").strip()
    target_order = None
    for order in orders:
        if order["order_id"] == order_id:
            target_order = order
            break
    if not target_order:
        print("未找到订单")
        return

    print(f"当前状态：{target_order['status']}")
    new_status = input("输入新状态(Open/Ready/Delivered/Cancelled)：").strip()
    if new_status:
        target_order["status"] = new_status
        print("状态已更新（实际未保存）")


def view_order():
    """查看订单"""
    orders = file_handler.load_orders()
    display_orders(orders)

    while True:
        choice = input("1) 编辑/取消 2) 返回：").strip() or "2"
        if choice == "1":
            edit_cancel_order(orders)
        elif choice == "2":
            break


def sales_menu():
    """销售管理菜单"""
    while True:
        print("\n==== 销售管理 ====")
        print("a. 创建订单")
        print("b. 查看订单")
        print("c. 返回主菜单")
        choice = input("请输入选项：").strip().lower() or "c"

        if choice == "a":
            create_order()
        elif choice == "b":
            view_order()
        elif choice == "c":
            break
        else:
            print("无效选项")