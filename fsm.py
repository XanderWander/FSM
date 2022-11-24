from color import blue, reset, r, g, b
import random


class State:
    def __init__(self, name: str, transitions: dict[str, str] = None, accepting: bool = False):
        self.name = name
        self.transitions = {}
        self.accepting = accepting
        if transitions is not None:
            self.transitions = transitions

    def define_transition(self, edge: str, target: str):
        self.transitions[edge] = target
        return self


class StateMachine:
    """
    This class represents a Finite state machine and handles all interactions
    between states, see State class for information about defining transitions

    Args:
    states (list[State]): A list of states in this state machine
    on_undefined (string = "stay"): "stay" or "doom", what to do when a transition is not defined
    """

    def __init__(self, states: list[State], start: str, on_undefined: str = "stay"):
        self.states = states
        self.state_names = [s.name for s in self.states]
        self.on_undefined = on_undefined
        self.current_state = start
        if start not in self.state_names:
            raise ValueError(f"Starting state '{start}' not in provided states")
        if self.on_undefined == "doom":
            self.states.append(State("Doom"))

    def get_state(self, name) -> State:
        """
        Get a State by name

        Args:
        name (string): The name of the state to find

        Returns:
        State: The found State or None if fnot found
        """
        for state in self.states:
            if state.name == name:
                return state
        raise ValueError(f"State '{name}' not in available states")

    def use(self, edge: str) -> State:
        """
        Apply a transition to the state machine to (posibly) go to a new state

        Args:
        edge (string): The name of the transition to follow

        Returns:
        State: The State the machine is on after using the transition
        """
        current = self.get_state(self.current_state)
        if edge in current.transitions:
            self.current_state = current.transitions[edge]
        elif self.on_undefined == "doom":
            self.current_state = "Doom"
        return self.get_state(self.current_state)


class VendingMachine:
    """
    A VendingMachine class to simulate a vanding machine
    use self.start() to start to simulation

    Args:
    stock (list[[str, float, int]]): A list of items as [name, price, stock]
    payment_fail_chance (int=10): The percentage of chance that a transaction will fail (0 = no chance to fail)
    """

    def __init__(self, stock: list[list], payment_fail_chance=10):
        sleep = State("Sleep", {"wake": "Select"})
        select = State("Select", {
            "cancel": "Sleep",
            "unavailable": "Select",
            "selected": "Payment"
        })
        payment = State("Payment", {
            "cancel": "Sleep",
            "card": "Code"
        })
        code = State("Code", {
            "fill": "Transaction",
            "cancel": "Sleep"
        })
        transaction = State("Transaction", {
            "accepted": "Complete",
            "failed": "Failed"
        })
        complete = State("Complete", {
            "take": "Sleep"
        })
        failed = State("Failed", {
            "again": "Payment",
            "cancel": "Sleep"
        })
        self.machine = StateMachine([sleep, select, payment, code, transaction, complete, failed], "Sleep")
        self.selected = None
        self.stock = stock
        self.chance = payment_fail_chance
        self.skip_clear = False

    def start(self):
        """
        Start the vending machine simulation, this will start a while
        loop constantly requiring input from the user to be used.
        """

        while True:
            current = self.machine.current_state

            if current == "Sleep":
                print("\n" * 100)
                print(f"Welcome to the VendingMachine.")
                print(f"Type {b('wake')} to start.")

            if current == "Select":
                if not self.skip_clear:
                    print("\n" * 100)
                else:
                    self.skip_clear = False
                print("Please select:")
                for option in self.stock[0:-1]:
                    if option[2] > 0:
                        print(f"{b(option[0])}", end=", ")
                print(f"{b(self.stock[-1][0])}", end=".\n")
                print(f"Or type {b('cancel')} to stop.")
                inp = input(": ")

                found = False
                for option in self.stock:
                    if option[0] == inp:
                        if option[2] > 0:
                            self.machine.use("selected")
                        else:
                            self.machine.use("unavailable")
                            print("\n" * 100)
                            print(f"\nThe {b(option[0])} is currently {r('out of stock')}.\n")
                            self.skip_clear = True
                        self.selected = option
                        found = True
                        break
                if not found:
                    self.machine.use(inp)
                continue

            if current == "Payment":
                print("\n" * 100)
                print(f"You have selected {b(self.selected[0])} which costs {blue}{self.selected[1]:.2f}{reset}.")
                print(f"Please type {b('card')} to present your card.")
                print(f"Or type {b('cancel')} to stop.")

            if current == "Code":
                print("\n" * 100)
                print(f"Please type {b('fill')} to fill in your passcode.")
                print(f"Or type {b('cancel')} to stop.")

            if current == "Transaction":
                print("\n" * 100)
                if random.randint(0,100) < self.chance:
                    self.machine.use("failed")
                else:
                    self.machine.use("accepted")
                    print(f"The transaction was {g('successfull')}!")
                continue

            if current == "Complete":
                print(f" > {b(self.selected[0])}")
                print(f"Type {b('take')} to take the product and exit.")
                while True:
                    inp = input(": ")
                    if inp == "take":
                        break
                self.machine.use("take")
                for i, o in enumerate(self.stock):
                    if o == self.selected:
                        self.stock[i][2] -= 1
                continue

            if current == "Failed":
                print("\n" * 100)
                print(f"The transaction has {r('failed')}.")
                print(f"Type {b('again')} to try again or {b('cancel')} to stop.")

            inp = input(": ")
            self.machine.use(inp)


def main():
    machine = VendingMachine(
        stock=[
            ["Coffee", 3.00, 0],
            ["Twix", 1.50, 2],
            ["Mars", 1.00, 15],
            ["Milky way", 1.20, 11],
        ],
        payment_fail_chance=10
    )
    machine.start()


if __name__ == "__main__":
    main()
