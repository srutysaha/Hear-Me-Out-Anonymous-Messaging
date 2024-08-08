from tkinter import *
import sqlite3
from sum import summarization
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import io

# Configure root window
root = Tk()
root.title("Hear Me Out - Dashboard")
root.geometry("600x600+400+30")
root.resizable(False, False)
root.configure(bg='MediumPurple1')
root.iconbitmap('icon.ico')  # Replace with your .ico file path

# Define styles with Poppins font
heading_font = ("Poppins", 20, "bold")
subheading_font = ("Poppins", 16, "bold")
paragraph_font = ("Poppins", 13)
bg_color = 'MediumPurple1'
btn_color = 'azure'
text_color = 'black'
highlight_color = 'lightblue'
button_radius = 10  # Radius for rounded corners

def create_button(frame, category, row, col):
    # Create a canvas for the button
    canvas = Canvas(frame, width=150, height=60, bg=bg_color, bd=0, highlightthickness=0)
    canvas.grid(row=row, column=col, padx=20, pady=5, sticky='nsew')
    
    # Draw rounded rectangle
    draw_rounded_rectangle(canvas, btn_color, category)

    # Bind highlight effects to the canvas
    canvas.bind("<Enter>", lambda e: on_button_enter(e, category))
    canvas.bind("<Leave>", lambda e: on_button_leave(e, category))
    canvas.bind("<Button-1>", lambda e: on_button_click(e, category))

def view_feedback(category):
    # Placeholder function to view feedback by category
    print(f"Viewing feedback for category: {category}")

def on_button_enter(event, category):
    canvas = event.widget
    # Redraw rounded rectangle with highlight color
    canvas.delete("all")
    draw_rounded_rectangle(canvas, highlight_color, category)

def on_button_leave(event, category):
    canvas = event.widget
    # Redraw rounded rectangle with normal button color
    canvas.delete("all")
    draw_rounded_rectangle(canvas, btn_color, category)

def on_button_click(event, category):
    # Open a new window with a title based on the button category
    open_new_window(category)

