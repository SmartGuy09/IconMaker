import tkinter as tk
from tkinter import filedialog
from PIL import Image
import requests
import webbrowser

class IconMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Icon Maker")  # The title of the window
        # The Icon file should be in the same directory
        self.root['background']='#282b30'

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # width and height
        window_width = 600
        window_height = 500

        # the math
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set the window geometry
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")  # the final piece to center the window
        self.root.resizable(False, False)  # the window is not resizable in both x and y
        self.create_widgets()

    def create_widgets(self):
        file_label = tk.Label(self.root, text="Choose a Image file:", bg='#282b30',fg='white', font='bold')
        file_label.pack(pady=5)

        self.file_entry = tk.Entry(self.root, width=40, bg='grey',bd=0)
        self.file_entry.pack()

        self.supported_formats_label = tk.Label(self.root, text="Supported formats: jpg, jpeg, webp, png", fg="lightgray", bg='#282b30')
        self.supported_formats_label.pack()

        self.file_button = tk.Button(self.root, text="Browse", command=self.browse_file, bg='lightgrey', bd=0, activebackground='#282b30')
        self.file_button.pack(pady=20)

        self.remove_bg_var = tk.BooleanVar()
        self.remove_bg_var.set(False)  # Default value is False to save you api previews


        self.remove_bg_checkbox = tk.Checkbutton(self.root, text="Remove Background", variable=self.remove_bg_var,font=(34), bg='#282b30',fg='white', activebackground='#282b30',bd=0, selectcolor='black', command=self.check_clicked)
        self.remove_bg_checkbox.pack(pady=10)

        self.convert_button = tk.Button(self.root, text="Convert to .ico", command=self.convert_to_ico, bg='lightgrey', bd=0, activebackground='#282b30')
        self.convert_button.pack(pady=10)

        self.noteLabel = tk.Label(self.root, text="THERE ARE SOME PROBLEMS HERE,\n YOU HAVE TO RESTART THE APPLICATION IF YOU WANT TO CONVERT ANOTHER IMAGE AFTER THE FIRST ONE \n I CAN PROBABLY FIX IT BUT I'M TOO LAZY", bg='#282b30', fg='green')
        self.noteLabel.pack(side='bottom')

        self.api_entry = tk.Entry(self.root, width=40, bg='grey',bd=0)
        self.api_entry.pack(pady= 20, side='bottom')

        file_apilabel = tk.Label(self.root, text="Enter API key:", bg='#282b30',fg='white', font='bold')
        file_apilabel.pack(side='bottom')


    def check_clicked(self):
        if self.remove_bg_var.get() == True:
            # self.show_error("No api key found. \n If not available Create on here")
            if self.api_entry.get() == "":
                self.show_error("No api key found \n Please add an api key below \n You can create one here...","api")
                
                self.remove_bg_var.set(False)
                return
        else:
            # self.remove_bg_checkbox.selectcolor="black"
            return
    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Choose the Image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.webp;*.png")])
        self.file_entry.insert(0, filename)

    def remove_bg(self):
        filepath = self.file_entry.get()
        apikey = self.api_entry.get()
        if self.remove_bg_var.get():  # Check if the checkbox is checked
            with open(filepath, 'rb') as file:
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': file},
                    data={'size': 'auto'},                    
                    headers={'X-Api-Key': f'{apikey}'},
                )
                if response.status_code == requests.codes.ok:
                    # Generate a new filename for the processed image
                    new_filepath = filepath[:-4] + "_processed.png"
                    with open(new_filepath, 'wb') as out:
                        out.write(response.content)
                    return new_filepath  # Return the file path of the processed image
                else:
                    self.show_error(f"Error: {response.status_code}, {response.text}","any")
                    return None
        else:
            return filepath

    def convert_to_ico(self):
        file_path = self.remove_bg() # Either the removed background image or the normal one
        if file_path:
            img = Image.open(file_path)
            img = img.convert("RGBA")  # Convert to RGBA format [important]

            # Define target sizes with aspect ratio preserved
            aspect_ratio = img.width / img.height
            # Resize image to appropriate icon sizes (e.g., 16x16, 32x32, 64x64) [FOR RECTANGLE IMAGES]
            sizes = [(256, int((256 / aspect_ratio*float(3/2)))),
                     (512, int((512 / aspect_ratio)*float(3/2))),
                     (1024, int((1024 / aspect_ratio)*float(3/2)))]
            icon_images = [img.resize(size) for size in sizes]

            # Save each resized image to .ico format
            output_path = filedialog.asksaveasfilename(defaultextension=".ico", filetypes=[("Icon files", "*.ico")])

            if output_path:
                icon_images[0].save(output_path, format="ICO", sizes=[img.size for img in icon_images])

            # THERE ARE SOME PROBLEMS HERE, YOU HAVE TO RESTART THE APPLICATION IF YOU WANT TO CONVERT ANOTHER IMAGE AFTER THE FIRST ONE
            # I CAN PROBABLY FIX IT BUT I'M TOO LAZY
        else:
            self.show_error("No Image found!!","any")

    def show_error(self, message, button):
        self.error_window = tk.Tk()
        self.error_window.title("Error")
        self.error_window['background']='#282b30'

        # this shit again
        screen_width = self.error_window.winfo_screenwidth()
        screen_height = self.error_window.winfo_screenheight()

        window_width = 300
        window_height = 200

        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        self.error_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Display the error message
        self.error_label = tk.Label(self.error_window, text=message , bg='#282b30' , fg= "white",font=(10))
        self.error_label.pack(padx=20, pady=10)

        # Sorry button to close the error window
        if button == "api":
            self.getapi_button = tk.Button(self.error_window, text="Get API!", command=self.open_link, bg='lightgrey', bd=0, activebackground='#282b30')
            self.getapi_button.pack(pady=10)

            self.anoteLabel = tk.Label(self.error_window, text="Login Required for API!!", bg='#282b30', fg='green')
            self.anoteLabel.pack()
            self.tipLabel = tk.Label(self.error_window, text="TIP: Just remove background \n from https://remove.bg [no login]", bg='#282b30', fg='yellow')
            self.tipLabel.pack(side='bottom')
        else:
            self.sorry_button = tk.Button(self.error_window, text="Sorry!", command=self.error_window.destroy, bg='lightgrey', bd=0, activebackground='#282b30')
            self.sorry_button.pack(pady=30)

    def open_link(self):
        webbrowser.open_new("https://www.remove.bg/dashboard#api-key")
        self.error_window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = IconMakerApp(root)
    root.mainloop()

#1JQeEQf5YCYE2DnzVD2YiDTc
#1JQeEQf5YCYE2DnzVD2YiDTc