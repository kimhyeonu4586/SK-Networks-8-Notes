from customer.repository.customer_repository_impl import CustomerRepositoryImpl
from mart.repository.mart_repository_impl import MartRepositoryImpl
from order.repository.order_repository_impl import OrderRepositoryImpl
from order.service.order_service import OrderService


class OrderServiceImpl(OrderService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__orderRepository = OrderRepositoryImpl.getInstance()
            cls.__instance.__martRepository = MartRepositoryImpl.getInstance()
            cls.__instance.__customerRepository = CustomerRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def __checkAvailability(self, fruitName, quantity):
        fruitMap = self.__martRepository.mapList()

        if fruitName in fruitMap:
            if fruitMap[fruitName] >= quantity:
                return True

        return False

    def buyFruit(self, fruitName, fruitCount, customerId):
        isValid = self.__checkAvailability(fruitName, fruitCount)

        if isValid is True:
            print("주문이 유효합니다")
            self.__martRepository.update(fruitName, -fruitCount)
            self.__orderRepository.create(fruitName, fruitCount, customerId) # order 객체 생성
            return

        print("주문이 유효하지 않습니다")

    def orderList(self, customerId):
        customer = self.__customerRepository.findById(customerId)
        print(f"{customer.getName()} 님의 구매 내역입니다.")

        orderInfo = self.__orderRepository.findOrderByCustomerId(customerId)
        print(f"주문 항목: {orderInfo.getFruitName()}, 주문 수량: {orderInfo.getQuantity()}")
