import file_handler
import inventory  # 用于复用产品/附加项显示函数
from datetime import datetime  # 用于处理配送日期（可选，作业bonus功能）


def filter_products_by_category(products):
    """按分类筛选产品（功能：销售创建订单-选项1）"""
    fixed_categories = ["浪漫", "生日", "开业", "慰问", "周年"]
    fixed_categories_en = ["Romantic", "Birthday", "Grand Opening", "Condolence", "Anniversary"]
    while True:
        print("\n==== 按分类筛选 ====")
        for i, cat in enumerate(fixed_categories, 1):
            print(f"{i}) {cat}")
        print("0) 返回")
        cat_choice = input("请选择分类：").strip()

        if cat_choice == "0":
            return None  # 返回上一级（产品列表）
        try:
            cat_index = int(cat_choice) - 1
            if 0 <= cat_index < len(fixed_categories):
                selected_cat = fixed_categories[cat_index]
                # 筛选该分类下的可用产品
                cat_index = int(cat_choice) - 1
                filtered = [p for p in products if p["category"] == fixed_categories_en[cat_index] and p["status"] == "Available"]
                if not filtered:
                    print(f"分类 '{fixed_categories[cat_index]}' 中没有可用的产品。")
                    continue
                # 显示筛选结果
                inventory.display_products(filtered)
                # 提供后续选项
                while True:
                    sub_choice = input("\n1) 下单 2) 返回分类筛选 3) 返回主菜单：").strip()
                    if sub_choice == "1":
                        return filtered  # 返回筛选后的产品列表，进入下单流程
                    elif sub_choice == "2":
                        break  # 返回分类选择
                    elif sub_choice == "3":
                        return "back_to_main"  # 标记返回主菜单
                    else:
                        print("错误：无效的选项。请输入 1、2 或 3。")
            else:
                print("错误：请输入 0 到 5 之间的数字。")
        except ValueError:
            print("错误：无效的输入。请输入数字。")


def sort_products_by_price(products):
    """按价格升序排序产品（功能：销售创建订单-选项2）"""
    # 筛选可用产品后排序
    available_products = [p for p in products if p["status"] == "Available"]
    if not available_products:
        print("没有可用的产品可供排序。")
        return None
    # 按price升序排序
    sorted_products = sorted(available_products, key=lambda x: x["price"])
    # 显示排序结果
    print("\n==== 产品按价格排序（升序）====")
    inventory.display_products(sorted_products)
    # 提供后续选项
    while True:
        sub_choice = input("\n1) 下单 2) 返回主菜单：").strip()
        if sub_choice == "1":
            return sorted_products  # 进入下单流程
        elif sub_choice == "2":
            return "back_to_main"  # 返回主菜单
        else:
            print("错误：无效的选项。请输入 1 或 2。")


