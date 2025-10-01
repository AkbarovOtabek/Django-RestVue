<template>
  <div class="page-category">
    <div class="culumn is-12">
      <h2 class="is-size-2 has-text-centered">{{ category.name }}</h2>
    </div>
    <div class="columns is-multiline">
      <ProductBox
        v-for="product in category.products"
        :key="product.id"
        :product="product"
      />
    </div>
  </div>
</template>

<script>
import ProductBox from "../components/ProductBox.vue";
import axios from "axios";
import { toast } from "bulma-toast";
export default {
  name: "Category",
  components: {
    ProductBox,
  },
  data() {
    return {
      category: {
        products: [],
      },
    };
  },
  mounted() {
    this.getCategory();
  },
  watch: {
    $route(to, from) {
      if (to.name === "Category") {
        this.getCategory();
      }
    },
  },
  methods: {
    async getCategory() {
      const categorySlug = this.$route.params.category_slug;
      this.$store.commit("setIsLoading", true);

      await axios
        .get(`/api/v1/products/${categorySlug}/`)
        .then((response) => {
          this.category = response.data;
        })
        .catch((error) => {
          console.log(error);
          toast({
            message: "Somethis went wrong. Please rty again",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right",
          });
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>
