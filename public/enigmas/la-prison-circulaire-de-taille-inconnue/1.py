import random

def UpperBound(p, l):
    p.counter += 1
    if p.counter <= p.r:
        p.is_active = l or p.is_active
        return f"[Upper Bound] ({p.counter}/{p.r})"
    else:
        p.is_active = l and p.is_active
        B = 2**p.r
        if p.counter == B + p.r:
            if p.is_active:
                p.phase = 'Next'
                p.B = B
                return f"[Upper Bound] ({B}/{B}) B = {p.B}"
            p.counter = 0
            p.is_active = p.is_captain
            p.r += 1
            return f"[Upper Bound] ({B}/{B}) repeat with r = {p.r}"
        return f"[Upper Bound] ({p.counter-p.r}/{B})"

def PrepareAnnouncement(p, predicate, name):
    p.phase = name
    p.is_active = predicate
    p.counter = 0

def Announcement(p, l, name, name_next):
    p.counter += 1
    p.is_active = l or p.is_active
    if p.counter == p.B:
        p.phase = name_next
        return f"[{name}] ({p.counter}/{p.B}) Announcement = {p.is_active}", p.is_active
    return f"[{name}] ({p.counter}/{p.B})", None

class Prisoner:
    def __init__(self, is_captain=False):
        self.is_captain = is_captain
        self.is_active = is_captain
        self.phase = 'Upper Bound'
        self.r, self.B = 1, None
        self.counter = 0
        self.number = 1 if is_captain else None
        self.is_candidate = False
        self.n_candidates = 0
        self.i, self.d = 1, 1

    def log(self, msg, day):
        if self.is_captain:
            print(f'[{day}]'+msg)

    def turn_on(self):
        return self.is_active
    
    def see_light(self, l, day):

        # Execute current phase using today's light input 

        current_phase = self.phase
        if current_phase == 'Upper Bound':
            msg = UpperBound(self, l)
            self.log(msg, day)

        if current_phase == 'Unnumbered Announcement':
            msg, answer = Announcement(self, l, 'Unnumbered Announcement', 'Prepare Candidate Selection Day')
            if answer is not None:
                if not answer:
                    self.log(f"[End] everyone is numbered, and everyone knows n={self.d}", day)
                    return True
            self.log(msg, day)
                
        if current_phase == 'Candidate Selection Day':
            self.log(f"[{current_phase}]", day)
            self.is_candidate = l
            self.phase = 'Prepare Candidate Announcement'

        if current_phase == 'Candidate Announcement':
            msg, answer = Announcement(self, l, 'Candidate Announcement', 'Prepare Candidate Announcement')
            if answer is not None:
                self.i += 1
                if answer:
                    self.n_candidates += 1
                self.log(msg + f', n_candidates = {self.n_candidates}', day)
                if self.i > self.d:
                    self.phase = 'Prepare Unnumbered Candidate Announcement'
            else:
                self.log(msg, day)

        if current_phase == 'Unnumbered Candidate Announcement':
            msg, answer = Announcement(self, l, 'Unnumbered Candidate Announcement', 'Next')
            if answer is not None:
                if answer:
                    if self.n_candidates == 1:
                        self.d += 1
                        if self.is_candidate:
                            self.number = self.d
                    self.log(msg + f', d = {self.d}', day)
                else:
                    self.log(msg + ', retry', day)
                self.i = 1
                self.n_candidates = 0
            else:
                self.log(msg, day)

        # Preparation for tomorrow

        if self.phase == 'Prepare Candidate Selection Day':
            self.is_active = False
            self.flip = False
            if self.number:
                self.flip = random.random() < .5
                self.is_active = self.flip 
            self.phase = 'Candidate Selection Day'
        if self.phase == 'Prepare Unnumbered Candidate Announcement':
            PrepareAnnouncement(self, self.is_candidate & (self.number is None), 'Unnumbered Candidate Announcement')
        if self.phase == 'Prepare Candidate Announcement':
            PrepareAnnouncement(self, (self.number == self.i) & self.flip, 'Candidate Announcement')
        if self.phase == 'Next':
            PrepareAnnouncement(self, self.number is None, 'Unnumbered Announcement')

def simulate_prisoners(n):
    prisoners = [Prisoner(i==0) for i in range(n)]

    day = 0
    while True:
        day += 1
        prisoners_shuffled = random.sample(prisoners, len(prisoners))

        lights = []
        for i in range(n):
            lights.append(prisoners_shuffled[i].turn_on())
        for i in range(n):
            stop = prisoners_shuffled[(i+1) % n].see_light(lights[i], day)
        if stop:
            break

if __name__ == "__main__":
    simulate_prisoners(5)