def time_to_seconds(time_str):
  """
  Converts a time string in 00:00:00 format to seconds.

  Args:
    time_str: The time string in 00:00:00 format.

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

while True:
  try:
    time_str = input("Enter time in 00:00:00 format (hour:minute:second), or just minute:second, or just second: ")
    seconds = time_to_seconds(time_str)
    print(f"Time in seconds: {seconds}")
  except KeyboardInterrupt:
    print("\nConversion canceled.")
    break
  except ValueError:
    print("Invalid time format. Please use 00:00:00, 00:00, or 00.")
