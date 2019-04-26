#! /bin/bash/python

# A Backtracking program  in Python to solve the knight / knave problem as follows:
# BRAINTEASER: On a certain island there live only knights, who always tell the truth, and knaves, who always lie.
# One day you find 10 island natives standing in a circle. Each one states: "Both people next to me are knaves!"
#
# Of the 10 in the circle, what is the minimum possible number of knights?
# I figured this would be a decent way to illustrate the use of backtracking algorithms that rely on the all
# so important notion of recursion.

class KKBackTracker:
    # Members
    knight = 1
    knave = 0
    idx = 0
    # debug / info prints
    debug = True

    # 2D array representing the flattened circle of individuals
    arr = []

    # array tracking if an individual has been assigned to the corresponding position
    valid = []

    flag = False

    # Methods
    # initialize array of length size with values corresponding to neither knights nor knaves
    def __init__(self, size):
        for i in range(size):
            self.arr.append(2)
            self.valid.append(0)

    # Utility function to print the flattened circle of individuals as solved
    def print_flattened_circle(self):
        for val in self.arr:
            if val == self.knight:
                print('Knight')
            if val == self.knave:
                print('Knave')

    # Return boolean that indicates if condition for knight is met
    def satisfies_knight_condition(self, arr, idx):
        # knight condition: idx-1 and idx+1 must both be knaves (neither can be a knight)
        if ((self.prev_neighbor(arr, idx) != self.knight and self.next_neighbor(arr, idx) != self.knight)):
            self.debug_print(['Knight condition met.'])
            return True
        return False

    # Return boolean that indicates if condition for knave is met
    def satisfies_knave_condition(self, arr, idx):
        # knave condition: idx-1 and idx+1 cannot both be knaves
        prev = self.prev_neighbor(arr,idx)
        next = self.next_neighbor(arr,idx)
        self.debug_print(['prev neighbor: {}'.format(prev),
                          'next neighbor: {}'.format(next),
                          'knave = {}'.format(self.knave)])
        if ((prev != self.knave and next == self.knave) or
                (prev == self.knave and next != self.knave) or
                (prev != self.knave and next != self.knave)):
            self.debug_print(['Knave condition met.'])
            return True
        else:
            self.debug_print(['Knave condition not met.'])
            return False

    # calculate previous neighbor
    def prev_neighbor(self, arr, idx):
        return arr[idx - 1] # note: if idx = 0 this will result in -1 which is the last element in the list


    # calculate next neighbor
    def next_neighbor(self, arr, idx):
        if idx < (len(arr) - 1):
            val = arr[idx + 1]
        else:
            val =  arr[0]
        return val

    # Check whether it will be legal to assign num to current position based on previous assignments
    # Returns a boolean that indicates whether it will be legal to assign num to the given slot
    def check_prev_location_is_safe(self, arr, idx):
        # if prev idx is a knight, check that the proposed assignment doesn't break any rules
        if (arr[idx-1] == self.knight):
            self.debug_print(['prev position is a knight, checking validity'])
            return self.satisfies_knight_condition(arr, idx-1)

        # if prev idx is a knave, check that the proposed assignment doesn't break any rules
        if (arr[idx-1] == self.knave):
            self.debug_print(['prev position is a knave, checking validity'])
            return self.satisfies_knave_condition(arr, idx-1)

        if (arr[idx-1] == 2):
            return True


    # Checks whether it will be legal to assign num to current position based on current assignment
    # This method is unused here, but would be applicable for something like backtrack solving of a Sudoku grid
    def check_curr_location_is_safe(self, arr, idx):
        # if current index is Knight (1)
        if (arr[idx] == self.knight):
            self.debug_print(['Current position is a knight, checking validity'])
            return self.satisfies_knight_condition(arr, idx)

            # if current index is Knave (0)
        if (arr[idx] == self.knave):
            self.debug_print(['Current position is a knave, checking validity'])
            return self.satisfies_knave_condition(arr, idx)


    # Check to see if we have assigned all slots to either knight or knave
    def check_all_valid(self):
        for i in range(len(self.arr)):
            if(not self.check_curr_location_is_safe(self.arr, i)):
                return False
            else:
                return True

    # Check to make sure everything is assigned
    def check_all_assigned(self):
        for i in self.valid:
            if i == 0:
                return 0

        if self.flag == False:
            self.reset_valid()
            return 1
        if self.flag == True:
            return 2

    # Reset the validity tracker.
    # This is done so we go throug the circle twice to ensure everything is valid
    def reset_valid(self):
        for i in range(len(self.valid)):
            self.valid[i] = 0
        print('RESETTING VALIDITY TRACKER')
        self.flag = True


    # debug print for items in string array
    def debug_print(self, string):
        if(self.debug):
            for i in string:
                print(i)


    def increment_idx(self):
        if(self.idx < (len(self.arr)-1)):
            self.idx = self.idx + 1
        else:
            self.idx = 0

    # solves the problem!
    def solve(self):
        # increment to the next position in the circle
        self.increment_idx()

        # If there is no unassigned location, we are done
        if (self.check_all_assigned() == 2):
            self.debug_print(['\nEverything assigned and valid!\n'])
            return True

        # Test 0 first (knave), then test 1 (knight)
        # This will place priority on assignments being knaves
        for num in [0,1]:
            self.debug_print(['\nIndex: {}'.format(self.idx), 'checking value: {}'.format(num)])

            # make tentative assignment
            self.arr[self.idx] = num
            # check to see that this assignment is safe for the previous element
            if (self.check_prev_location_is_safe(self.arr, self.idx) and self.check_curr_location_is_safe(self.arr, self.idx)):
                self.debug_print(['satisfies conditions'])
                self.valid[self.idx] = 1

                if (self.solve()):
                    self.debug_print(['Returning True'])
                    return True

                # Failure, unmake & try again
                self.arr[self.idx] = 0
                self.valid[self.idx] = 0
                self.idx = self.idx - 1

        # Trigger backtracking
            self.debug_print(['Failed.  Backtracking...\n'])
        return False


# Main
if __name__ == "__main__":
    print('Starting...')

    # Instantiate circle of 10 individuals
    KKB = KKBackTracker(10)

    # If sucess print the circle of individuals
    if (KKB.solve()):
        print('\n\n\n')
        print('Success! Order of individuals is: \n')
        KKB.print_flattened_circle()
    else:
        print
        "No solution exists"
