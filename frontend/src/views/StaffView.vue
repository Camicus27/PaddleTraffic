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
                I am jake knowlton i guess
            </template>
            <template v-slot:contact>
                https://www.linkedin.com/in/jacob-knowlton/
            </template>
        </StaffBio>
        <StaffBio class="bio"
            image-path="https://cdn.discordapp.com/attachments/1147209389858619475/1230687236484501554/meAnime.png?ex=663439ce&is=6621c4ce&hm=072b79cbe03a7b863e65eca13d7a7439c2d67ca08edd7e20139351401afcf249&">
            <template v-slot:title>
                Ian McBride
            </template>
            <template v-slot:bio>
                Ian McBride is a driven BS/MS student in Computer Science at the University of Utah, with a B.S. in Computer Science and Applied Mathematics. He anticipates graduating in May 2025. Ian currently works as a Junior Developer at Hexagon IT Solutions in Draper, Utah, where he plays a key role in enhancing client deliverables and optimizing business operations through innovative technology solutions. With strong technical skills in programming languages such as Java, C#, Python, and various web technologies, Ian has contributed to a range of projects. Notably, he worked with his capstone team to develop PaddleTraffic. He also has a background in consumer IT support, providing network solutions and system optimizations from 2015 to 2020. Ian is an Eagle Scout, demonstrating his leadership and commitment to community service. His technical prowess and problem-solving abilities make him a promising professional in the technology sector.
            </template>
            <template v-slot:contact>
                https://www.linkedin.com/in/ianmmcbride/
            </template>
        </StaffBio>
        <StaffBio class="bio"
            image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:title>
                Brensen Villegas
            </template>
            <template v-slot:bio>
                Brensen Villegas is a driven Computer Science graduate student at the University of Utah, pursuing a Master of Science degree while also actively contributing as a Teaching Assistant. With a solid foundation established during his Bachelor's program, Brensen has gained diverse experience across various domains, from software engineering internships at prestigious organizations like the Church of Jesus Christ of Latter Day Saints to managing operations at Sparkling Ponds LLC. His proficiency spans a wide array of technologies, from Java and Python to React and Vue.js, showcasing his versatility in both backend and frontend development. Brensen's passion for problem-solving shines through in his projects, such as developing a full-stack web application for pickleball enthusiasts and crafting a compiler from scratch as part of his coursework. With strong technical acumen, excellent communication skills, and a commitment to continuous learning, Brensen is poised to make significant contributions in the field of computer science.
            </template>
            <template v-slot:contact>
                801-111-2222
            </template>
        </StaffBio>
        <StaffBio class="bio"
            image-path="https://media.licdn.com/dms/image/C5603AQFc98B9cSqmdw/profile-displayphoto-shrink_200_200/0/1642535153163?e=2147483647&v=beta&t=JIITcjzpVjOJ-hhPRLHnIJM0YUudqcPZvIuDA6vq9g8">
            <template v-slot:title>
                Camron Wilson
            </template>
            <template v-slot:bio>
                I am jacob knowlton
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