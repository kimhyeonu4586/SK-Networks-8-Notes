export interface CartState {
  cartList: Cart[]
  cart: Cart | null

  currentPage: Number
  totalPages: Number
}

export interface Cart {
  id: number
  title: string
  price: number
  description: string
  quantity: number
  image: string
}
  