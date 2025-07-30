from lap_time import LapTimeProcessor

if __name__ == "__main__":
    processor = LapTimeProcessor(time_format='%H:%M:%S.%f')
    laps = processor.read_lap_data('example_lap_data.csv')
    lap_times = processor.calculate_lap_times(laps)
    processor.print_scoreboard(lap_times) 