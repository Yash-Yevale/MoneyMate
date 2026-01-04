from win10toast import ToastNotifier
  
# create an object to ToastNotifier class
n = ToastNotifier()
  
n.show_toast("GEEKSFORGEEKS", "Notification body", duration = 1,
  icon_path ="https://media.geeksforgeeks.org/wp-content/uploads/geeks.ico")