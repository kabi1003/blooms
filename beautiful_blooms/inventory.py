import file_handler  # 导入文件操作模块


def inventory_menu():
    """库存管理子菜单"""
    while True:
        print("\n---- 库存管理 ----")
        print("a. 查看/更新花卉")
        print("b. 返回主菜单")
        
        choice = input("请输入选项：").strip().lower()
        
        if choice == 'a':
            view_update_products()
        elif choice == 'b':
            return
        else:
            print("错误：无效的选项。请输入 'a' 或 'b'。")


def display_products(products):
    """打印产品列表（格式化输出）"""
    print("\n==== 当前花卉产品列表 ====")
    print(f"{'编号':<8} {'名称':<20} {'类别':<15} {'价格 (￥)':<10} {'状态':<10}")
    print("-" * 70)
    for product in products:
        print(f"{product['code']:<8} {product['name']:<20} {product['category']:<15} {product['price']:<10.2f} {product['status']:<10}")
    print("-" * 70)


def view_update_products():
    """功能a：查看/更新花束（产品）"""
    products = file_handler.load_products()
    if not products:
        print("未在 Products.txt 中找到任何产品。")
        return

    # 显示产品列表
    display_products(products)

    # 提示用户输入产品code或0返回
    while True:
        user_input = input("\n请输入要更新的产品编号（输入0返回上一级菜单）：").strip()
        if user_input == "0":
            return  # 返回库存子菜单
        # 查找输入的code是否存在
        target_product = None
        for product in products:
            if product["code"] == user_input:
                target_product = product
                break
        if not target_product:
            print(f"错误：未找到编号为 '{user_input}' 的产品。请重试。")
            continue

        # 显示目标产品当前信息
        print(f"\n==== 产品 {target_product['code']} 的详细信息 ====")
        print(f"名称：{target_product['name']}")
        print(f"当前价格：￥{target_product['price']:.2f}")
        print(f"当前状态：{target_product['status']}")

        # 收集新价格和新状态（允许用户按回车保持原值）
        new_price_input = input("请输入新价格（直接按回车保持当前价格）：").strip()
        new_status_input = input("请输入新状态（可用/不可用，直接按回车保持当前状态）：").strip()

        # 更新价格（需验证为正数）
        if new_price_input:
            try:
                new_price = float(new_price_input)
                if new_price <= 0:
                    print("Error: Price must be positive. No update to price.")
                else:
                    target_product["price"] = new_price
                    print(f"Price updated to ${new_price:.2f}")
            except ValueError:
                print("Error: Invalid price format. No update to price.")

        # 更新状态（需为指定值）
        if new_status_input:
            if new_status_input in ["Available", "Unavailable"]:
                target_product["status"] = new_status_input
                print(f"Status updated to {new_status_input}")
            else:
                print("Error: Status must be 'Available' or 'Unavailable'. No update to status.")

        # 同步到文件
        file_handler.save_products(products)
        print("Product updated successfully!")
        break  # 完成更新后返回子菜单


def add_new_product():
    """功能b：新增花束（产品）"""
    products = file_handler.load_products()
    fixed_categories = ["浪漫", "生日", "开业", "慰问", "周年"]
    fixed_categories_en = ["Romantic", "Birthday", "Grand Opening", "Condolence", "Anniversary"]

    # 1. 收集产品信息
    # 产品名称
    while True:
        name = input("请输入新花卉的名称：").strip()
        if name:
            break
        print("错误：名称不能为空。请重试。")

    # 产品分类（仅允许固定选项）
    while True:
        print(f"\n可选分类：{', '.join(fixed_categories)}")
        category_input = input("请输入新花卉的分类：").strip()
        category_index = -1
        for i, cat in enumerate(fixed_categories):
            if category_input == cat:
                category_index = i
                break
        if category_index >= 0:
            category = fixed_categories_en[category_index]
            break
        print(f"错误：分类必须是以下之一 {', '.join(fixed_categories)}。请重试。")

    # 产品价格（正数验证）
    while True:
        price_input = input("请输入新花卉的价格：").strip()
        try:
            price = float(price_input)
            if price > 0:
                break
            print("错误：价格必须为正数。请重试。")
        except ValueError:
            print("错误：无效的价格格式。请输入数字。")

    # 产品code（唯一验证，支持手动/自动生成）
    while True:
        code_choice = input("\n请输入'M'手动输入编号，或'A'自动生成编号：").strip().upper()
        if code_choice not in ["M", "A"]:
            print("错误：请输入'M'或'A'。")
            continue

        if code_choice == "M":
            # 手动输入code
            code = input("请输入产品编号（必须唯一）：").strip()
            # 检查唯一性
            code_exists = any(p["code"] == code for p in products)
            if code_exists:
                print(f"错误：编号'{code}'已存在。请重试。")
                continue
            break
        else:
            # 自动生成code（按分类前缀：R=浪漫, B=生日, GO=开业, C=慰问, A=周年）
            prefix = {
                "Romantic": "R",
                "Birthday": "B",
                "Grand Opening": "GO",
                "Condolence": "C",
                "Anniversary": "A"
            }[category]
            # 查找当前分类下最大的序号（如R001→序号1）
            max_num = 0
            for p in products:
                if p["code"].startswith(prefix):
                    try:
                        num = int(p["code"][len(prefix):])
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        continue
            # 生成新code（前缀+3位序号，如R002）
            code = f"{prefix}{max_num + 1:03d}"
            print(f"自动生成的产品编号：{code}")
            break

    # 2. 创建新产品并添加到列表
    new_product = {
        "code": code,
        "name": name,
        "category": category,
        "price": price,
        "status": "Available"  # 默认状态为Available（可用）
    }
    products.append(new_product)

    # 3. 同步到文件
    file_handler.save_products(products)
    print(f"\n新花卉'{name}'（编号：{code}）添加成功！")


