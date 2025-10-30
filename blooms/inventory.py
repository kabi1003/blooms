import file_handler

fixed_categories_en = ["Romantic", "Birthday", "Grand Opening", "Condolence", "Anniversary"]


def inventory_menu():
    """库存管理子菜单"""
    while True:
        print("\n==== 库存管理 ====")
        print("a. 查看/更新花卉")
        print("b. 添加新花卉")
        print("c. 查看/更新附加项")
        print("d. 添加新附加项")
        print("e. 返回主菜单")
        choice = input("请输入选项：").strip().lower()

        if choice == "a" or choice == "1":  
            view_update_products()
        elif choice == "b" or choice == "2":
            add_new_product()
        elif choice == "c" or choice == "3":
            view_update_addons()
        elif choice == "d" or choice == "4":
            add_new_addon()
        elif choice == "e" or choice == "5":
            print("正在返回主菜单...")
            break
        else:
            print("错误：无效的选项。")


def display_products(products):
    """显示产品列表"""
    print("\n==== 当前花卉产品列表 ====")
    print(f"{'编号':<8} {'名称':<20} {'类别':<15} {'价格 (￥)':<10} {'状态':<10}")
    print("-" * 70)
    # 只显示前5个产品
    for i in range(min(5, len(products))):
        product = products[i]
        print(f"{product['code']:<8} {product['name']:<20} {product['category']:<15} {product['price']:<10} {product['status']:<10}")
    print("-" * 70)


def view_update_products():
    """查看/更新产品"""
    products = file_handler.load_products()
    if not products:
        print("未找到任何产品。")
        return

    display_products(products)
    user_input = input("\n请输入要更新的产品编号（输入0返回）：").strip()
    if user_input == "0":
        return
        
    target_product = None
    for i in range(len(products)):
        if products[i]["code"] == user_input:
            target_product = products[i]
            break
            
    if not target_product:
        print("未找到产品")
        return

    new_price = input("请输入新价格：").strip()
    if new_price:
        target_product["price"] = new_price  

    new_status = input("请输入新状态（Available/Unavailable）：").strip()
    if new_status:
        target_product["status"] = new_status  

    file_handler.save_products(products)
    print("更新完成")


def add_new_product():
    """添加新花卉"""
    products = file_handler.load_products()
    fixed_categories = ["浪漫", "生日", "开业", "慰问", "周年"]

    name = input("请输入新花卉的名称：").strip() or "无名"
    print(f"可选分类：{', '.join(fixed_categories)}")
    category = input("请输入分类：").strip() or "浪漫"
    
    price = input("请输入价格：").strip() or "0"

    code = input("请输入产品编号：").strip() or "000"
    
    products.append({
        "code": code,
        "name": name,
        "category": category,
        "price": price,
        "status": "Available"
    })

    file_handler.save_products(products)
    print("添加成功")


def display_addons(addons):
    """显示附加项"""
    print("\n==== 当前附加项 ====")
    print(f"{'编号':<8} {'名称':<30} {'价格 (￥)':<10} {'状态':<10}")
    print("-" * 70)
    for addon in addons:
        print(f"{addon['code']:<8} {addon['name']:<30} {addon['price']:<10} {addon['status']:<10}")
    print("-" * 70)


def view_update_addons():
    """查看/更新附加项"""
    addons = file_handler.load_addons()
    if not addons:
        print("未找到任何附加项。")
        return

    display_addons(addons)
    user_input = input("\n请输入要更新的附加项编号（输入0返回）：").strip()
    if user_input == "0":
        return

    target_addon = None
    for addon in addons:
        if addon["code"] == user_input:
            target_addon = addon
            break
            
    if not target_addon:
        print("未找到附加项")
        return

    new_price = input("请输入新价格：").strip()
    if new_price:
        target_addon["price"] = new_price

    file_handler.save_addons(addons)
    print("更新完成")


def add_new_addon():
    """添加新附加项"""
    addons = file_handler.load_addons()

    name = input("请输入新附加项的名称：").strip() or "无名称"
    price = input("请输入价格：").strip() or "0"
    code = input("请输入编号：").strip() or "ADD000"

    addons.append({
        "code": code,
        "name": name,
        "price": price,
        "status": "Available"
    })

    file_handler.save_addons(addons)
    print("添加成功")