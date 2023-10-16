from flask import Flask, render_template
import cv2
import os

# Create a Flask web application
app = Flask(__name__)

# Define a route and a view function
@app.route("/")
def hello_world():
    directory_path = "static/movies"
    folder_info_list = []

    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)

        if os.path.isdir(folder_path):
            mp4_files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]

        if len(mp4_files) == 1:
            mp4_file = f"static/movies/{folder_name}/{mp4_files[0]}"

            thumbnail_path = os.path.join(folder_path, "thumbnail.png")  # Removed leading '/'


            if not os.path.exists(thumbnail_path):
                cap = cv2.VideoCapture(mp4_file)

                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        # Save the thumbnail image in the 'static' directory
                        thumbnail_path = f"static/movies/{folder_name}/thumbnail.png"
                        cv2.imwrite(thumbnail_path, frame)
                        print(f"Thumbnail for {folder_name} saved as thumbnail.png")
                    cap.release()
                else:
                    print(f"Error: Could not open video file: {mp4_file}")
            else:
                print(f"Thumbnail already exists for {folder_name}. Loading video...")


                png_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
                png_file = f"movies/{folder_name}/{png_files[0]}" if png_files else ""

                folder_info = {
                    "name": folder_name,
                    "video": os.path.basename(mp4_file),
                    "thumbnail": png_file,
                }
                folder_info_list.append(folder_info)

    return render_template("index.html", movies=folder_info_list)

@app.route("/watch/<movie>/<file>")
def watch(movie,file):
    return render_template("movie.html",name=movie,file=file)
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)
