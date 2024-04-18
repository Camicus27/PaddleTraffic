<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';
import StaffBio from '@/components/StaffBio.vue'
</script>

<template>
  <CommonHeader />
    <h1 class="mt-4">Project Staff</h1>
    <div class="grid">
        <StaffBio class="bio" 
        image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:bio>
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake knowlton
            </template>
            <template v-slot:contact>
                801-111-2222
            </template>
        </StaffBio>
        <StaffBio class="bio" 
        image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:bio>
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake knowlton
            </template>
            <template v-slot:contact>
                801-111-2222
            </template>
        </StaffBio>
        <StaffBio class="bio" 
        image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:bio>
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake knowlton
            </template>
            <template v-slot:contact>
                801-111-2222
            </template>
        </StaffBio>
        <StaffBio class="bio" 
        image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:bio>
                I am jake knowlton I am jake knowltonI am jake knowltonI am jake knowltonI am jake knowltonI am jake knowlton
            </template>
            <template v-slot:contact>
                801-111-2222
            </template>
        </StaffBio>
    </div>
</template>

<style scoped lang="scss">
    .grid {
        display: grid;
        gap: 15px;
        grid-template-columns: repeat(1, 1fr);
        margin-top: 30px;
    }
</style>