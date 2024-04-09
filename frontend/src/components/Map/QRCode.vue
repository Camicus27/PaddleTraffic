<script setup lang="ts">
import { onMounted, ref } from 'vue';
import options from './options'
import QRCodeStyling from 'qr-code-styling';

const qrCode = ref<HTMLElement | undefined>()
const props = defineProps<{
    url: string
}>()

let qrObj = new QRCodeStyling(options)

qrObj.update({
    data: props.url
})

const download = (name: string | undefined) => {
    const download_options: any = { // or hatever, JS
        name: 'qr-code',
        extension: 'png'
    }

    if (name) {
        download_options.name = name
    }
    qrObj.download(download_options)
}
defineExpose({
    download
})

onMounted(() => {
    qrObj.append(qrCode.value)
})
</script>

<template>
    <div id="qr-code" ref="qrCode"></div>
</template>

<style scoped lang="scss"></style>