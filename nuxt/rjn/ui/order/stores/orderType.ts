// 개별 주문 항목 (OrderItem) 인터페이스
export interface OrderItem {
  id: number; // 상품 ID
  title: string; // 상품명
  price: number; // 상품 가격
  description: string; // 상품 설명
  quantity: number; // 수량
  image: string; // 이미지 URL
  total: number; // 총 금액 (price * quantity)
}

// 주문(Order) 인터페이스
export interface Order {
  id: number; // 주문 ID
  userId: number; // 사용자 ID
  orderDate: string; // 주문 날짜
  totalAmount: number; // 주문 총 금액
  status: "pending" | "completed" | "canceled"; // 주문 상태
  items: OrderItem[]; // 주문 항목 배열
  shippingAddress?: string; // 배송 주소 (선택)
  deliveryDate?: string; // 예상 배송일 (선택)
}
