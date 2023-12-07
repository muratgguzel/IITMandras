class NaiveStopWatch:
    def find_interval(self, start, stop):
        pass

class NaiveQuartzStopWatch(NaiveStopWatch):
    def capture_quartz_time(self, time):
        # quartz specific logic
        return time

    def find_interval(self, start, stop):
        startTime = self.capture_quartz_time(start)
        stopTime = self.capture_quartz_time(stop)
        interval = stopTime - startTime

        return interval

class NaiveOpticStopWatch(NaiveStopWatch):
    def capture_optic_time(self, time):
        #optic specific logic
        return time

    def find_interval(self, start, stop):
        startTime = self.capture_optic_time(start)
        stopTime = self.capture_optic_time(stop)
        interval = stopTime - startTime

        return interval
