<template>
  <div>
    <b-card
    v-if="data"
    :title="data.name"
    :img-src="setImage()"
    img-alt="Image"
    img-top
    tag="article"
    class="mb-2 detail-card"
    >
    <b-card-text>
      {{data.description}}
    </b-card-text>

    <b-button @click="moveRegister" href="#" variant="primary"
    >수정하기</b-button>

    <b-button @click="deleteMenu" href="#" variant="danger">삭제</b-button>
    <b-button @click="moveList" href="#" variant="outline-primary">
      목록</b-button>
    </b-card>
  </div>
</template>

<script>
import { api } from '@/utils/axios'
export default {
  data(){
    return{
      data: {}
    };
  },

  async created(){
    console.log(this.$route);
    console.log(this.$route.params.id);
    const result = await api.menus.findOne(this.$route.params.id);
    
    this.data = result.data;
    console.log(this.data);
  },
  methods :{
    setImage(){
      console.log(this.data.image_src);
      return `http://43.200.145.225:8080/${this.data.image_src}`;
    },

    moveRegister(){
      this.$router.push(`/admin/menus/register/${this.$route.params.id}`);
    },
    async deleteMenu(){
      const confirmResult = confirm("삭제하시겠습니까?");
      if(confirmResult){
        const result = await api.menus.delete(this.$route.params.id);
        alert(result.data.message);
        this.$router.push("/admin/menus");
      }
      console.log("삭제 구현");
    },
    moveList(){
      this.$router.push("/admin/menus");
    },
  },
}
</script>

<style scoped>

</style>
