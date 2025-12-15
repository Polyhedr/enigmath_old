import itertools
import numpy as np

def proper_subsets(k):
    S = list(range(1, k+1))
    subsets = []
    for r in range(1, k):
        for combo in itertools.combinations(S, r):
            subsets.append(list(combo))
    return subsets

class Prisoner:
    def __init__(self, is_captain=False):
        self.is_captain = is_captain
        self.is_active = is_captain
        self.phase = 'Upper Bound'
        self.r, self.B = 1, None
        self.counter = 0
        self.k = 2
        self.proper_subsets = proper_subsets(self.k)
        self.proper_subsets_index = 0
        self.Iprime = []
        self.j = 1 if is_captain else 2
        self.i = 1
        self.eqs = []

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

        if current_phase == 'Union Flash':
            self.log(f"[{current_phase}], I={self.proper_subsets[self.proper_subsets_index]}, i={self.i}", day)
            self.is_in_T = l
            self.phase = 'Prepare First Announcement'

        if current_phase == 'First Announcement':
            msg, answer = Announcement(self, l, 'First Announcement', 'Prepare Second Announcement')
            if answer is not None:
                self.first_announcement = answer
            self.log(msg, day)

        if current_phase == 'Second Announcement':
            msg, answer = Announcement(self, l, 'Second Announcement', 'Next')
            if answer is not None:
                if self.first_announcement and answer:
                    self.k += 1
                    if (self.j == self.i) & (not self.is_in_T):
                        self.j = self.k
                    self.proper_subsets = proper_subsets(self.k)
                    self.proper_subsets_index = 0
                    self.Iprime = []
                    self.eqs = []
                    self.i = 1
                else:
                    self.phase = 'Prepare First Announcement'
                    if self.first_announcement:
                        self.Iprime.append(self.i)
                    self.i += 1
                    if self.i > self.k:
                        self.phase = 'Next'
                        self.i = 1
                        v = np.zeros(self.k)
                        v[np.array(self.proper_subsets[self.proper_subsets_index]) - 1] += 1
                        v[np.array(self.Iprime) - 1] -= 1
                        self.eqs.append(v)
                        self.proper_subsets_index += 1
                        self.Iprime = []
                        if self.proper_subsets_index >= len(self.proper_subsets):
                            _, S, Vt = np.linalg.svd(self.eqs)
                            null_mask = (S < 1e-10)
                            null_space = Vt[null_mask].T
                            assert null_space.shape[1] == 1
                            x = null_space[:,0]
                            self.log(f"[End] everyone knows n={round(sum(x)/x[0])}", day)
                            return True
                self.log(msg+f', k={self.k}', day)
            else:
                self.log(msg, day)
        
        # Preparation for tomorrow            
        
        if self.phase == 'Next':
            self.is_active = self.j in self.proper_subsets[self.proper_subsets_index]
            self.phase = 'Union Flash'
        if self.phase == 'Prepare First Announcement':
            PrepareAnnouncement(self, (self.j == self.i) & self.is_in_T, 'First Announcement')
        if self.phase == 'Prepare Second Announcement':
            PrepareAnnouncement(self, (self.j == self.i) & (not self.is_in_T), 'Second Announcement')