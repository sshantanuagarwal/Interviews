import csv
from datetime import datetime
from typing import List, Dict
from tabulate import tabulate

class LapTimeProcessor:
    def __init__(self, time_format='%H:%M:%S.%f'):
        self.time_format = time_format

    def read_lap_data(self, file_path: str) -> List[Dict]:
        """Reads lap data from a CSV file. Expects columns: driver, lap, timestamp."""
        laps = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                laps.append(row)
        return laps

    def calculate_lap_times(self, laps: List[Dict]) -> Dict[str, List[float]]:
        """Calculates lap times for each driver. Returns a dict: driver -> list of lap times in seconds."""
        driver_laps = {}
        import pprint
        pprint.pprint(laps)
        for row in laps:
            driver = row['driver']
            lap = int(row['lap'])
            timestamp = datetime.strptime(row['timestamp'].strip(), self.time_format)
            if driver not in driver_laps:
                driver_laps[driver] = []
            driver_laps[driver].append((lap, timestamp))
        # Sort laps and calculate differences
        driver_lap_times = {}
        for driver, lap_list in driver_laps.items():
            lap_list.sort()  # sort by lap number
            times = [t for _, t in lap_list]
            lap_times = [(times[i] - times[i-1]).total_seconds() for i in range(1, len(times))]
            driver_lap_times[driver] = lap_times
        return driver_lap_times
    
    def print_scoreboard(self, driver_lap_times: Dict[str, List[float]]) -> None:
        """Prints a formatted scoreboard showing lap times for each driver."""
        print("\n" + "="*60)
        print("🏁 LAP TIME SCOREBOARD 🏁")
        print("="*60)
        
        # Calculate statistics for each driver
        driver_stats = {}
        for driver, lap_times in driver_lap_times.items():
            if lap_times:
                avg_time = sum(lap_times) / len(lap_times)
                best_time = min(lap_times)
                total_time = sum(lap_times)
                driver_stats[driver] = {
                    'avg_time': avg_time,
                    'best_time': best_time,
                    'total_time': total_time,
                    'lap_count': len(lap_times)
                }
        
        # Sort drivers by best lap time
        sorted_drivers = sorted(driver_stats.items(), key=lambda x: x[1]['best_time'])
        
        # Prepare table data
        table_data = []
        headers = ["Pos", "Driver", "Best Lap (s)", "Avg Lap (s)", "Total Time (s)", "Laps"]
        
        for i, (driver, stats) in enumerate(sorted_drivers, 1):
            table_data.append([
                f"{i}",
                driver,
                f"{stats['best_time']:.3f}",
                f"{stats['avg_time']:.3f}",
                f"{stats['total_time']:.3f}",
                stats['lap_count']
            ])
        
        # Print main scoreboard table
        print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="center"))
        print("="*60)
        
        # Print detailed lap times table
        print("\n📊 DETAILED LAP TIMES:")
        print("-" * 40)
        
        detailed_data = []
        detailed_headers = ["Driver", "Lap", "Time (s)"]
        
        for driver, lap_times in driver_lap_times.items():
            for i, lap_time in enumerate(lap_times, 1):
                detailed_data.append([driver, f"Lap {i}", f"{lap_time:.3f}"])
        
        print(tabulate(detailed_data, headers=detailed_headers, tablefmt="simple", stralign="left"))