def draw_rounded_rectangle(canvas, color, category):
    canvas_width = canvas.winfo_reqwidth()
    canvas_height = canvas.winfo_reqheight()
    
    # Draw rounded rectangle
    canvas.create_arc((0, 0, button_radius*2, button_radius*2), start=90, extent=90, fill=color, outline=color)
    canvas.create_arc((canvas_width-button_radius*2, 0, canvas_width, button_radius*2), start=0, extent=90, fill=color, outline=color)
    canvas.create_arc((0, canvas_height-button_radius*2, button_radius*2, canvas_height), start=180, extent=90, fill=color, outline=color)
    canvas.create_arc((canvas_width-button_radius*2, canvas_height-button_radius*2, canvas_width, canvas_height), start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle((button_radius, 0, canvas_width-button_radius, canvas_height), fill=color, outline=color)
    canvas.create_rectangle((0, button_radius, canvas_width, canvas_height-button_radius), fill=color, outline=color)
    
    # Place text on the button
    canvas.create_text(canvas_width/2, canvas_height/2, text=category, font=paragraph_font, fill=text_color, tags="text")

def open_new_window(category):
    new_window = Toplevel(root)
    new_window.title(f"Hear Me Out - {category}")
    new_window.geometry("600x600+400+30")
    new_window.iconbitmap('icon.ico')
    new_window.resizable(False, False)
    new_window.configure(bg=bg_color)

    # Header for the new window
    header = Label(new_window, text="Hear Me Out - Your Opinions Matter!", font=heading_font, bg=bg_color, fg='white')
    header.pack(pady=10)

    # Placeholder for category specific content
    category_label = Label(new_window, text=f"Category: {category}", font=subheading_font, bg=bg_color, fg='white', anchor='w')
    category_label.pack(pady=20, anchor='w', padx=20)

    # Text display below the category label
    text_display = Label(new_window, text=summarization(category), font=paragraph_font, bg='white', fg=text_color, wraplength=500)
    text_display.pack(pady=(10, 40), padx=20, fill='both', expand=True)

# Function to fetch data from the database
def fetch_data():
    conn = sqlite3.connect('../web-interface/instance/feedback.db')  # Adjust the path as needed
    cursor = conn.cursor()
    cursor.execute('SELECT message_en, category, image FROM fb WHERE image IS NOT NULL')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to display the image from blob data
def display_image(image_data):
    if image_data:
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((100, 100))  # Resize image if needed
        return ImageTk.PhotoImage(image), image
    return None, None

# Function to download image
def download_image(image):
    if image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            image.save(file_path)

# Function to populate data in the new window
def populate_data_frame(frame):
    rows = fetch_data()
    row_num = 0
    for row in rows:
        message, category, image_data = row
        photo_image, pil_image = display_image(image_data)
        
        if photo_image:
            image_label = Label(frame, image=photo_image)
            image_label.image = photo_image  # Keep a reference to avoid garbage collection
            image_label.grid(row=row_num, column=0, padx=10, pady=10)
            
            download_button = Button(frame, text="Download image",cursor="hand2",font=paragraph_font, command=lambda img=pil_image: download_image(img))
            download_button.grid(row=row_num, column=1, padx=10, pady=10)
        
        message_label = Label(frame, text=message,font=paragraph_font, wraplength=400, justify=LEFT)
        message_label.grid(row=row_num, column=2, padx=10, pady=10)
        
        category_label = Label(frame, text=category,font=paragraph_font)
        category_label.grid(row=row_num, column=3, padx=10, pady=10)
        
        row_num += 1

# Function to open the issue window and populate it with data
def issue():
    window = Toplevel(root)
    window.geometry("800x600+400+30")
    window.title("Issues with images")
    window.iconbitmap('icon.ico')
    window.configure(bg=bg_color)
    
    # Create a canvas and a scrollbar
    canvas = Canvas(window, bg=bg_color, highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    button_frame = Frame(canvas, bg=bg_color)
    canvas.create_window((0, 0), window=button_frame, anchor='nw')

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    button_frame.bind("<Configure>", on_frame_configure)

    # Populate the frame with data
    populate_data_frame(button_frame)

# Configure grid for centering
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Header Frame
header_frame = Frame(root, bg=bg_color)
header_frame.grid(row=0, column=0, pady=(10, 0), sticky='n')

# Header
header = Label(header_frame, text="Hear Me Out - Your Opinions Matter!", font=heading_font, bg=bg_color, fg='white')
header.pack()

# Welcome message
welcome_msg = Label(header_frame, text="Welcome to the Dashboard", font=subheading_font, bg=bg_color, fg='white')
welcome_msg.pack()

# Feedback category label
category_label = Label(header_frame, text="View Feedback by Category:", font=subheading_font, bg=bg_color, fg='white')
category_label.pack(pady=(50, 10), padx=20, anchor='w')  # Reduced bottom padding

# Frame for buttons with Canvas and Scrollbar
canvas = Canvas(root, bg=bg_color, highlightthickness=0)
canvas.grid(row=1, column=0, sticky='nsew')

scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
scrollbar.grid(row=1, column=1, sticky='ns')

canvas.configure(yscrollcommand=scrollbar.set)

button_frame = Frame(canvas, bg=bg_color)
canvas.create_window((0, 0), window=button_frame, anchor='nw')

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

button_frame.bind("<Configure>", on_frame_configure)

# Connect to the database
conn = sqlite3.connect("../web-interface/instance/feedback.db")
cursor = conn.cursor()

# Query data from the table
cursor.execute('SELECT DISTINCT CATEGORY FROM fb')
rows = cursor.fetchall()
l = len(rows)
j = 0
while j < l:
    create_button(button_frame, rows[j][0], j // 3, j % 3)  # Adjusted for grid placement
    j += 1

# Adjusting the column to push buttons to the right
for i in range(4):
    button_frame.columnconfigure(i, weight=1)
for i in range(l//3):
    button_frame.rowconfigure(i, weight=1)

def visual():
    vw = Toplevel(root)
    vw.title("Statistics Report")
    vw.iconbitmap('icon.ico')
    vw.geometry("600x600+400+30")
    vw.attributes()
    vw.configure(bg=bg_color)

    conn = sqlite3.connect("../web-interface/instance/feedback.db")
    cursor = conn.cursor()

    cursor.execute('''
    SELECT CATEGORY, 
           SUM(CASE WHEN SENTIMENT = 1 THEN 1 ELSE 0 END) as positive_count,
           SUM(CASE WHEN SENTIMENT = -1 THEN 1 ELSE 0 END) as negative_count
    FROM fb
    GROUP BY CATEGORY
    ''')
    rows = cursor.fetchall()

    categories = [row[0] for row in rows]
    positive_counts = [row[1] for row in rows]
    negative_counts = [row[2] for row in rows]

    # Create a figure for the bar plot
    fig, ax = plt.subplots()

    # Define bar width
    bar_width = 0.35

    # Set the positions of the bars on the x-axis
    bar1 = range(len(categories))
    bar2 = [i + bar_width for i in bar1]

    # Create bar plots
    ax.bar(bar1, positive_counts, width=bar_width, label='Positive', color='blue')
    ax.bar(bar2, negative_counts, width=bar_width, label='Negative', color='red')

    # Add labels, title, and legend
    ax.set_xlabel('Categories')
    ax.set_ylabel('Counts')
    ax.set_title('Sentiment Analysis by Category')
    ax.set_xticks([i + bar_width / 2 for i in range(len(categories))])
    ax.set_xticklabels(categories)
    ax.legend()

    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=vw)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    # Close the database connection
    conn.close()

end = (l // 3) + 1
b = Button(root, text="View Statistics Report", font=paragraph_font, command=visual, width="30", cursor="hand2", bg="lightblue")
b.grid(row=end, column=0, pady=(0, 20))

critical = Button(root, text="Issues with images", font=paragraph_font, command=issue)
critical.grid(row=(end + 1), column=0, pady=(0, 20))

# Close the connection
conn.close()

root.mainloop()
