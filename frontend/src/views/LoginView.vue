<script setup lang="ts">
</script>

<template>
    <div id="login-wrapper">
        <header>
            <h1>Welcome Back!</h1>
            <p>Please enter your details</p>
        </header>

        <main>
            <form action="/profile/login/" method="POST" id="login_form">
                <div id="username_ct">
                    <label for="username">Username:</label>
                    <input type="text" name="username" id="username" autofocus tabindex="1" placeholder="Your Username..." required/>
                </div>
                <div id="password_ct">
                    <label for="password">Password:</label>
                    <input type="password" name="password" id="password" tabindex="2" placeholder="Your Password..." required/>
                </div>
                <div id="button_ct">
                    <button type="submit">Log in</button>
                </div>
                <div id="sign-up">
                    <p>Don't have an account yet?</p>
                    <RouterLink to="/create-account">Sign Up!</RouterLink>
                </div>
            </form>
        </main>
    </div>
</template>