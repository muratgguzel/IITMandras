class StopWatch:
    def capture_time(self, time):
        pass

    def find_interval(self, start, stop):
        startTime = self.capture_time(start)
        stopTime = self.capture_time(stop)
        interval = stopTime - startTime

        return interval

class QuartzStopWatch(StopWatch):
    def capture_time(self, time):
        #quartz specific logic- example : time*1000
        return time


class OpticStopWatch(StopWatch):
    def capture_time(self, time):
        #optic specific logic - example : time *100
        return time


