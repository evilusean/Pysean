import subprocess
import os

def movie_to_gif(input_file, start_time, end_time, output_file, fps=10, width="max"):
  """
  Converts a section of a movie to a GIF using ffmpeg.

  Args:
    input_file: Path to the input movie file.
    start_time: Start time of the section to convert (in seconds).
    end_time: End time of the section to convert (in seconds).
    output_file: Path to the output GIF file (default: "output.gif").
    fps: Frames per second for the GIF (default: 10).
    width: Width of the output GIF in pixels (default: "max" for maximum width).

    Example 'timestamps.txt' file:
    00:01:30-00:02:00
    00:05:15-00:05:45
    01:00:00-01:00:30

  """

  # Get movie dimensions using ffprobe
  probe_command = ["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", input_file]
  probe_output = subprocess.check_output(probe_command).decode("utf-8").strip().split(",")
  movie_width = int(probe_output[0])

  # Set width based on input
  if width == "max":
    width = movie_width  # type "max" to automatically set the width of the saved gif to the same size as movie
  else:
    width = int(width)  # type the width of the size of gif you want, Ex: 640, 1280 etc

  # Check if output file exists, if so, increment the name
  base_name, ext = os.path.splitext(output_file)
  counter = 1
  while os.path.exists(output_file):
    output_file = f"{base_name}_{counter}{ext}"
    counter += 1

  # Construct the ffmpeg command
  command = [
    "ffmpeg",
    "-ss", str(start_time),
    "-i", input_file,
    "-t", str(end_time - start_time),
    "-vf", f"scale={width}:-1",  # Adjust the width, height will be scaled proportionally
    "-r", str(fps),  # Set GIF frame rate
    "-y",  # Overwrite existing output file
    output_file
  ]

  # Run the ffmpeg command
  subprocess.run(command)

def read_timestamps_from_file(file_path):
  """
  Reads timestamps from a text file.

  Args:
    file_path: Path to the text file containing timestamps.

  Returns:
    A list of tuples, where each tuple represents a start and end time: [(start_time1, end_time1), (start_time2, end_time2), ...]
  """
  timestamps = []
  with open(file_path, 'r') as f:
    for line in f:
      start_time_str, end_time_str = line.strip().split('-')
      start_time = time_to_seconds(start_time_str)
      end_time = time_to_seconds(end_time_str)
      timestamps.append((start_time, end_time))
  return timestamps

def time_to_seconds(time_str):
  """
  Converts a time string in 00:00:00, 00:00, or 00 format to seconds.

  Args:
    time_str: The time string.

  Returns:
    The time in seconds.
  """
  parts = time_str.split(':')
  seconds = 0
  if len(parts) >= 3:
    hours, minutes, seconds = map(int, parts[:3])
    seconds += hours * 3600 + minutes * 60
  if len(parts) >= 2:
    minutes, seconds = map(int, parts[-2:])
    seconds += minutes * 60
  if len(parts) >= 1:
    seconds += int(parts[-1])
  return seconds

# Example usage:
#input_movie = "/home/sean/Downloads/movie_1.mp4"
input_movie = "/media/sean/D80477BF04779EE6/CyberpunkEdgerunners/Cyberpunk - Edgerunners - S01E01 - Let You Down.mkv"
gif_fps = 15  # Set the GIF frame rate FPS
gif_width = 640  # will save the first gif as 640 (for cell phones/whatever)
gif_width2 = "max"  # type "max" to automatically set the width of the saved gif to the same size as movie, 
#type an int to use another size

# Read timestamps from a file
timestamps_file = "timestamps.txt"  # Replace with your actual file path
timestamps = read_timestamps_from_file(timestamps_file)

# Create GIFs for each timestamp
for i, (start_time, end_time) in enumerate(timestamps):
  output_gif = f"/home/sean/Pictures/gif/Cyberpunk_{i+1}_small.gif"  # Generate unique output file names
  output_gif2 = f"/home/sean/Pictures/gif/Cyberpunk_{i+1}_full.gif"  # Generate unique output file names
  movie_to_gif(input_movie, start_time, end_time, output_gif, gif_fps, gif_width)
  movie_to_gif(input_movie, start_time, end_time, output_gif2, gif_fps, gif_width2)
