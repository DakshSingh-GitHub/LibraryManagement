import controllers.admin_controller.admin_controller as admin

username = str(input("Enter username: "))
admin.add_users(username)
print(admin.check_if_user("root"))
