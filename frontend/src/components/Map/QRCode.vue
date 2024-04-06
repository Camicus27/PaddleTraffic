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

const download = () => qrObj.download()
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