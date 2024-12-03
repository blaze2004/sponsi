<template>
    <FormContainer title="Sign In">
        <form @submit.prevent="handleSubmit">
            <div class="mb-4">
                <label for="email" class="d-block fw-medium mb-2">Email</label>
                <input id="email" v-model="email" type="email" required name="email" placeholder="Email" aria-label="Email" class="input" />
            </div>
            <div class="mb-4">
                <label for="password" class="d-block fw-medium mb-2">Password</label>
                <input
                    id="password"
                    v-model="password"
                    type="password"
                    required
                    name="password"
                    placeholder="Password"
                    aria-label="Password"
                    class="input"
                />
            </div>
            <div class="mb-4">
                <button type="submit" :disabled="loading" class="w-full btn btn-primary btn-lg"><Spinner v-if="loading" /> &nbsp;Sign In</button>
            </div>
            <div class="text-center">
                <RouterLink to="/signup" class="text-primary">Don't have an account? Sign Up</RouterLink>
            </div>
        </form>
    </FormContainer>
</template>

<script>
import FormContainer from '@/components/FormContainer.vue';
import Spinner from '@/components/Spinner.vue';
import { useUserStore } from '@/stores/user';
import { toast } from 'vue-sonner';

export default {
    components: { FormContainer, Spinner },
    data() {
        return {
            email: '',
            password: '',
            loading: false,
        };
    },
    methods: {
        async handleSubmit() {
            if (!this.email || !this.password) {
                toast.error('All fields are required.');
                return;
            }

            const store = useUserStore();
            this.loading = true;
            const res = await store.signIn({ email: this.email, password: this.password });
            this.loading = false;

            if (res) {
                this.$router.push('/dashboard');
            }
        },
    },
};
</script>
