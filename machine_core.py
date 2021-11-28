from transitions import Machine


class PizzaBoy:  # Отсылочка к ремастеру строй игры) (GTA Vice City)
    """Класс описывющий стейт-машину для бота."""

    state = [
        'waiting',
        'pizza_size',
        'pay_method',
        'confirm',
        'cancel',
        'done'
    ]

    def __init__(self) -> None:
        self.__pizza_size = None
        self.__pay_method = None

        self.machine = Machine(
            model=self,
            states=PizzaBoy.state,
            initial='waiting'
        )

        self.machine.add_transition(
            trigger='start', source='waiting', dest='pizza_size'
        )
        self.machine.add_transition(
            trigger='next', source='pizza_size', dest='pay_method'
        )
        self.machine.add_transition(
            trigger='next', source='pay_method', dest='confirm'
        )
        self.machine.add_transition(
            trigger='done', source='confirm', dest='done'
        )
        self.machine.add_transition(
            trigger='cancel', source='confirm', dest='cancel'
        )
        self.machine.add_transition(
            trigger='cancel', source='pay_method', dest='cancel'
        )
        self.machine.add_transition(
            trigger='cancel', source='pizza_size', dest='cancel'
        )
        self.machine.add_transition(
            trigger='end', source='cancel', dest='waiting'
        )
        self.machine.add_transition(
            trigger='end', source='done', dest='waiting'
        )

    def set_pizza_size(self, pizza_size) -> None:
        """Сеттер на размер пиццы"""
        self.__pizza_size = pizza_size

    def set_pay_method(self, pay_method) -> None:
        """Сеттер на метод оплаты"""
        self.__pay_method = pay_method

    def set_pizza_size_none(self) -> None:
        """Онуление размера"""
        self.__pizza_size = None

    def set_pay_method_none(self) -> None:
        """Онуление сбособа оплаты"""
        self.__pay_method = None

    def get_pizza_size(self) -> str:
        """Геттер на размер пиццы"""
        return self.__pizza_size

    def get_pay_method(self) -> str:
        """Геттер на метод оплаты"""
        return self.__pay_method
