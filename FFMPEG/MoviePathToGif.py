import subprocess

def movie_to_gif(input_file, start_time, end_time, output_file="output.gif", fps=10, width="max"):
  """
  Converts a section of a movie to a GIF using ffmpeg.

  Args:
    input_file: Path to the input movie file.
    start_time: Start time of the section to convert (in seconds).
    end_time: End time of the section to convert (in seconds).
    output_file: Path to the output GIF file (default: "output.gif").
    fps: Frames per second for the GIF (default: 10).
    width: Width of the output GIF in pixels (default: "max" for maximum width).
  """

  # Get movie dimensions using ffprobe
  probe_command = ["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", input_file]
  probe_output = subprocess.check_output(probe_command).decode("utf-8").strip().split(",")
  movie_width = int(probe_output[0])

  # Set width based on input
  if width == "max":
    width = movie_width #type "max" to automatically set the width of the saved gif to the same size as movie
  else:
    width = int(width) #type the width of the size of gif you want, Ex: 640, 1280 etc

  # Construct the ffmpeg command
  command = [
    "ffmpeg",
    "-ss", str(start_time),
    "-i", input_file,
    "-t", str(end_time - start_time),
    "-vf", f"scale={width}:-1",  # Adjust the width, height will be scaled proportionally
    "-gifflags", f"fps={fps}",  # Set GIF frame rate
    "-y",  # Overwrite existing output file
    output_file
  ]

  # Run the ffmpeg command
  subprocess.run(command)

# Example usage:
input_movie = "/home/sean/Downloads/movie_1.mp4"
start_time = 10  # Start at 10 seconds
end_time = 20  # End at 20 seconds
output_gif = "/home/sean/Pictures/gif/my_gif.gif"
gif_fps = 5  # Set the GIF frame rate to 5 fps
gif_width = "max"  # type "max" to automatically set the width of the saved gif to the same size as movie, 
#type an int to use another size

movie_to_gif(input_movie, start_time, end_time, output_gif, gif_fps, gif_width)


