// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    ssr: false,
    router: {
        options: {
            hashMode: true
        }
    },
    runtimeConfig: {
        public: {
          server_url: process.env.server_url,
        }
    },
    modules: [],

    css: ['@/assets/scss/style.scss'],
})
