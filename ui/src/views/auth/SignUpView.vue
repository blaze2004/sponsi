<template>
    <FormContainer title="Sign Up">
        <form @submit.prevent="handleSubmit">
            <div class="mb-4">
                <label for="name" class="d-block fw-medium mb-2">Name</label>
                <input id="name" v-model="formData.name" type="text" required name="name" placeholder="Name" aria-label="Name" class="input" />
            </div>
            <div class="mb-4">
                <label for="email" class="d-block fw-medium mb-2">Email</label>
                <input id="email" v-model="formData.email" type="email" required name="email" placeholder="Email" aria-label="Email" class="input" />
            </div>
            <div class="mb-4">
                <label for="role" class="d-block fw-medium mb-2">What describes you best?</label>
                <div class="d-flex justify-content-between align-items-center gap-2">
                    <div class="input d-flex align-items-center p-3 gap-2">
                        <input id="sponsor" v-model="formData.role" type="radio" name="role" value="sponsor" required class="form-check-input" />
                        <label class="form-check-label ml-2" for="sponsor">Sponsor</label>
                    </div>
                    <div class="input d-flex align-items-center p-3 gap-2">
                        <input
                            id="influencer"
                            v-model="formData.role"
                            type="radio"
                            name="role"
                            value="influencer"
                            required
                            class="form-check-input"
                        />
                        <label class="form-check-label ml-2" for="influencer">Influencer</label>
                    </div>
                </div>
            </div>
            <div class="mb-4">
                <label for="password" class="d-block fw-medium mb-2">Password</label>
                <input
                    id="password"
                    v-model="formData.password"
                    type="password"
                    required
                    name="password"
                    placeholder="Password"
                    aria-label="Password"
                    class="input"
                />
            </div>
            <div class="mb-4">
                <label for="password2" class="d-block fw-medium mb-2">Confirm Password</label>
                <input
                    id="password2"
                    v-model="formData.password2"
                    type="password"
                    required
                    name="password2"
                    placeholder="Confirm Password"
                    aria-label="Confirm Password"
                    class="input"
                />
            </div>
            <div class="mb-4">
                <button type="submit" :disabled="loading" class="w-full btn btn-primary btn-lg"><Spinner v-if="loading" /> &nbsp;Sign Up</button>
            </div>
            <div class="text-center">
                <RouterLink to="/signin" class="text-primary">Already have an account? Sign In</RouterLink>
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
            loading: false,
            formData: {
                name: '',
                email: '',
                role: '',
                password: '',
                password2: '',
            },
        };
    },
    methods: {
        async handleSubmit() {
            const { name, email, role, password, password2 } = this.formData;

            if (!name || !email || !role || !password || !password2) {
                toast.error('All fields are required.');
                return;
            }

            if (password !== password2) {
                toast.error('Passwords do not match.');
                return;
            }

            const formData = new FormData();
            for (const key in this.formData) {
                formData.append(key, this.formData[key]);
            }

            const store = useUserStore();
            this.loading = true;
            const res = await store.signUp(formData);
            this.loading = false;

            if (res) {
                this.$router.push('/signin');
            }
        },
    },
};
</script>