def collect_order_info(product, addons):
    """收集订单信息（客户、收件人、配送等）"""
    order_info = {}

    # 1. 附加项选择
    print("\n==== 可选附加项 ====")
    inventory.display_addons(addons)
    while True:
        addon_code = input("请输入附加项编号（输入0跳过）：").strip()
        if addon_code == "0":
            order_info["addon_info"] = {"code": "0", "name": "无", "price": 0.0}
            break
        # 查找附加项
        target_addon = None
        for addon in addons:
            if addon["code"] == addon_code and addon["status"] == "Available":
                target_addon = addon
                break
        if not target_addon:
            print(f"错误：附加项编号 '{addon_code}' 不存在或不可用。请重试。")
            continue
        order_info["addon_info"] = {
            "code": target_addon["code"],
            "name": target_addon["name"],
            "price": target_addon["price"]
        }
        break

    # 2. 客户与收件人信息
    order_info["customer_info"] = {}
    while True:
        customer_name = input("\n请输入客户姓名：").strip()
        if customer_name:
            order_info["customer_info"]["name"] = customer_name
            break
        print("错误：客户姓名不能为空。")
    while True:
        recipient_name = input("请输入收件人姓名：").strip()
        if recipient_name:
            order_info["customer_info"]["recipient"] = recipient_name
            break
        print("错误：收件人姓名不能为空。")

    # 3. 留言（限300字符）
    while True:
        message = input("请输入给收件人的留言（最多300字符）：").strip()
        if len(message) <= 300:
            order_info["customer_info"]["message"] = message
            break
        print(f"错误：留言过长（当前：{len(message)}字符）。最多300字符。")

    # 4. 取货/配送选择
    order_info["delivery_info"] = {}
    while True:
        delivery_choice = input("\n店铺自取还是配送？(自取/配送) (Z/P)：").strip().upper()
        if delivery_choice in ["Z", "P"]:
            order_info["delivery_info"]["type"] = "Pickup" if delivery_choice == "Z" else "Delivery"
            break
        print("错误：请输入'Z'（自取）或'P'（配送）。")

    # 5. 配送相关信息（仅配送时收集）
    if order_info["delivery_info"]["type"] == "Delivery":
        # 配送地址
        while True:
            address = input("请输入配送地址：").strip()
            if address:
                order_info["delivery_info"]["address"] = address
                break
            print("错误：配送地址不能为空。")
        # 配送日期（简单格式验证：YYYY-MM-DD，如2023-08-28）
        while True:
            date_input = input("请输入配送日期（格式：YYYY-MM-DD，例如：2023-08-28）：").strip()
            try:
                # 验证格式
                datetime.strptime(date_input, "%Y-%m-%d")
                order_info["delivery_info"]["date"] = date_input
                break
            except ValueError:
                print("错误：无效的日期格式。请使用'YYYY-MM-DD'格式（例如：2023-08-28）。")
        # 当日达选择
        while True:
            same_day = input("是否需要当日达？(是/否) (Y/N)：").strip().upper()
            if same_day in ["Y", "N"]:
                order_info["delivery_info"]["same_day"] = same_day
                # 配送费计算：基础35元 + 当日达35元
                base_fee = 35.0
                same_day_fee = 35.0 if same_day == "Y" else 0.0
                order_info["delivery_info"]["fee"] = base_fee + same_day_fee
                break
            print("错误：请输入'Y'（是）或'N'（否）。")
    else:
        # 取货：无需地址/日期，配送费0
        order_info["delivery_info"]["address"] = "店铺自取"
        order_info["delivery_info"]["date"] = "无需配送"
        order_info["delivery_info"]["same_day"] = "无需配送"
        order_info["delivery_info"]["fee"] = 0.0

    # 6. 产品信息（已选中的产品）
    order_info["product_info"] = {
        "code": product["code"],
        "name": product["name"],
        "price": product["price"]
    }

    # 7. 计算总金额
    total = (product["price"] + order_info["addon_info"]["price"] + order_info["delivery_info"]["fee"])
    order_info["total_amount"] = total

    return order_info


def display_order_summary(order_info):
    """显示订单汇总"""
    print("\n---------- 订单汇总 ---------")
    print(f"商品：        {order_info['product_info']['name']}     {order_info['product_info']['code']}         ${order_info['product_info']['price']:.2f}")
    print(f"附加项：     {order_info['addon_info']['name']}     {order_info['addon_info']['code']}         ${order_info['addon_info']['price']:.2f}")
    print("---------------------------------")
    print(f"\n配送日期：    {order_info['delivery_info']['date']}")
    same_day_text = "是" if order_info['delivery_info']['same_day'] == 'Y' else "否"
    same_day_fee = 35.0 if order_info['delivery_info']['same_day'] == 'Y' else 0.0
    print(f"当日配送：    {same_day_text}                   ${same_day_fee:.2f}")
    print(f"配送基础费用：                             ${order_info['delivery_info']['fee']:.2f}")
    print(f"订单总计：                                  ${order_info['total_amount']:.2f}")

    print(f"\n下单人姓名：  {order_info['customer_info']['name']}")
    print(f"收件人姓名：  {order_info['customer_info']['recipient']}")
    print(f"给收件人的留言：\n{order_info['customer_info']['message']}")
    print(f"配送地址：    {order_info['delivery_info']['address']}")
    print("---------------------------------")


