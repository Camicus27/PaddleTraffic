<script setup lang="ts">
import CommonHeader from '@/components/CommonHeader.vue';
import StaffBio from '@/components/StaffBio.vue'
import { useDisplay } from 'vuetify'
const { mobile } = useDisplay()

const env = import.meta.env
let dir: string
if (env.MODE === 'production')
    dir = '/static/'
else
    dir = ''
</script>

<template>
    <CommonHeader />
    <div class="top-bar">
        <v-btn :size="mobile ? 'small' : 'large'" color="#183400" @click="$router.push('/about')"
            variant="outlined">Back</v-btn>
        <h1>Project Staff</h1>
        <div></div>
    </div>
    <div class="grid">
        <StaffBio class="bio" :image-path="dir + 'jacob_profile.jpg'">
            <template v-slot:title>
                Jacob Knowlton
            </template>
            <template v-slot:bio>
                Jacob Knowlton is a top-achieving BS/MS student in Computer Science and Applied Mathematics at the
                University of Utah, on track for a June 2025 graduation with a 4.0 GPA. His academic excellence has
                earned him the Utah Flagship Scholarship and the Al Davis & Juliann D'Amore Scholarship. Jacob applies
                his problem-solving skills to real-world challenges, including the development of PaddleTraffic, his
                computer science capstone project designed to help pickleball players easily find available courts.

                His dedication to continuous learning is evident in his diverse coursework, including Artificial
                Intelligence, Computer Networks, Database Systems, and Advanced OS Implementation. Jacob balances his
                studies with professional roles as a Junior Developer at Hexagon IT Solutions and an Undergraduate
                Teaching Assistant at the University of Utah. He thrives in collaborative environments, applying his
                proficiency in Java, C#, Python, C++, and Rust to tackle diverse programming challenges.

                With his technical skills, Spanish fluency, and mathematical understanding, Jacob brings a valuable
                global perspective to problem-solving teams. Beyond the classroom, he demonstrates leadership and
                dedication as an Eagle Scout and a passionate long-distance runner. He actively engages with the tech
                community through the U of U Data Science Club and brings a creative touch to his work as a pianist and
                cellist.
            </template>
            <template v-slot:contact>
                <div class="d-flex-column">
                    <div>knowlton.jacob17@gmail.com</div>
                    <div>https://www.linkedin.com/in/jacob-knowlton/</div>
                </div>
            </template>
        </StaffBio>
        <StaffBio class="bio" :image-path="dir + 'ian_profile.png'">
            <template v-slot:title>
                Ian McBride
            </template>
            <template v-slot:bio>
                Ian McBride is a driven BS/MS student in Computer Science at the University of Utah, with a B.S. in
                Computer Science and Applied Mathematics. He anticipates graduating in May 2025. Ian currently works as
                a Junior Developer at Hexagon IT Solutions in Draper, Utah, where he plays a key role in enhancing
                client deliverables and optimizing business operations through innovative technology solutions. With
                strong technical skills in programming languages such as Java, C#, Python, and various web technologies,
                Ian has contributed to a range of projects. Notably, he worked with his capstone team to develop
                PaddleTraffic. He also has a background in consumer IT support, providing network solutions and system
                optimizations from 2015 to 2020. Ian is an Eagle Scout, demonstrating his leadership and commitment to
                community service. His technical prowess and problem-solving abilities make him a promising professional
                in the technology sector.
            </template>
            <template v-slot:contact>
                <div class="d-flex-column">
                    <div>imcb01@gmail.com</div>
                    <div>https://www.linkedin.com/in/ianmmcbride/</div>
                </div>
            </template>
        </StaffBio>
        <StaffBio class="bio" :image-path="dir + 'brensen_profile.JPEG'">
            <template v-slot:title>
                Brensen Villegas
            </template>
            <template v-slot:bio>
                Brensen Villegas is a driven Computer Science graduate student at the University of Utah, pursuing a
                Master of Science degree while also actively contributing as a Teaching Assistant. With a solid
                foundation established during his Bachelor's program, Brensen has gained diverse experience across
                various domains, from software engineering internships at prestigious organizations like the Church of
                Jesus Christ of Latter Day Saints to managing operations at Sparkling Ponds LLC. His proficiency spans a
                wide array of technologies, from Java and Python to React and Vue.js, showcasing his versatility in both
                backend and frontend development. Brensen's passion for problem-solving shines through in his projects,
                such as developing a full-stack web application for pickleball enthusiasts and crafting a compiler from
                scratch as part of his coursework. With strong technical acumen, excellent communication skills, and a
                commitment to continuous learning, Brensen is poised to make significant contributions in the field of
                computer science.
            </template>
            <template v-slot:contact>
                <div class="d-flex-column">
                    <div>brensen11@gmail.com</div>
                    <div>https://www.linkedin.com/in/brensen-villegas/</div>
                </div>
            </template>
        </StaffBio>
        <StaffBio class="bio" :image-path="dir + 'camron_profile.jpg'">
            <template v-slot:title>
                Camron Wilson
            </template>
            <template v-slot:bio>
                Camron Wilson is an ambitious Computer Science student at the University of Utah with a passion for
                technology and creativity. Throughout his academic tenure, Camron has actively engaged in various
                project affiliations, most notably contributing to his capstone project for the development of
                PaddleTraffic, as well as various smaller projects from mobile applications to open-source software.
                Beyond the classroom, Camron's interests extend into the vibrant worlds of gaming and web development.
                An avid gamer himself, he finds inspiration and joy in exploring different gaming platforms and
                experiences. This enthusiasm seamlessly transitions into his professional endeavors, where he channels
                his expertise in game development to create captivating experiences, including a published mobile game.
                Check out <a href="https://apps.apple.com/vn/app/holey-shoot/id6450563743">'Holey Shoot' on the App
                    Store</a>! Camron has honed skills in a broad range of areas including various programming languages
                such as Java, C#, Python, and C++, frameworks and APIs such as Vue.js, Spring.js, Node.js, and
                GoogleAPI, SQL databases such as MySQL, SQLite, and Postgres, as well as big data and data visualization
                with tools such as DOMO. He revels in the challenge of solving complex problems and writing elegant,
                maintainable code.
            </template>
            <template v-slot:contact>
                <div class="d-flex-column">
                    <div>CamronKWilson@gmail.com</div>
                    <div>https://www.linkedin.com/in/camron-wilson/</div>
                </div>
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