OPERATIONS = {
    '+': 2,
    '-': 3,
    '*': 4,
    '/': 8
}

class Processor:
    def __init__(self, id):
        self.id = id
        self.memory = []
        self.job = None
        self.eta = 0

class MatrixSystem:
    def __init__(self, P=7):
        self.processors = [Processor(i) for i in range(P)]
        self.central_processor = self.processors[0]
        self.history = []

    def _update_history(self, indices):
        step = [0 for _ in self.processors]
        for i in indices:
            step[i] = 1
        self.history.append(step)

    def _route(self, receiver, subtree):
        sender = next(
            proc for proc in self.processors if subtree in proc.memory
        )
        if receiver == self.central_processor:
            self._update_history([0, sender.id])
        elif sender == self.central_processor:
            self._update_history([0, receiver.id])
        else:
            self._update_history([0, sender.id])
            self._update_history([0, receiver.id])

    def _sync(self, processor, job):
        tree = job
        if (tree.lleaf.type == 'SUBTREE' and
            tree.lleaf.value not in processor.memory):
            self._route(processor, tree.lleaf.value)
        if (tree.rleaf.type == 'SUBTREE' and
            tree.rleaf.value not in processor.memory):
            self._route(processor, tree.rleaf.value)

    def apply_job(self, job):
        for processor in self.processors:
            if processor.job == None:
                processor.job = job
                processor.eta = OPERATIONS[job.operation.value]
                self._sync(processor, job)
                return
        self.next_tick()
        self.apply_job(job)

    def next_tick(self):
        time_spent = max(self.processors, key=lambda p: p.eta).eta
        active = [proc.id for proc in self.processors if proc.job != None]
        for _ in range(time_spent):
            self._update_history(active)
        
        for processor in self.processors:
            if processor.job == None:
                continue
            processor.memory.append(processor.job)
            processor.job = None
            processor.eta = 0

def get_jobs(token, result):
    if result == []:
        for _ in range(token.value.level + 1):
            result.append([])

    if token.type == 'SUBTREE':
        tree = token.value
        level = tree.level
        result[level].append(tree)

        if tree.lleaf.type == 'SUBTREE':
            get_jobs(tree.lleaf, result)
        if tree.rleaf.type == 'SUBTREE':
            get_jobs(tree.rleaf, result)
    
    return result

def model_matrix_system(tree):
    system = MatrixSystem()
    jobs = get_jobs(tree, [])

    for level in jobs:
        for operation in OPERATIONS.keys():
            for job in level:
                if job.operation.value == operation:
                    system.apply_job(job)
            system.next_tick()

    return system

def evaluate_matrix_system(tree, system):
    jobs = get_jobs(tree, [])
    t_seq = 0
    for level in jobs:
        for job in level:
            t_seq += OPERATIONS[job.operation.value]

    t_par = len(system.history)
    S = t_seq / t_par
    E = S / len(system.processors)

    return t_par, S, E
