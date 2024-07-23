import json
import sys
from datetime import datetime, timedelta

# Sequenze di escape ANSI per colori
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
RESET = '\033[0m'

# Funzione per calcolare la differenza in ore e minuti
def calculate_time_difference(worked_time_str, min_worked_time_str="08:24"):
    worked_time = datetime.strptime(worked_time_str, '%H:%M')
    min_worked_time = datetime.strptime(min_worked_time_str, '%H:%M')
    diff = worked_time - min_worked_time
    return diff

# Funzione per formattare la differenza di tempo
def format_time_difference(diff):
    total_minutes = abs(diff.total_seconds()) // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60
    sign = "-" if diff.total_seconds() < 0 else "+"
    return f"{sign}{int(hours):02}:{int(minutes):02}"

# Funzione per calcolare la percentuale di deviazione
def calculate_percentage_deviation(total_diff, total_min_worked_time):
    total_diff_seconds = total_diff.total_seconds()
    total_min_worked_seconds = total_min_worked_time.total_seconds()
    deviation_percentage = (total_diff_seconds / total_min_worked_seconds) * 100
    return deviation_percentage

# Funzione per generare il report
def generate_report(data):
    min_worked_time_str = "08:24"
    total_worked_time = timedelta()
    total_min_worked_time = timedelta(hours=8, minutes=24) * len(data)

    report_lines = []

    for entry in data:
        worked_date = entry['worked_date']
        worked_time_str = entry['worked_time']
        
        worked_time = datetime.strptime(worked_time_str, '%H:%M')
        worked_timedelta = timedelta(hours=worked_time.hour, minutes=worked_time.minute)
        total_worked_time += worked_timedelta

        diff = calculate_time_difference(worked_time_str, min_worked_time_str)
        formatted_diff = format_time_difference(diff)

        # Colorare il testo
        color = GREEN if diff.total_seconds() >= 0 else RED
        
        report_lines.append(f"{worked_date}: Differenza = {color}{formatted_diff}{RESET}")

    total_diff = total_worked_time - total_min_worked_time
    formatted_total_diff = format_time_difference(total_diff)
    deviation_percentage = calculate_percentage_deviation(total_diff, total_min_worked_time)

    # Convertire i tempi totali in ore e minuti
    total_worked_hours = total_worked_time.total_seconds() // 3600
    total_worked_minutes = (total_worked_time.total_seconds() % 3600) // 60

    total_min_worked_hours = total_min_worked_time.total_seconds() // 3600
    total_min_worked_minutes = (total_min_worked_time.total_seconds() % 3600) // 60

    # Creazione del report formattato
    report_lines.append("\nREPORT:")
    report_lines.append("+---------------------------------------+")
    report_lines.append(f"| {BLUE}Total Planned Time{RESET}     -> {int(total_min_worked_hours)} h {int(total_min_worked_minutes)} m")
    report_lines.append("+---------------------------------------+")
    report_lines.append(f"| {BLUE}Total Worked Time{RESET}      -> {int(total_worked_hours)} h {int(total_worked_minutes)} m")
    report_lines.append("+---------------------------------------+")
    report_lines.append(f"| {PURPLE}Deviation{RESET}              -> {GREEN if total_diff.total_seconds() >= 0 else RED}{formatted_total_diff}{RESET}")
    report_lines.append("+---------------------------------------+")
    report_lines.append(f"| {PURPLE}Deviation Percentage{RESET}   -> {deviation_percentage:.2f}%")
    report_lines.append("+---------------------------------------+")

    return "\n".join(report_lines)

# Funzione principale
def main(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    report = generate_report(data)
    print(report)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python report_generator.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    main(json_file_path)
