<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';
import StaffBio from '@/components/StaffBio.vue'
import { useDisplay } from 'vuetify'

const { mobile } = useDisplay()
</script>

<template>
    <CommonHeader />
    <div class="top-bar">
        <v-btn :size="mobile ? 'small' : 'large'" color="#183400" @click="$router.push('/about')" variant="outlined">Back to About</v-btn>
        <h1>Project Staff</h1>
        <div></div>
    </div>
    <div class="grid">
        <StaffBio class="bio"
            image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:title>
                Jacob Knowlton
            </template>
            <template v-slot:bio>
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake
                knowlton
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake
                knowlton
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake
                knowlton
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake
                knowlton
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake
                knowlton
            </template>
            <template v-slot:contact>
                801-111-2222
            </template>
        </StaffBio>
        <StaffBio class="bio"
            image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:bio>
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake
                knowlton
            </template>
            <template v-slot:contact>
                801-111-2222
            </template>
        </StaffBio>
        <StaffBio class="bio"
            image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:bio>
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake
                knowlton
            </template>
            <template v-slot:contact>
                801-111-2222
            </template>
        </StaffBio>
        <StaffBio class="bio"
            image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:bio>
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake
                knowlton
            </template>
            <template v-slot:contact>
                801-111-2222
            </template>
        </StaffBio>
    </div>
</template>

<style scoped lang="scss">
@use '@/styles/abstracts' as *;

.grid {
    display: grid;
    gap: 15px;
    grid-template-columns: repeat(1, 1fr);
    padding: 24px;
}

.top-bar {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    padding: 20px;

    button {
        width: fit-content;

        &:hover {
            background-color: lighten($pickle-100, 15%);
        }
    }
}

h1 {
    @include responsive($mobile-size) {
        font-size: 2.5rem;
        line-height: 2.5rem;
    }
}
</style>