def time_to_seconds(time_str):
  """
  Converts a time string in 00:00:00 format to seconds.

  Args:
    time_str: The time string in 00:00:00 format.

  Returns:
    The time in seconds.
  """
  hours, minutes, seconds = map(int, time_str.split(':'))
  return hours * 3600 + minutes * 60 + seconds

# Example usage:
time_str = "00:05:55"
seconds = time_to_seconds(time_str)
print(f"Time in seconds: {seconds}")