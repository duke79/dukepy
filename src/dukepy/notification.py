from win10toast import ToastNotifier

if __name__ == "__main__":
    toaster = ToastNotifier()
    toaster.show_toast("Hello World!!!",
                       "Python is 10 seconds awsm!",
                       icon_path="custom.ico",
                       duration=10)