def create_order():
    """功能a：创建订单（销售管理核心功能）"""
    # 加载产品和附加项数据
    products = file_handler.load_products()
    addons = file_handler.load_addons()

    if not products:
        print("没有可用的产品。无法创建订单。")
        return

    # 显示初始产品列表（仅Available）
    available_products = [p for p in products if p["status"] == "Available"]
    if not available_products:
        print("没有可供订购的产品。")
        return
    print("\n==== 可供订购的花卉 ====")
    inventory.display_products(available_products)

    # 初始选项：筛选/排序/下单
    while True:
        print("\n1) 按分类筛选产品")
        print("2) 按价格排序产品")
        print("3) 直接下单")
        choice = input("请输入选项：").strip()

        target_products = available_products  # 默认为所有可用产品
        if choice == "1":
            # 按分类筛选
            result = filter_products_by_category(available_products)
            if result == "back_to_main":
                return  # 返回主菜单
            elif result is not None:
                target_products = result
        elif choice == "2":
            # 按价格排序
            result = sort_products_by_price(available_products)
            if result == "back_to_main":
                return
            elif result is not None:
                target_products = result
        elif choice == "3":
            # 直接下单：从所有可用产品中选择
            pass
        else:
            print("错误：无效的选项。请输入 1、2 或 3。")
            continue

        # 进入下单流程：选择产品code
        while True:
            product_code = input("\n请输入产品编号（从上面的列表中选择）：").strip()
            # 查找产品（需在target_products中且Available）
            selected_product = None
            for p in target_products:
                if p["code"] == product_code and p["status"] == "Available":
                    selected_product = p
                    break
            if not selected_product:
                print(f"Error: Item code '{product_code}' is not available in the current list. Please try again.")
                continue

            # 收集订单信息
            order_info = collect_order_info(selected_product, addons)

            # 显示汇总并确认
            while True:
                display_order_summary(order_info)
                confirm_choice = input("Enter 1 to confirm, 2 to edit info, 0 to cancel: ").strip()
                if confirm_choice == "1":
                    # 生成订单ID并保存
                    order_id = file_handler.get_next_order_id()
                    final_order = {
                        "order_id": order_id,
                        "product_info": order_info["product_info"],
                        "addon_info": order_info["addon_info"],
                        "customer_info": order_info["customer_info"],
                        "delivery_info": order_info["delivery_info"],
                        "total_amount": order_info["total_amount"],
                        "status": "Open"  # 默认状态为Open
                    }
                    file_handler.save_order(final_order)
                    print(f"\nOrder created successfully! Your Order ID: {order_id}")
                    return
                elif confirm_choice == "2":
                    # 重新收集信息
                    print("Re-editing order info...")
                    break
                elif confirm_choice == "0":
                    print("Order cancelled.")
                    return
                else:
                    print("Error: Invalid option. Please enter 1, 2, or 0.")
            break


def display_orders(orders, filter_status=None):
    """打印订单列表（支持按状态筛选）"""
    if not orders:
        print("未找到任何订单。")
        return
    # 筛选状态（默认仅显示Open）
    filtered_orders = orders if filter_status is None else [o for o in orders if o["status"] == filter_status]
    if not filtered_orders:
        status_cn = {
            "Open": "未处理",
            "Ready": "已准备",
            "Delivered": "已送达",
            "Cancelled": "已取消"
        }.get(filter_status, filter_status)
        print(f"未找到状态为'{status_cn}'的订单。")
        return

    status_cn = {
        "Open": "未处理",
        "Ready": "已准备",
        "Delivered": "已送达",
        "Cancelled": "已取消"
    }.get(filter_status, filter_status) if filter_status else "未处理"
    print(f"\n==== 订单列表（状态：{status_cn}）====")
    print(f"{'订单编号':<12} {'产品名称':<20} {'客户姓名':<15} {'总金额 (￥)':<12} {'状态':<10}")
    print("-" * 80)
    for order in filtered_orders:
        status_cn = {
            "Open": "未处理",
            "Ready": "已准备",
            "Delivered": "已送达",
            "Cancelled": "已取消"
        }.get(order['status'], order['status'])
        print(f"{order['order_id']:<12} {order['product_info']['name']:<20} {order['customer_info']['name']:<15} {order['total_amount']:<12.2f} {status_cn:<10}")
    print("-" * 80)


