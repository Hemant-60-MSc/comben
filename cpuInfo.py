class CpuInfo:
    
    def __init__(self, P_CORE_LINUX_FILE_PATH, E_CORE_LINUX_FILE_PATH):
        # Reading P-Core information
        with open(P_CORE_LINUX_FILE_PATH, 'r', encoding = "utf-8") as p_core_file:
            self.p_core_range = p_core_file.read().splitlines()
        
        self.p_core_range = [int(i) for i in self.p_core_range[0].split('-')]

        # Reading E-core information
        with open(E_CORE_LINUX_FILE_PATH, 'r', encoding = "utf-8") as e_core_file:
            self.e_core_range = e_core_file.read().splitlines()
        
        self.e_core_range = [int(i) for i in self.e_core_range[0].split('-')]

    def get_e_core_range(self):
        return self.e_core_range

    def get_p_core_range(self):
        return self.p_core_range

    '''
    parameters : int
        core_id = id assigned to a core
    return : str
        "P" : if core is a performance core
        "E" : if core is an efficient core
        "N" : if core is N/A or invalid/unassigned
        
    '''
    def classify_core_id(self, core_id:int) -> str:
        if core_id >= self.p_core_range[0] and core_id <= self.p_core_range[1]:
            return "P"
        elif core_id >= self.e_core_range[0] and core_id <= self.e_core_range[1]:
            return "E"
        else:
            return "N"
