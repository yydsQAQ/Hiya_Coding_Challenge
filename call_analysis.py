class CallEvent:
    def __init__(self, from_person, to, timestamp):
        self.from_person = from_person
        self.to = to
        self.timestamp = timestamp

class Call(CallEvent):
    pass

class Hangup(CallEvent):
    pass

def calculate_average_call_durations(events):
    call_starts = {}  # Starting timestamp of each call
    total_durations = {}  # Total duration of calls per caller
    call_counts = {}  # Number of calls made by each caller

    for event in events:
        # Construct a unique key for each call
        key = (event.from_person, event.to)

        if isinstance(event, Call):
            call_starts[key] = event.timestamp
        elif isinstance(event, Hangup):
            # Reverse the key for hangup if 'from' and 'to' are swapped
            reverse_key = (event.to, event.from_person)
            if reverse_key in call_starts:
                start_time = call_starts.pop(reverse_key)
                duration = event.timestamp - start_time
                # Accumulate total duration and count for the caller
                caller = reverse_key[0]
                if caller in total_durations:
                    total_durations[caller] += duration
                    call_counts[caller] += 1
                else:
                    total_durations[caller] = duration
                    call_counts[caller] = 1
            elif key in call_starts:
                start_time = call_starts.pop(key)
                duration = event.timestamp - start_time
                # Accumulate total duration and count for the caller
                caller = key[0]
                if caller in total_durations:
                    total_durations[caller] += duration
                    call_counts[caller] += 1
                else:
                    total_durations[caller] = duration
                    call_counts[caller] = 1

    # Calculate average call duration for each caller
    average_durations = {caller: total / call_counts[caller] for caller, total in total_durations.items()}

    # Identify callers with average duration under 5 seconds
    short_callers = [caller for caller, avg in average_durations.items() if avg < 5]

    return short_callers

# Example input
# To test my program with different inputs, please enter your input below accordingly.
events = [
    Call("Bob", "Alice", 1711132463),
    Call("Carl", "Doug", 1711132465),
    Hangup("Alice", "Bob", 1711132467),
    Call("Ed", "Frank", 1711132481),
    Hangup("Carl", "Doug", 1711132482),
    Call("Bob", "Doug", 1711132483),
    Hangup("Doug", "Bob", 1711132484),
    Hangup("Ed", "Frank", 1711132501)
]


short_callers = calculate_average_call_durations(events)
print(short_callers)  # Expected output: ['Bob']