def display_addons(addons):
    """打印附加项列表（格式化输出）"""
    print("\n==== 当前附加项 ====")
    print(f"{'编号':<8} {'名称':<30} {'价格 (￥)':<10} {'状态':<10}")
    print("-" * 70)
    for addon in addons:
        print(f"{addon['code']:<8} {addon['name']:<30} {addon['price']:<10.2f} {addon['status']:<10}")
    print("-" * 70)


def view_update_addons():
    """功能c：查看/更新附加项"""
    addons = file_handler.load_addons()
    if not addons:
        print("在 Addons.txt 中未找到任何附加项。")
        return

    # 显示附加项列表
    display_addons(addons)

    # 提示用户输入附加项code或0返回
    while True:
        user_input = input("\n请输入要更新的附加项编号（输入0返回上一级菜单）：").strip()
        if user_input == "0":
            return
        # 查找输入的code是否存在
        target_addon = None
        for addon in addons:
            if addon["code"] == user_input:
                target_addon = addon
                break
        if not target_addon:
            print(f"错误：未找到编号为 '{user_input}' 的附加项。请重试。")
            continue

        # 显示目标附加项当前信息
        print(f"\n==== 附加项 {target_addon['code']} 的详细信息 ====")
        print(f"名称：{target_addon['name']}")
        print(f"当前价格：￥{target_addon['price']:.2f}")
        print(f"当前状态：{target_addon['status']}")

        # 收集新价格和新状态
        new_price_input = input("请输入新价格（直接按回车保持当前价格）：").strip()
        new_status_input = input("请输入新状态（可用/不可用，直接按回车保持当前状态）：").strip()

        # 更新价格
        if new_price_input:
            try:
                new_price = float(new_price_input)
                if new_price <= 0:
                    print("错误：价格必须为正数。价格未更新。")
                else:
                    target_addon["price"] = new_price
                    print(f"价格已更新为 ￥{new_price:.2f}")
            except ValueError:
                print("错误：无效的价格格式。价格未更新。")

        # 更新状态
        if new_status_input:
            status = new_status_input.lower()
            if status in ['可用', '不可用', 'available', 'unavailable']:
                if status in ['可用', 'available']:
                    target_addon["status"] = 'Available'
                else:
                    target_addon["status"] = 'Unavailable'
                print(f"状态已更新为：{target_addon['status']}")
            else:
                print("错误：状态必须是'可用'或'不可用'。状态未更新。")

        # 同步到文件
        file_handler.save_addons(addons)
        print("附加项更新成功！")
        break


def add_new_addon():
    """功能d：新增附加项"""
    addons = file_handler.load_addons()

    # 1. 收集附加项信息
    # 附加项名称
    while True:
        name = input("请输入新附加项的名称：").strip()
        if name:
            break
        print("错误：名称不能为空。请重试。")

    # 附加项价格
    while True:
        price_input = input("请输入新附加项的价格：").strip()
        try:
            price = float(price_input)
            if price > 0:
                break
            print("错误：价格必须为正数。请重试。")
        except ValueError:
            print("错误：无效的价格格式。请输入数字。")

    # 附加项code（唯一验证，支持手动/自动生成，前缀建议为ADD）
    while True:
        code_choice = input("\n请输入'M'手动输入编号，或'A'自动生成编号：").strip().upper()
        if code_choice not in ["M", "A"]:
            print("错误：请输入'M'或'A'。")
            continue

        if code_choice == "M":
            code = input("请输入附加项编号（必须唯一，建议使用'ADD'前缀）：").strip()
            code_exists = any(a["code"] == code for a in addons)
            if code_exists:
                print(f"错误：编号'{code}'已存在。请重试。")
                continue
            break
        else:
            # 自动生成code（ADD+4位序号，如ADD004）
            max_num = 0
            for a in addons:
                if a["code"].startswith("ADD"):
                    try:
                        num = int(a["code"][3:])
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        continue
            code = f"ADD{max_num + 1:03d}"
            print(f"自动生成的附加项编号：{code}")
            break

    # 2. 创建新附加项并添加到列表
    new_addon = {
        "code": code,
        "name": name,
        "price": price,
        "status": "Available"
    }
    addons.append(new_addon)

    # 3. 同步到文件
    file_handler.save_addons(addons)
    print(f"\n新附加项'{name}'（编号：{code}）添加成功！")


def inventory_menu():
    """库存管理子菜单：整合所有库存功能"""
    while True:
        print("\n==== 库存管理 ====")
        print("a. 查看/更新花卉")
        print("b. 添加新花卉")
        print("c. 查看/更新附加项")
        print("d. 添加新附加项")
        print("e. 返回主菜单")
        choice = input("请输入选项：").strip().lower()

        if choice == "a":
            view_update_products()
        elif choice == "b":
            add_new_product()
        elif choice == "c":
            view_update_addons()
        elif choice == "d":
            add_new_addon()
        elif choice == "e":
            print("正在返回主菜单...")
            break
        else:
            print("错误：无效的选项。请输入 'a'、'b'、'c'、'd' 或 'e'。")