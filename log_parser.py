from re import sub
from datetime import datetime, timedelta
from statistics import mean

data = []
results = []
drivers_best_laps = []
race_best_lap = {}
drivers_avg_speed = []
drivers_diff_to_first = []

def parse():
  """ opens the log file in right mode """
  """ for each line remove extra spaces and dashes, spliting the items in a list """
  """ append the items to the data array """
  log_file = open("./log.in", "r")
  log_file.readline()
  for line in log_file:
    items = sub('[ –]+', ' ', line).split()
    data.append(items)
  log_file.close()

""" tested """
def extract_name(code):
  """ slices the array in order to get the name(data[i][2]) that corresponds to the code """
  """ remove duplicates then pop the only name that's left, which will be returned by the function """
  return set([data[i][2] for i in range(0,len(data)) if data[i][1] == code]).pop()

""" tested """
def extract_laps(code):
  """ slices the array in order to get the number of laps(data[i][3]) that corresponds to the code """
  """ return the length of the sliced array as the number of laps """
  return len([data[i][3] for i in range(0,len(data)) if data[i][1] == code])

""" tested """
def extract_race_time(code):
  """ slices the array in order to get the lap times(data[i][4]) that corresponds to the code """
  """ converts each element to datetime, with the expected format """
  """ sum all the values as timedelta then return the amount of time, in seconds """
  lap_times = [datetime.strptime(data[i][4], "%M:%S.%f") for i in range(0,len(data)) if data[i][1] == code]
  delta = timedelta(minutes=0, seconds=0, microseconds=0)
  for lap in lap_times:
    delta = delta + timedelta(minutes=lap.minute, seconds=lap.second, microseconds=lap.microsecond)
  return delta.seconds + delta.microseconds/10**6

""" tested """
def extract_best_lap(code):
  """ slices the array in order to get the lap times(data[i][4]) that corresponds to the code """
  """ converts each element to datetime, with the expected format """
  """ get the min value convert to timedelta then return the amount of time, in seconds """
  lap = min([datetime.strptime(data[i][4], "%M:%S.%f") for i in range(0,len(data)) if data[i][1] == code])
  delta = timedelta(minutes=lap.minute, seconds=lap.second, microseconds=lap.microsecond)
  return delta.seconds + delta.microseconds/10**6

""" tested """
def extract_avg_speed(code):
  """ slices the array in order to get the average speeds(data[i][5]) that corresponds to the code """
  """ converts each element to float type, with the expected format """
  """ calculates the mean and return a float with expected format """
  speeds = [float(data[i][5].replace(',', '.')) for i in range(0,len(data)) if data[i][1] == code]
  return float(format(mean(speeds), '.3f'))

""" tested """
def extract_diff_to_first(code):
  """ slices the array in order to get the race time(results[i]['time']) for each driver that corresponds to the code """
  """ calculates the abs difference to the race winner and return a float with expected format """
  t = [results[i]['time'] for i in range(0, len(results)) if results[i]['code'] == code][0]
  return float(format(abs(results[0]['time'] - t), '.3f'))

""" tested """  
def build_result():
  """ slices the array in order to get all the codes """
  """ for each code extract all the required informations and append the dictionary in the array """
  """ sort the results by the time and associate the position """
  global results
  codes = set([data[i][1] for i in range(0,len(data))])
  for code in codes:
    d = {}
    d['code'] = code
    d['name'] = extract_name(code)
    d['laps'] = extract_laps(code)
    d['time'] = extract_race_time(code)
    results.append(d)
  results = sorted(results, key=lambda k: k['time'])
  for i, item in enumerate(results):
    item['position'] = i + 1

""" tested """
def build_drivers_best_lap():
  """ for each item from results extract all the required informations and append the dictionary in the array"""
  for item in results:
    d = {}
    d['name'] = item['name']
    d['best_lap'] = extract_best_lap(item['code'])
    drivers_best_laps.append(d)

""" tested """
def build_race_best_lap():
  """ assign to 'race_best_lap' the min value from the drivers best lap array"""
  global race_best_lap
  race_best_lap = min(drivers_best_laps, key=lambda k: k['best_lap'])

""" tested """
def build_drivers_avg_speed():
  """ for each item from results extract all the required informations and append the dictionary in the array"""
  for item in results:
    d = {}
    d['name'] = item['name']
    d['avg_speed'] = extract_avg_speed(item['code'])
    drivers_avg_speed.append(d)

""" tested """
def build_drivers_diff_to_first():
  """ for each item from results extract all the required informations and append the dictionary in the array"""
  for item in results:
    d = {}
    d['name'] = item['name']
    d['to_first'] = extract_diff_to_first(item['code'])
    drivers_diff_to_first.append(d)

def print_results():
  print("RESULTS")
  for item in results:
    print(f"Position: {item['position']}\tCode: {item['code']}\tName: {item['name']}\t\tLaps: {item['laps']}\tTime: {item['time']} seconds")
  print()

def print_drivers_best_lap():
  print("DRIVERS BEST LAP")
  for item in drivers_best_laps:
    print(f"Name: {item['name']}\tBest Lap: {item['best_lap']} seconds")
  print()

def print_race_best_lap():
  print("RACE BEST LAP")
  print(f"Name: {race_best_lap['name']}\tBest Lap: {race_best_lap['best_lap']} seconds\n")

def print_drivers_avg_speed():
  print("DRIVERS AVERAGE SPEED")
  for item in drivers_avg_speed:
    print(f"Name: {item['name']}\tAvg Speed: {item['avg_speed']}")
  print()

def print_drivers_diff_to_first():
  print("DRIVERS DIFFERENCE TO FIRST")
  for item in drivers_diff_to_first:
    print(f"Name: {item['name']}\tFrom First: {item['to_first']} seconds")
  print()

def menu_options():
  print("MENU")
  print("Choose an option and press 'enter'")
  print("\tRace results: '1'")
  print("\tDriver's best lap: '2'")
  print("\tRace best lap: '3'")
  print("\tDriver's avg speed: '4'")
  print("\tDriver's diff to first: '5'")
  print("\tQuit: '0'")
  return int(input())

if __name__ == "__main__":
  parse()
  build_result()
  build_drivers_best_lap()
  build_race_best_lap()
  build_drivers_avg_speed()
  build_drivers_diff_to_first()
  
  op = menu_options()
  while op != 0:
    if op == 1:
      print_results()
    elif op == 2:
      print_drivers_best_lap()
    elif op == 3:
      print_race_best_lap()
    elif op == 4:
      print_drivers_avg_speed()
    elif op == 5:
      print_drivers_diff_to_first()
    else:
      print("invalid option")
    op = menu_options()