def edit_cancel_order(orders):
    """编辑/取消订单（仅Open状态可修改）"""
    order_id = input("\n请输入要编辑/取消的订单编号：").strip()
    # 查找订单
    target_order = None
    for order in orders:
        if order["order_id"] == order_id:
            target_order = order
            break
    if not target_order:
        print(f"错误：未找到订单编号 '{order_id}'。")
        return

    # 按订单状态提供选项
    print(f"\n==== 订单 {order_id} 的详细信息 ====")
    status_cn = {
        "Open": "未处理",
        "Ready": "已准备",
        "Delivered": "已送达",
        "Cancelled": "已取消"
    }.get(target_order["status"], target_order["status"])
    print(f"状态：{status_cn}")
    if target_order["status"] != "Open":
        print("无法编辑/取消状态为'已准备'、'已送达'或'已取消'的订单。")
        return

    # Open状态：提供修改状态或取消
    while True:
        print("\n1) 更新订单状态（改为已准备/已送达/已取消）")
        print("2) 取消订单（改为已取消）")
        print("3) 返回上一级菜单")
        choice = input("请输入选项：").strip()

        if choice == "1":
            # 更新状态
            print("\n可选状态：")
            print("1) Ready - 已准备")
            print("2) Delivered - 已送达")
            print("3) Cancelled - 已取消")
            status_choice = input("请选择新状态（1/2/3）：").strip()
            status_map = {"1": "Ready", "2": "Delivered", "3": "Cancelled"}
            new_status = status_map.get(status_choice)
            if not new_status:
                print("错误：请输入1、2或3选择状态。")
                continue
            target_order["status"] = new_status
            # 重新保存所有订单（因Orders.txt是追加模式，需覆盖整个文件）
            with open("Orders.txt", "w", encoding="utf-8") as f:
                for o in orders:
                    # 复用save_order的格式
                    addon_code = o["addon_info"]["code"] if o["addon_info"]["code"] != "0" else "0"
                    addon_name = o["addon_info"]["name"] if addon_code != "0" else "无"
                    addon_price = o["addon_info"]["price"] if addon_code != "0" else 0
                    line = (f"{o['order_id']}|{o['product_info']['code']}|{o['product_info']['name']}|{o['product_info']['price']}|"
                            f"{addon_code}|{addon_name}|{addon_price}|{o['customer_info']['name']}|{o['customer_info']['recipient']}|"
                            f"{o['customer_info']['message']}|{o['delivery_info']['type']}|{o['delivery_info']['address']}|"
                            f"{o['delivery_info']['date']}|{o['delivery_info']['same_day']}|{o['delivery_info']['fee']}|"
                            f"{o['total_amount']}|{o['status']}\n")
                    f.write(line)
            status_cn = {
                "Ready": "已准备",
                "Delivered": "已送达",
                "Cancelled": "已取消"
            }.get(new_status, new_status)
            print(f"订单状态已成功更新为'{status_cn}'！")
            break
        elif choice == "2":
            # 取消订单（状态设为Cancelled）
            target_order["status"] = "Cancelled"
            # 重新保存所有订单
            with open("Orders.txt", "w", encoding="utf-8") as f:
                for o in orders:
                    addon_code = o["addon_info"]["code"] if o["addon_info"]["code"] != "0" else "0"
                    addon_name = o["addon_info"]["name"] if addon_code != "0" else "无"
                    addon_price = o["addon_info"]["price"] if addon_code != "0" else 0
                    line = (f"{o['order_id']}|{o['product_info']['code']}|{o['product_info']['name']}|{o['product_info']['price']}|"
                            f"{addon_code}|{addon_name}|{addon_price}|{o['customer_info']['name']}|{o['customer_info']['recipient']}|"
                            f"{o['customer_info']['message']}|{o['delivery_info']['type']}|{o['delivery_info']['address']}|"
                            f"{o['delivery_info']['date']}|{o['delivery_info']['same_day']}|{o['delivery_info']['fee']}|"
                            f"{o['total_amount']}|{o['status']}\n")
                    f.write(line)
            print(f"订单 {order_id} 已成功取消！")
            break
        elif choice == "3":
            break
        else:
            print("错误：无效的选项。请输入 1、2 或 3。")


def view_order():
    """功能b：查看订单（销售管理核心功能）"""
    orders = file_handler.load_orders()
    # 默认显示Open状态订单
    display_orders(orders, filter_status="Open")

    while True:
        print("\n1) 编辑/取消订单")
        print("2) 按状态筛选订单")
        print("3) 返回主菜单")
        choice = input("请输入选项：").strip()

        if choice == "1":
            edit_cancel_order(orders)
            # 重新加载订单并显示
            orders = file_handler.load_orders()
            display_orders(orders, filter_status="Open")
        elif choice == "2":
            # 按状态筛选
            print("\n订单状态：")
            print("Open - 未处理")
            print("Ready - 已准备")
            print("Delivered - 已送达")
            print("Cancelled - 已取消")
            status = input("请输入要筛选的状态：").strip()
            display_orders(orders, filter_status=status)
        elif choice == "3":
            print("正在返回主菜单...")
            break
        else:
            print("错误：无效的选项。请输入 1、2 或 3。")


def sales_menu():
    """销售管理子菜单：整合所有销售功能"""
    while True:
        print("\n==== 销售管理 ====")
        print("a. 创建订单")
        print("b. 查看订单")
        print("c. 返回主菜单")
        choice = input("请输入选项：").strip().lower()

        if choice == "a":
            create_order()
        elif choice == "b":
            view_order()
        elif choice == "c":
            print("正在返回主菜单...")
            break
        else:
            print("错误：无效的选项。请输入 'a'、'b' 或 'c'。")