<template>
  <div>
      <div @click="moveDetail(order.id)" v-for="order in orders" :key="order.id">
        <div class="order-container">
          <div>
            주문 번호 : {{order.id}}
          </div>

          <div class="menu-info-wrapper">
            <p class="order-detail"> 주문 메뉴 : {{ order.menu_name }}<br>주문 갯수 : {{ order.quantity}}<br> 주문 디테일 : {{order.request_detail }}</p>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import { api } from "@/utils/axios";
export default {
  data() {
    return {
      orders: [],
    };
  },
  async created() {
    this.$store.commit("SET_TITLE", "주문 목록");
    const result = await api.orders.findAll();
    this.orders = result.data;
    console.log(this.orders);
  },
  methods: {
    moveDetail(id){
      this.$router.push(`/orders/${id}`)
    }
  },
};
</script>

<style>
.order-container {
  display: flex;
  align-content: center;
  border-bottom: 3px solid black;
}

.order-info-wrapper {
  margin: 0 auto;
  text-align: center;
}

.order-menu {
  font-size: 25px;
  font-weight: bold;
}

.order-detail {
  padding-top: 25px;
  padding-bottom: 0px;
}


</style>
