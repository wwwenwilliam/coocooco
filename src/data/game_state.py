
class GlobalState:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalState, cls).__new__(cls)
            cls._instance.rage_level = 90.0
            cls._instance.max_rage = 100.0
            cls._instance.is_crashout = False
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    def add_rage(self, amount):
        if self.is_crashout:
            return # Already crashing out
            
        self.rage_level += amount
        self.rage_level = min(self.rage_level, self.max_rage)
        
        if self.rage_level >= self.max_rage - 0.01:
            self.trigger_crashout()
            
    def trigger_crashout(self):
        print("CRASHOUT TRIGGERED!")
        self.is_crashout = True
        # Could set a timer to reset? Or reset manually.
        
    def reset_rage(self):
        self.rage_level = 0.0
        self.is_crashout = False
