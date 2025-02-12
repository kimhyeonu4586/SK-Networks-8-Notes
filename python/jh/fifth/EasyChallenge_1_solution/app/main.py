from mart.entity.fruit import Fruit
from mart.service.mart_service_impl import MartServiceImpl
from order.service.order_service_impl import OrderServiceImpl
from customer.service.customer_service_impl import CustomerServiceImpl

martService = MartServiceImpl.getInstance()
martService.loadFruit(Fruit.APPLE, 3)
martService.loadFruit(Fruit.ORANGE, 5)
fruitList = martService.fruitMapList()
print(f"현재 저희 매장에 남은 과일은: {fruitList}")

customerService = CustomerServiceImpl.getInstance()
customerName = customerService.createCustomer('code_man')

orderService = OrderServiceImpl.getInstance()
orderService.buyFruit(Fruit.APPLE, 2, customerName)

fruitList = martService.fruitMapList()
print(f"주문 이후 매장에 남은 과일은: {fruitList}")

orderService.orderList(customerName)