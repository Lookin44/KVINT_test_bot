from transitions import Machine


class PizzaBoy:  # Отсылочка к ремастеру строй игры) (GTA Vice City)
    """Класс описывющий стейт-машину для бота."""

    state = ['waiting', 'pizza_size', 'pay_method', 'confirm', 'cancel', 'done']

    def __init__(self):
        self.pizza_size = None
        self.pay_method = None

        self.machine = Machine(model=self, states=PizzaBoy.state, initial='waiting')

        self.machine.add_transition(trigger='start', source='waiting', dest='pizza_size')
        self.machine.add_transition(trigger='next', source='pizza_size', dest='pay_method')
        self.machine.add_transition(trigger='next', source='pay_method', dest='confirm')
        self.machine.add_transition(trigger='done', source='confirm', dest='done')
        self.machine.add_transition(trigger='cancel', source='confirm', dest='cancel')
        self.machine.add_transition(trigger='cancel', source='pay_method', dest='cancel')
        self.machine.add_transition(trigger='cancel', source='pizza_size', dest='cancel')
        self.machine.add_transition(trigger='end', source='cancel', dest='waiting')
        self.machine.add_transition(trigger='end', source='done', dest='waiting')

    def set_pizza_size(self, pizza_size):
        """Сеттер на размер пиццы"""
        self.pizza_size = pizza_size

    def set_pay_method(self, pay_method):
        """Сеттер на метод оплаты"""
        self.pay_method = pay_method
